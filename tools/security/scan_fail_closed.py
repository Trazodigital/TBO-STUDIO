"""Temporary FB-7 integration; remove only after an upstream fix is verified.

Publish an original scanner report atomically only after checking execution and
SARIF. The unmodified framework rejects the absent report on every failure.
This is repository tooling, not the TypeScript application or a replacement gate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile

SCHEMA = Path(__file__).parent / "vendor" / "sarif-schema-2.1.0.json"
SCHEMA_SHA256 = "c3b4bb2d6093897483348925aaa73af03b3e3f4bd4ca38cef26dcb4212a2682e"
MAX_REPORT_BYTES = 32 * 1024 * 1024
FINDING_EXIT = {"osv-scanner": 1, "gitleaks": 3}


class RejectedScan(ValueError):
    """A scan that must never leave a report where the gate looks for one."""


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise RejectedScan("duplicate JSON property")
        result[key] = value
    return result


def _invalid_constant(value: str) -> None:
    raise RejectedScan("non-finite JSON constant")


def validate_report(raw: bytes, scanner: str, exit_code: int) -> None:
    # Imported after the output is removed: missing validator also fails closed.
    from jsonschema import Draft4Validator

    schema_bytes = SCHEMA.read_bytes()
    if hashlib.sha256(schema_bytes).hexdigest() != SCHEMA_SHA256:
        raise RejectedScan("vendored SARIF schema integrity mismatch")
    schema = json.loads(schema_bytes)
    Draft4Validator.check_schema(schema)
    data = json.loads(raw, object_pairs_hook=_unique_object, parse_constant=_invalid_constant)
    error = next(Draft4Validator(schema).iter_errors(data), None)
    if error is not None:
        # Do not print instance values: they may contain secrets.
        raise RejectedScan("SARIF 2.1.0 schema violation")
    if not data["runs"] or data.get("inlineExternalProperties"):
        raise RejectedScan("expected nonempty, self-contained SARIF runs")

    count = 0
    for run in data["runs"]:
        if run["tool"]["driver"]["name"] != scanner:
            raise RejectedScan("SARIF driver does not match the selected scanner")
        if not isinstance(run.get("results"), list) or run.get("externalPropertyFileReferences"):
            raise RejectedScan("expected inline results array, not metadata or external results")
        count += len(run["results"])
        invocations = list(run.get("invocations", []))
        if run.get("conversion"):
            invocations.append(run["conversion"]["invocation"])
        for invocation in invocations:
            if invocation.get("executionSuccessful") is False:
                raise RejectedScan("SARIF reports unsuccessful execution")
            if invocation.get("exitCode", exit_code) not in (0, FINDING_EXIT[scanner]):
                raise RejectedScan("SARIF invocation reports an operational error")
            for field in ("toolExecutionNotifications", "toolConfigurationNotifications"):
                if any(n.get("level") == "error" for n in invocation.get(field, [])):
                    raise RejectedScan("SARIF reports a tool execution/configuration error")
        # Reject malformed numerical severities instead of letting float() hide
        # non-finite/out-of-range values. Do not change any legitimate score.
        components = [run["tool"]["driver"], *run["tool"].get("extensions", [])]
        items = [*run["results"], *(r for c in components for r in c.get("rules", []))]
        for item in items:
            value = item.get("properties", {}).get("security-severity")
            if value is not None:
                try:
                    score = float(value)
                except (TypeError, ValueError):
                    raise RejectedScan("invalid security-severity") from None
                if isinstance(value, bool) or not math.isfinite(score) or not 0 <= score <= 10:
                    raise RejectedScan("invalid security-severity")
    if (exit_code == FINDING_EXIT[scanner]) != (count > 0):
        raise RejectedScan("scanner exit and SARIF result count disagree")


def _command(scanner: str, raw: Path) -> list[str]:
    if scanner == "osv-scanner":
        return [scanner, "scan", "source", "--format", "sarif", "--lockfile", "package-lock.json"]
    # Default Gitleaks exit 1 is ambiguous: both leaks and partial scans use it.
    # Its native flag separates completed findings (3) from operational errors (1).
    return [scanner, "git", "--redact=100", "--exit-code", "3", "--report-format", "sarif",
            "--report-path", str(raw)]


def scan(scanner: str, results: Path, timeout: float) -> int:
    results = results.absolute()
    # Clear even when invoked directly (the framework also clears old reports).
    results.unlink(missing_ok=True)
    diagnostics_root = Path.cwd() / ".qf" / "security-scans"
    diagnostics_root.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix=f"{scanner}-", dir=diagnostics_root))
    raw = folder / "raw.sarif"
    command = _command(scanner, raw)
    status = {"scanner": scanner, "command": command, "native_exit_code": None,
              "report_accepted": False, "reason": "not completed"}
    candidate = None
    try:
        stdout_path = raw if scanner == "osv-scanner" else folder / "stdout.log"
        with stdout_path.open("wb") as stdout, (folder / "stderr.log").open("wb") as stderr:
            process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=stdout,
                                       stderr=stderr, start_new_session=True)
            try:
                status["native_exit_code"] = process.wait(timeout=timeout)
            except BaseException:
                # Stop descendants too, so none can publish a late/partial result.
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.wait()
                status["native_exit_code"] = process.returncode
                raise
        if status["native_exit_code"] not in (0, FINDING_EXIT[scanner]):
            raise RejectedScan("operational or unsupported scanner exit")
        if raw.stat().st_size > MAX_REPORT_BYTES:
            raise RejectedScan("SARIF exceeds the 32 MiB safety limit")
        report = raw.read_bytes()
        validate_report(report, scanner, status["native_exit_code"])
        results.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(prefix=".fb7-", dir=results.parent, delete=False) as target:
            candidate = Path(target.name)
            target.write(report)
            target.flush()
            os.fsync(target.fileno())
        status.update(report_accepted=True, reason="validated original report")
        (folder / "diagnostic.json").write_text(json.dumps(status, indent=2) + "\n")
        # Last operation that can publish: no fabricated/reformatted SARIF.
        os.replace(candidate, results)
    except (Exception, KeyboardInterrupt) as error:
        results.unlink(missing_ok=True)
        reason = str(error) if isinstance(error, RejectedScan) else type(error).__name__
        status.update(report_accepted=False, reason=reason)
        (folder / "diagnostic.json").write_text(json.dumps(status, indent=2) + "\n")
        print(f"FB-7: scan rejected ({reason}); diagnostics: {folder}", file=sys.stderr)
        native = status["native_exit_code"]
        return native if isinstance(native, int) and 0 < native < 256 else 2
    finally:
        if candidate is not None:
            candidate.unlink(missing_ok=True)
    print(f"FB-7: original SARIF validated; diagnostics: {folder}")
    return status["native_exit_code"]


def _timeout(value: str) -> float:
    seconds = float(value)
    if not math.isfinite(seconds) or not 0 < seconds <= 600:
        raise argparse.ArgumentTypeError("timeout must be between 0 and 600 seconds")
    return seconds


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scanner", required=True, choices=tuple(FINDING_EXIT))
    parser.add_argument("--results", required=True, type=Path)
    parser.add_argument("--timeout", type=_timeout, default=600.0)
    args = parser.parse_args()
    try:
        return scan(args.scanner, args.results, args.timeout)
    except (OSError, KeyboardInterrupt) as error:
        print(f"FB-7: cannot prepare scan ({type(error).__name__})", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
