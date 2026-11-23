"""Removal evidence for the temporary FB-7 adapter (ADR-0003): the adapter's
regressions run against the unchanged native scan_security_gate of the pinned
framework, with no adapter in the command. The adapter may go only when every
case passes; on v5.4.9 the two FB-11 cases fail. Not a CI step: run it by hand
when the framework pin moves.

Two cases, a `results` that is an object and a result that is a string, pass on
SCAN_NOT_RUN or on a crash of the gate: the framework's runner reports a gate
that raises as GATE_CRASHED, a failed gate, so CI fails closed there too
(FB-11). Any other case that crashes fails.

Builds a throwaway copy of the product (qf.yaml + stack.yaml, no git, so no run
cache), rewrites only the two scanner rows to a stand-in scanner, and asserts the
gate's findings per case.

    python3 -B tools/security/native_gate_regressions.py .
"""

import json
import shutil
import sys
import tempfile
from pathlib import Path

import yaml

PRODUCT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(PRODUCT / ".framework"))

from gates.sup.scan_security_gate import check  # noqa: E402
from tools.read_product_config_tool import read_product_config  # noqa: E402
from tools.run_stack_commands_tool import read_stack  # noqa: E402

VERSIONS = {"gitleaks": "8.30.1", "osv-scanner": "2.7.1"}
COMPLETED = {"gitleaks": [0, 3], "osv-scanner": [0, 1]}
RESULTS = {"gitleaks": "reports/secrets.sarif", "osv-scanner": "reports/dependencies.sarif"}

SCANNER = r'''
import json, os, signal, sys, pathlib
tool = sys.argv[1]
if sys.argv[2] == "--version":
    print({"gitleaks": "8.30.1", "osv-scanner": "Scanner version: 2.7.1"}[tool]); sys.exit(0)
mode, out = sys.argv[2], pathlib.Path(sys.argv[3])
out.parent.mkdir(parents=True, exist_ok=True)
def sarif(results=(), name=tool):
    driver = {"name": name} if name else {}
    return json.dumps({"version": "2.1.0", "runs": [{"tool": {"driver": driver}, "results": list(results)}]})
def result(severity=None):
    r = {"ruleId": "R1", "message": {"text": "found"},
         "locations": [{"physicalLocation": {"artifactLocation": {"uri": "src/x.ts"}, "region": {"startLine": 2}}}]}
    if severity is not None:
        r["properties"] = {"security-severity": severity}
    return r
code = {
    "clean": (sarif(), 0),
    "operational-1-valid-report": (sarif(), 1),
    "operational-2-valid-report": (sarif(), 2),
    "foreign-exit-3": (sarif(), 3),
    "empty-object": ("{}", 0),
    "non-sarif-version": (json.dumps({"version": "2.0.0", "runs": []}), 0),
    "unnamed-tool": (sarif(name=None), 0),
    "truncated": ('{"version": "2.1.0", "runs": [', 0),
    "no-report": (None, 0),
    "secret-unscored": (sarif([result()]), 3),
    "dependency-high": (sarif([result("7.5")]), 1),
    "dependency-low": (sarif([result("3.1")]), 1),
    "signal": (sarif(), None),
    "leak-exit-no-results": (sarif(), 3),
    "clean-exit-with-leak": (sarif([result()]), 0),
    "results-not-a-list": (json.dumps({"version": "2.1.0", "runs": [{"tool": {"driver": {"name": tool}}, "results": {"a": 1}}]}), 0),
    "result-not-an-object": (json.dumps({"version": "2.1.0", "runs": [{"tool": {"driver": {"name": tool}}, "results": ["x"]}]}), 0),
    "runs-empty": (json.dumps({"version": "2.1.0", "runs": []}), 0),
}[mode]
if code[0] is not None:
    out.write_text(code[0])
if code[1] is None:
    os.kill(os.getpid(), signal.SIGKILL)
sys.exit(code[1])
'''

