# ADR-0003 — Temporary fail-closed scanner integration

```yaml decision
id: ADR-0003
title: Guard declared scanner reports until FB-7 is fixed upstream
status: proposed
date: "2026-11-12"
context: >-
  The independent reviewer requested changes on PR 10 at b94a3be because FB-7
  lets operational scanner errors and non-SARIF JSON pass the pinned framework
  gate. The owner explicitly authorized a local fail-closed adapter, regression
  tests and named feedback workaround, without changing .framework or its pin.
  This implementation authorization is not formal checkpoint 3 approval.
options:
  - name: Wait for a released upstream correction before continuing
    pros:
      - Repairs the shared gate for every product without local maintenance.
      - Follows the framework's preferred upstream correction path.
    cons:
      - Depends on external maintainers and has no confirmed delivery time.
      - Leaves the current checkpoint waiting while the defective integration remains selected.
  - name: Apply a temporary fail-closed adapter outside the framework
    pros:
      - Makes operational errors and invalid reports block using the existing SCAN_NOT_RUN gate behavior.
      - Allows local implementation and verification without waiting for an external release.
      - Preserves original report bytes and the gate's vulnerability severity policy.
    cons:
      - Requires maintenance, an explicit exception and independent re-review before acceptance.
      - Protects only the declared commands and does not repair the upstream gate.
      - Adds Python repository tooling and a vendored schema using the existing framework runtime.
choice: Apply a temporary fail-closed adapter outside the framework
consequences: >-
  Invoke tools/security/scan_fail_closed.py from both scanner run rows. Reject
  unsupported/operational exits and invalid/incomplete SARIF before atomically
  publishing unchanged reports. Use OSV native findings exit 1 and Gitleaks
  --exit-code 3 to separate completed findings from its operational exit 1.
  Maintain regression tests through the actual unchanged gate and run them as
  product-owned CI steps without changing mandatory framework steps. Retain
  raw diagnostics privately under ignored .qf/security-scans. Record every file
  and removal criteria in FB-7; keep it open until a released upstream fix is
  adopted and equivalent regressions pass without the adapter. Upstream issue
  publication, commit, push, merge, deployment and human checkpoint approval
  are not authorized by this record. No real scanner or provider run is claimed.
```

[Implementation contract and removal](../../tools/security/README.md) ·
[Executed synthetic evidence](../architecture/evidence/fail-closed-scanner-checks.json) ·
[Original FB-7 reproduction](../architecture/evidence/security-gate-reproduction.md).
