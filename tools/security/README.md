# Temporary FB-7 fail-closed scanner integration

**Owner-authorized local mitigation, not an upstream fix or checkpoint approval.**
See [ADR-0003](../../docs/decisions/0003-temporary-fail-closed-scanner-integration.md)
and [FB-7](../../FRAMEWORK_FEEDBACK.md#fb-7--security-gate-accepts-operational-scanner-errors-and-non-sarif-json-objects).
No file or pin inside `.framework` is changed.

## Why an exit code is not sufficient

The pinned framework ignores execution status once it can read a JSON object.
The adapter must therefore **withhold the configured `results` file on any
execution or validation failure**. The real gate then reports `SCAN_NOT_RUN`.
An error plus a published clean report would still be unsafe.

## Contract

1. Remove an earlier published report, including on direct invocations.
2. Run the selected binary without a shell, from the product root, with a
   private per-run raw report, stdout/stderr and native exit in
   `.qf/security-scans/<scanner>-<unique>/`. Directories are mode 0700 and are
   ignored by Git. Logs may contain sensitive diagnostics: do not publish them.
3. Allow completed OSV exits **0/1** only. Reserve other statuses for rejection,
   including 127 (error), 128 (no packages), and future/unsupported result codes.
   Reserved 2–126 are **not** redefined as OSV general errors; support needs an
   explicit reviewed contract before they can be accepted.
4. Invoke Gitleaks with its native `--redact=100 --exit-code 3`: completed scans
   use **0/3**. Its default 1 is ambiguous: both findings and partial/error scans
   use it. With the explicit flag, operational exit 1 always blocks, even when
   accompanied by an apparently valid report containing findings.
5. Validate against the full vendored OASIS SARIF 2.1.0 schema using `jsonschema`
   (already a framework runtime dependency). Check the schema's digest; never
   fetch schemas or report references during a run. Reject duplicate JSON keys,
   non-finite constants, empty/null runs, metadata-only runs lacking `results`,
   external results, mismatched driver names and explicit invocation errors.
   Reject invalid/non-finite/out-of-range security severity values.
6. Require status/results consistency: exit 0 has no findings; the selected
   findings exit has at least one result. A well-formed empty `results: []` is
   allowed for a completed clean scan, not for an operational failure.
7. Publish **the exact original bytes**, without filtering findings or changing
   scores, by atomic replacement only after validation and diagnostic recording.
   Preserve the native exit (OSV findings remain 1, Gitleaks findings remain 3).
   High/critical/unscored findings are still decided by the original gate; a
   medium 6.9 finding can still pass as required by its policy.

Timeout is 600 seconds per scan, below the framework's 900-second command timeout.
The adapter kills the scanner process group on timeout/interruption. Reports
larger than 32 MiB are rejected, not truncated or declared clean. Setup, missing
binary/validator, malformed report and unsupported-status failures publish
nothing. Raw evidence remains separate from the exact file the gate consumes.

This only protects the two declared scanner commands. It does **not** fix other
products, every gate, scanner internals, scanning coverage or missing binaries.
It assumes the repository/toolchain is trusted; it is not a sandbox for hostile
scanner executables. Infrastructure tooling is Python 3.12+ using the existing
framework runtime dependencies; the browser/server remain TypeScript.

## Checks without installing/running real scanners

From the repository root, in the Python environment used by the framework:

```sh
FB7_EVIDENCE=docs/architecture/evidence/fail-closed-scanner-checks.json \
  python3 -B -m unittest discover -s tests/tooling -p 'test_*.py' -v
```

The tests execute **the actual proposed `run` commands**, actual subprocesses
and the actual unchanged framework gate. Only `osv-scanner`/`gitleaks` are doubles
on a temporary PATH. They use temporary product roots, no inherited provider
credentials and no network. They also exercise both actual stack rows together,
native statuses, stale reports, missing dependencies, schema tampering, timeout,
termination and framework run-cache replay.

The JSON contains asserted matrix observations; the unittest result separately
establishes whether the entire suite passed. The product-owned CI step runs the
suite and uploads **only synthetic regression metadata**, not raw diagnostics.
Existing framework CI commands, triggers and permissions remain unchanged.

These are tooling regression tests, **not** application unit/software tests or
a real vulnerability scan. No real scanner binary was installed/run as part of
this mitigation. Native binary/lockfile scanning remains for the later toolchain
implementation; missing prerequisites block rather than fabricate success.

## Removal

Keep FB-7 **open**, with the workaround named. Report it upstream separately
when authorized; no issue/PR or release is implied by this local work.
After a released upstream version protects the same error/report cases:

1. Review and authorize the submodule version change through a product PR.
2. Run equivalent negative/positive regressions against the corrected gate
   **without this adapter**, including both scanner exit contracts.
3. Restore direct native scanner commands, remove the adapter, vendored schema
   and temporary CI/test integration together, and record the verified removal
   in FB-7. Do not remove protection merely because a release number increased.

## Primary sources

- [OSV output and exit contract](https://google.github.io/osv-scanner/output/#return-codes).
- [OSV 2.7.1 SARIF writer](https://github.com/google/osv-scanner/blob/v2.7.1/internal/output/sarif.go).
- [Gitleaks 8.30.1 exit handling](https://github.com/gitleaks/gitleaks/blob/v8.30.1/cmd/root.go#L409-L467).
- [OASIS schema provenance/digest](vendor/README.md).