# (case, gitleaks mode, osv mode, expected sorted rules); CRASH_OR_NOT_RUN also
# accepts a crash of the gate, which run_gates reports as GATE_CRASHED.
CRASH_OR_NOT_RUN = "SCAN_NOT_RUN or GATE_CRASHED"
CASES = [
    ("both clean", "clean", "clean", []),
    ("gitleaks operational exit 1 with a valid clean report", "operational-1-valid-report", "clean", ["SCAN_NOT_RUN"]),
    ("osv operational exit 2 with a valid clean report", "clean", "operational-2-valid-report", ["SCAN_NOT_RUN"]),
    ("osv exit 3 is not its completed exit", "clean", "foreign-exit-3", ["SCAN_NOT_RUN"]),
    ("gitleaks {} report", "empty-object", "clean", ["SCAN_NOT_RUN"]),
    ("osv non-SARIF JSON (version 2.0.0)", "clean", "non-sarif-version", ["SCAN_NOT_RUN"]),
    ("gitleaks run without a tool name", "unnamed-tool", "clean", ["SCAN_NOT_RUN"]),
    ("osv truncated JSON", "clean", "truncated", ["SCAN_NOT_RUN"]),
    ("gitleaks stale report, no new one", "no-report", "clean", ["SCAN_NOT_RUN"]),
    ("gitleaks killed by a signal", "signal", "clean", ["SCAN_NOT_RUN"]),
    ("missing scanner binary", "missing-binary", "clean", ["SCAN_NOT_RUN", "TOOL_VERSION_MISMATCH"]),
    ("gitleaks leak exit 3, unscored", "secret-unscored", "clean", ["SECURITY_FINDING"]),
    ("osv high vulnerability exit 1", "clean", "dependency-high", ["SECURITY_FINDING"]),
    ("osv low vulnerability exit 1 keeps the severity policy", "clean", "dependency-low", []),
    ("both fail operationally together", "operational-1-valid-report", "operational-2-valid-report", ["SCAN_NOT_RUN", "SCAN_NOT_RUN"]),
    # FB-11: the edges the adapter guards and the native gate does not (v5.4.9).
    ("FB-11: gitleaks exit 3 (leaks) but zero results", "leak-exit-no-results", "clean", ["SCAN_NOT_RUN"]),
    ("FB-11: SARIF with no runs at all", "runs-empty", "clean", ["SCAN_NOT_RUN"]),
    ("gitleaks exit 0 (clean) but a leak result", "clean-exit-with-leak", "clean", ["SECURITY_FINDING"]),
    ("results is an object, not a list", "results-not-a-list", "clean", CRASH_OR_NOT_RUN),
    ("a result is a string, not an object", "result-not-an-object", "clean", CRASH_OR_NOT_RUN),
]


def build(work: Path, modes: dict[str, str]) -> Path:
    root = work / "product"
    if root.exists():
        shutil.rmtree(root)
    (root / "docs/architecture").mkdir(parents=True)
    shutil.copy(PRODUCT / "qf.yaml", root / "qf.yaml")
    (root / ".framework").symlink_to(PRODUCT / ".framework")
    (root / "scan.py").write_text(SCANNER)
    stack = yaml.safe_load((PRODUCT / "docs/architecture/stack.yaml").read_text())
    for row in stack["areas"]:
        tool = row.get("tool")
        if row.get("area") in ("secrets_scanner", "dependencies_scanner"):
            mode = modes[tool]
            row["version_command"] = f"{sys.executable} scan.py {tool} --version"
            row["run"] = (
                f"no-such-scanner-binary --out {RESULTS[tool]}"
                if mode == "missing-binary"
                else f"{sys.executable} scan.py {tool} {mode} {RESULTS[tool]}"
            )
            if mode == "missing-binary":
                row["version_command"] = "no-such-scanner-binary version"
            row["results"] = RESULTS[tool]
            row["completed_exit_codes"] = COMPLETED[tool]
    (root / "docs/architecture/stack.yaml").write_text(yaml.safe_dump(stack, sort_keys=False))
    if modes["gitleaks"] == "no-report":  # a clean report left by an earlier run
        (root / "reports").mkdir()
        (root / RESULTS["gitleaks"]).write_text(
            json.dumps({"version": "2.1.0", "runs": [{"tool": {"driver": {"name": "gitleaks"}}, "results": []}]})
        )
    return root


def main() -> int:
    failures = 0
    with tempfile.TemporaryDirectory() as tmp:
        for name, gitleaks, osv, expected in CASES:
            root = build(Path(tmp), {"gitleaks": gitleaks, "osv-scanner": osv})
            config = read_product_config(root)
            assert read_stack(config) is not None, "stack must validate, or the gate returns [] silently"
            try:
                findings = check(config)
            except Exception as error:  # run_gates reports it as GATE_CRASHED: fails closed
                ok = expected == CRASH_OR_NOT_RUN
                failures += not ok
                print(f"{'PASS' if ok else 'FAIL'}  {name}: gate crashed, {type(error).__name__}: {error}")
                continue
            rules = sorted(f.rule for f in findings)
            ok = rules == (["SCAN_NOT_RUN"] if expected == CRASH_OR_NOT_RUN else sorted(expected))
            failures += not ok
            print(f"{'PASS' if ok else 'FAIL'}  {name}: {rules}")
            if not ok:
                for f in findings:
                    print(f"      {f.rule}: {f.message}")
    print(f"\n{len(CASES) - failures}/{len(CASES)} passed against {PRODUCT / '.framework'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
