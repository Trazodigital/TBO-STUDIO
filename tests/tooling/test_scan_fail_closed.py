"""FB-7 regression tests: real adapter/processes and real, unmodified framework gate.

Only scanner executables are doubles, resolved from a private temporary PATH.
No scanner installation, product scan, network access or provider credentials.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import yaml

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / ".framework"))
from gates.sup.scan_security_gate import check  # noqa: E402
from tools.read_product_config_tool import read_product_config  # noqa: E402
from tools.run_stack_commands_tool import run_command, read_stack  # noqa: E402

OBSERVATIONS = []
VERSIONS = {"osv-scanner": "2.7.1", "gitleaks": "8.30.1"}
AREAS = {"osv-scanner": "dependencies_scanner", "gitleaks": "secrets_scanner"}
RESULTS = {"osv-scanner": "reports/dependencies.sarif", "gitleaks": "reports/secrets.sarif"}

DOUBLE = '''#!{python}
import json, os, signal, sys, time
from pathlib import Path
plan = json.loads(Path(__file__).with_suffix('.json').read_text())
if '--version' in sys.argv or sys.argv[1:] == ['version']:
    print(plan['scanner'] + ' ' + plan['version'])
    sys.exit(0)
Path(__file__).with_suffix('.argv.json').write_text(json.dumps(sys.argv[1:]))
print('synthetic scanner diagnostic', file=sys.stderr)
if plan['raw'] is not None:
    if plan['scanner'] == 'osv-scanner':
        sys.stdout.buffer.write(plan['raw'].encode())
        sys.stdout.buffer.flush()
    else:
        Path(sys.argv[sys.argv.index('--report-path') + 1]).write_text(plan['raw'])
if plan.get('sleep'):
    time.sleep(plan['sleep'])
if plan.get('signal'):
    os.kill(os.getpid(), signal.SIGTERM)
sys.exit(plan['exit'])
'''


def report(scanner: str, score: str | None = None, *, finding: bool = False) -> dict:
    rule = {"id": "TEST-ONLY-RULE"}
    if score is not None:
        rule["properties"] = {"security-severity": score}
    return {"version": "2.1.0", "runs": [{
        "tool": {"driver": {"name": scanner, "rules": [rule] if finding else []}},
        "results": [{"ruleId": rule["id"], "message": {"text": "synthetic finding"},
                     "locations": [{"physicalLocation": {"artifactLocation": {"uri": "src/test.ts"},
                                                        "region": {"startLine": 4}}}]}]
                   if finding else [],
    }]}


class FailClosedIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="tbo-fb7-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "tools").mkdir()
        shutil.copytree(REPO / "tools/security", self.root / "tools/security")
        shutil.copyfile(REPO / "qf.yaml", self.root / "qf.yaml")
        (self.root / "docs/architecture").mkdir(parents=True)
        self.stack_path = self.root / "docs/architecture/stack.yaml"
        self.bin = self.root / "bin"
        self.bin.mkdir()
        # Deliberately do not inherit GH/Gemini/Loki or other credentials.
        self.environment = {"PATH": os.pathsep.join((str(self.bin), str(Path(sys.executable).parent), os.defpath)),
                            "PYTHONDONTWRITEBYTECODE": "1", "LC_ALL": "C.UTF-8"}

    def prepare(self, scanner, raw, code, **extra):
        if isinstance(raw, dict) or isinstance(raw, list):
            raw = json.dumps(raw, indent=2) + "\n"
        executable = self.bin / scanner
        executable.write_text(DOUBLE.format(python=sys.executable))
        executable.chmod(0o700)
        executable.with_suffix(".json").write_text(json.dumps({
            "scanner": scanner, "version": VERSIONS[scanner], "raw": raw, "exit": code, **extra,
        }))
        stack = yaml.safe_load((REPO / "docs/architecture/stack.yaml").read_text())
        stack["areas"] = [row for row in stack["areas"] if row["area"] == AREAS[scanner]]
        # This is the actual proposed run command, not a reconstruction of it.
        if extra.get("sleep"):
            stack["areas"][0]["run"] += " --timeout 0.05"
        self.stack_path.write_text(yaml.safe_dump(stack))
        return raw

    def diagnostic(self, scanner):
        paths = sorted((self.root / ".qf/security-scans").glob(f"{scanner}-*/diagnostic.json"))
        self.assertTrue(paths)
        latest = max(paths, key=lambda p: p.stat().st_mtime_ns)
        return json.loads(latest.read_text()), latest.parent

    def through_gate(self, case, scanner, raw, code, expected, **extra):
        original = self.prepare(scanner, raw, code, **extra)
        result_path = self.root / RESULTS[scanner]
        result_path.parent.mkdir(exist_ok=True)
        result_path.write_text(json.dumps(report(scanner)))  # stale success must not survive
        with patch.dict(os.environ, self.environment, clear=True):
            config = read_product_config(self.root)
            self.assertIsNotNone(read_stack(config), "invalid fixture stack would skip the gate")
            findings = check(config)
        rules = [finding.rule for finding in findings]
        self.assertEqual(rules, expected, case)
        accepted = "SCAN_NOT_RUN" not in expected
        self.assertEqual(result_path.is_file(), accepted, case)
        diagnostic, folder = self.diagnostic(scanner)
        self.assertEqual(diagnostic["report_accepted"], accepted)
        self.assertTrue((folder / "stderr.log").is_file())
        if not extra.get("sleep"):
            self.assertIn("synthetic scanner diagnostic", (folder / "stderr.log").read_text())
        if accepted:
            self.assertEqual(result_path.read_bytes(), original.encode(), "report was rewritten")
        # A timeout may kill the double before it writes all (or any) bytes.
        if raw is not None and not extra.get("sleep"):
            self.assertEqual((folder / "raw.sarif").read_bytes(), original.encode())
        if not extra:
            self.assertEqual(diagnostic["native_exit_code"], code)
        for finding in findings:
            if finding.rule == "SECURITY_FINDING":
                self.assertEqual((finding.file, finding.line), ("src/test.ts", 4))
        OBSERVATIONS.append({"case": case, "scanner": scanner,
                             "native_exit_code": diagnostic["native_exit_code"],
                             "report_accepted": accepted, "gate_rules": rules,
                             "published_bytes_match_original": True if accepted else None,
                             "reason": diagnostic["reason"]})

    def test_completed_scan_and_findings_keep_gate_severity_policy(self):
        for scanner, code in (("osv-scanner", 1), ("gitleaks", 3)):
            self.through_gate("clean", scanner, report(scanner), 0, [])
            for score, expected in (("3.1", []), ("6.9", []), ("7.0", ["SECURITY_FINDING"]),
                                    ("9.8", ["SECURITY_FINDING"]), (None, ["SECURITY_FINDING"])):
                with self.subTest(scanner=scanner, score=score):
                    self.through_gate(f"finding_{score}", scanner,
                                      report(scanner, score, finding=True), code, expected)

    def test_operational_and_reserved_exits_never_publish_even_valid_reports(self):
        for scanner in VERSIONS:
            self.through_gate("original_FB7_exit127_object", scanner, {}, 127, ["SCAN_NOT_RUN"])
            codes = (2, 126, 127, 128, 129, 255) if scanner == "osv-scanner" else (1, 2, 126, 127, 128, 255)
            for code in codes:
                for finding in (False, True):
                    with self.subTest(scanner=scanner, code=code, finding=finding):
                        self.through_gate(f"error_{code}_findings_{finding}", scanner,
                                          report(scanner, finding=finding), code, ["SCAN_NOT_RUN"])

    def test_malformed_reports_and_incomplete_runs_never_publish(self):
        for scanner in VERSIONS:
            malformed = {"object": {}, "array": [], "invalid_json": "{", "empty_file": "",
                         "missing": None, "empty_runs": {"version": "2.1.0", "runs": []},
                         "null_runs": {"version": "2.1.0", "runs": None}}
            for name in ("wrong_version", "wrong_driver", "no_results", "null_results", "bad_result",
                         "bad_rule", "failed_invocation", "invocation_error_exit", "error_notification",
                         "external_results", "malformed_score", "nan_score", "negative_score"):
                data = report(scanner)
                run = data["runs"][0]
                if name == "wrong_version":
                    data["version"] = "2.0.0"
                elif name == "wrong_driver":
                    run["tool"]["driver"]["name"] = "unrelated-tool"
                elif name == "no_results":
                    del run["results"]
                elif name == "null_results":
                    run["results"] = None
                elif name == "bad_result":
                    run["results"] = ["not a result"]
                elif name == "bad_rule":
                    run["tool"]["driver"]["rules"] = [None]
                elif name == "failed_invocation":
                    run["invocations"] = [{"executionSuccessful": False}]
                elif name == "invocation_error_exit":
                    run["invocations"] = [{"executionSuccessful": True, "exitCode": 127}]
                elif name == "error_notification":
                    run["invocations"] = [{"executionSuccessful": True, "toolExecutionNotifications": [
                        {"level": "error", "message": {"text": "synthetic operational error"}}]}]
                elif name == "external_results":
                    run["externalPropertyFileReferences"] = {"results": [{"location": {"uri": "other.sarif"}}]}
                else:
                    score = {"malformed_score": "unknown", "nan_score": "NaN", "negative_score": "-1"}[name]
                    run["tool"]["driver"]["rules"] = [{"id": "x", "properties": {"security-severity": score}}]
                malformed[name] = data
            valid = json.dumps(report(scanner))
            malformed["duplicate_key"] = valid.replace('"results": []', '"results": [], "results": []')
            malformed["nonfinite_json"] = valid.replace('"results": []', '"results": [], "properties": {"x": NaN}')
            for name, raw in malformed.items():
                with self.subTest(scanner=scanner, case=name):
                    self.through_gate(name, scanner, raw, 0, ["SCAN_NOT_RUN"])

    def test_exit_and_result_count_must_be_consistent(self):
        for scanner, finding_exit in (("osv-scanner", 1), ("gitleaks", 3)):
            self.through_gate("findings_exit_non_SARIF_object", scanner, {},
                              finding_exit, ["SCAN_NOT_RUN"])
            self.through_gate("findings_exit_without_results", scanner, report(scanner),
                              finding_exit, ["SCAN_NOT_RUN"])
            self.through_gate("clean_exit_with_results", scanner, report(scanner, finding=True),
                              0, ["SCAN_NOT_RUN"])

    def test_timeout_and_signal_block_partial_reports(self):
        for scanner in VERSIONS:
            self.through_gate("timeout", scanner, report(scanner), 0, ["SCAN_NOT_RUN"], sleep=2)
            self.through_gate("signal", scanner, report(scanner), 0, ["SCAN_NOT_RUN"], signal=True)

    def test_both_declared_scanners_run_together_with_the_original_stack(self):
        for scanner in VERSIONS:
            self.prepare(scanner, report(scanner), 0)
        self.stack_path.write_bytes((REPO / "docs/architecture/stack.yaml").read_bytes())
        with patch.dict(os.environ, self.environment, clear=True):
            self.assertEqual(check(read_product_config(self.root)), [])
        for scanner in VERSIONS:
            self.assertTrue((self.root / RESULTS[scanner]).is_file())
            diagnostic, _ = self.diagnostic(scanner)
            self.assertTrue(diagnostic["report_accepted"])
        self.prepare("gitleaks", report("gitleaks", finding=True), 1)  # partial scan, not findings exit 3
        self.stack_path.write_bytes((REPO / "docs/architecture/stack.yaml").read_bytes())
        with patch.dict(os.environ, self.environment, clear=True):
            findings = check(read_product_config(self.root))
        self.assertEqual([f.rule for f in findings], ["SCAN_NOT_RUN"])
        self.assertFalse((self.root / RESULTS["gitleaks"]).exists())
        self.assertTrue((self.root / RESULTS["osv-scanner"]).is_file())

    def test_direct_invocation_clears_stale_report_and_preserves_native_exits(self):
        for scanner, code in (("osv-scanner", 1), ("gitleaks", 3)):
            self.prepare(scanner, report(scanner, "6.9", finding=True), code)
            command = [sys.executable, "-B", "tools/security/scan_fail_closed.py",
                       "--scanner", scanner, "--results", RESULTS[scanner]]
            run = subprocess.run(command, cwd=self.root, env=self.environment, capture_output=True)
            self.assertEqual(run.returncode, code)
            self.prepare(scanner, {}, 0)
            run = subprocess.run(command, cwd=self.root, env=self.environment, capture_output=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertFalse((self.root / RESULTS[scanner]).exists())

    def test_missing_binary_and_validator_fail_closed(self):
        for scanner in VERSIONS:
            self.prepare(scanner, report(scanner), 0)
            (self.bin / scanner).unlink()
            with patch.dict(os.environ, self.environment, clear=True):
                findings = check(read_product_config(self.root))
            self.assertIn("SCAN_NOT_RUN", [finding.rule for finding in findings])
            self.assertFalse((self.root / RESULTS[scanner]).exists())
        # -S disables site-packages, so jsonschema really is unavailable in child.
        self.prepare("osv-scanner", report("osv-scanner"), 0)
        result = self.root / RESULTS["osv-scanner"]
        result.parent.mkdir(exist_ok=True)
        result.write_text("stale")
        run = subprocess.run([sys.executable, "-S", "-B", "tools/security/scan_fail_closed.py",
                              "--scanner", "osv-scanner", "--results", str(result)],
                             cwd=self.root, env=self.environment, capture_output=True)
        self.assertNotEqual(run.returncode, 0)
        self.assertFalse(result.exists())

    def test_schema_integrity_and_native_gitleaks_error_separation(self):
        self.prepare("gitleaks", report("gitleaks", finding=True), 3)
        with patch.dict(os.environ, self.environment, clear=True):
            self.assertEqual([f.rule for f in check(read_product_config(self.root))], ["SECURITY_FINDING"])
        argv = json.loads((self.bin / "gitleaks.argv.json").read_text())
        self.assertEqual(argv[argv.index("--exit-code") + 1], "3")
        self.assertIn("--redact=100", argv)
        (self.root / "tools/security/vendor/sarif-schema-2.1.0.json").write_text("{}")
        with patch.dict(os.environ, self.environment, clear=True):
            findings = check(read_product_config(self.root))
        self.assertEqual([f.rule for f in findings], ["SCAN_NOT_RUN"])

    def test_framework_reports_missing_result_even_with_cached_runs(self):
        self.prepare("osv-scanner", report("osv-scanner"), 127)
        config = read_product_config(self.root)
        entry = read_stack(config)["security_scans"]["dependencies"]
        with patch.dict(os.environ, self.environment, clear=True):
            first = run_command(config, "security_scans", "dependencies", entry, key="fb7-test")
            second = run_command(config, "security_scans", "dependencies", entry, key="fb7-test")
        self.assertEqual(first.exit_code, 127)
        self.assertEqual(first.results, [])
        self.assertEqual(second.results, [])


def tearDownModule():
    destination = os.environ.get("FB7_EVIDENCE")
    if destination:
        path = Path(destination)
        path.parent.mkdir(parents=True, exist_ok=True)
        schema = REPO / "tools/security/vendor/sarif-schema-2.1.0.json"
        pin = subprocess.check_output(["git", "-C", str(REPO / ".framework"), "rev-parse", "HEAD"],
                                      text=True).strip()
        path.write_text(json.dumps({
            "scope": "Synthetic scanners through actual adapter and unmodified framework gate; NOT real scanner runs",
            "framework_pin": pin,
            "python_version": sys.version.split()[0],
            "jsonschema_version": importlib.metadata.version("jsonschema"),
            "pyyaml_version": importlib.metadata.version("PyYAML"),
            "adapter_sha256": hashlib.sha256((REPO / "tools/security/scan_fail_closed.py").read_bytes()).hexdigest(),
            "tests_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "stack_sha256": hashlib.sha256((REPO / "docs/architecture/stack.yaml").read_bytes()).hexdigest(),
            "framework_gate_sha256": hashlib.sha256((REPO / ".framework/gates/sup/scan_security_gate.py").read_bytes()).hexdigest(),
            "schema_sha256": hashlib.sha256(schema.read_bytes()).hexdigest(),
            "note": "Only asserted matrix cases are recorded here; unittest success is required separately",
            "cases": OBSERVATIONS,
        }, indent=2) + "\n")


if __name__ == "__main__":
    unittest.main()
