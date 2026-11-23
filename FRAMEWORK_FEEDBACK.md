# Framework feedback

Running log of Quality Framework weaknesses found while building this product
(principle #47). Copy it to the product as *qf.yaml paths.framework_feedback_file*;
*check_framework_feedback_gate* checks it on every pull request.

**What belongs here:** anything the framework claims that is not true, anything
it enforces that it should not, and anything it says it enforces and does not.
Evidenced findings only — a command that was run and the output it produced. A
finding only reasoned about is a hypothesis; say so in **Verification**.

**Do not patch around the framework locally.** Record the gap here and leave the
product in its honest state. A local workaround hides the defect from every
other product built on the framework. If you must unblock, name exactly what you
did in **Workaround applied** and mark it for removal.

**On every framework version bump** — a change of the submodule at
*paths.framework_dir* — record what you found, or a line naming the new
version: *No findings for v6.1.0 (a1b2c3d)*. Silence is indistinguishable from
having forgotten.

## How to use this file

One `### FB-<n>` entry per finding, newest first under **Log**. Never edit a
closed entry: add a follow-up and link it. Fill every field; write `n/a` rather
than deleting one, so a missing answer stays visible.

| Severity | Meaning |
|---|---|
| critical | A gate reports success without checking: a green build that means nothing. |
| high | A declared gate has no implementation, or a document asserts something false. |
| medium | A contract defect, an incomplete fix, or two files disagreeing on one fact. |
| low | Friction, documentation, a missing capability with a workaround. |

| Class | Meaning |
|---|---|
| C1 | Silent bypass — a gate passes without reading its input |
| C2 | False claim — a document or configuration asserts what is not true |
| C3 | Unimplemented policy — a declared gate with nothing behind it |
| C4 | Contract defect — a schema or template wrong, ambiguous or unsafe |
| C5 | Missing capability |
| C6 | Friction or documentation |

## Entry template

```markdown
### FB-<n> — <one-line summary>

- **Date:** YYYY-MM-DD
- **Framework version:** <tag> @ <submodule SHA>
- **Severity:** critical | high | medium | low
- **Class:** C1 | C2 | C3 | C4 | C5 | C6
- **Status:** open | reported | fixed upstream in <version> | wontfix | superseded by FB-<n>

**What the framework claims** — quote it, with the file and line.

**What actually happens** — the command that was run and its output.

**Reproduction** — the smallest input that shows it.

**Verification** — run, or only read? Running is evidence; reading is a hypothesis.

**Blast radius** — this product only, or every product on the framework?

**Impact on this product** — what it broke, paused or shipped anyway.

**Workaround applied** — none, or the exact files, marked for removal.
```

## Log

<!-- Newest first. -->

### FB-11 — Security gate still passes a SARIF log with no runs, and a leak exit with zero results, as clean scans

- **Date:** 2026-11-22
- **Framework version:** v5.4.9 @ 538d78ddc05b221e730aa9f736283916bc6eb194
- **Status:** reported
- **Issue:** https://github.com/alexxo/ASPICE_agent/issues/13

**Impact on this product** — The temporary FB-7 adapter (ADR-0003) stays: it rejects an empty `runs` list (`tools/security/scan_fail_closed.py:58`) and an exit that disagrees with the result count (`:92`), so neither report is published and the native gate blocks `SCAN_NOT_RUN`. The adapter's 10 regression tests pass on v5.4.9. Its retirement waits for a fix of this entry.

**Workaround applied** — The FB-7 adapter, unchanged, now behind the native `completed_exit_codes` of both rows of `docs/architecture/stack.yaml`; added `tools/security/native_gate_regressions.py`, the removal evidence ADR-0003 asks for. Remove both with the adapter once every case passes without it. A fix upstream could require a nonempty `runs` list, and a result count that agrees with the exit for the scanners whose exit says whether they found something.

**Follow-up (2026-11-22, review of PR #20)** — The crash on a malformed `results` (an object, or a result that is a string) is accepted as fail-closed, not as part of this entry's defect: `agent/run_gates_tool.py` reports a gate that raises as `GATE_CRASHED`, a failed gate, so CI blocks; verified by running `run_gates` on such a copy (`fail`, `GATE_CRASHED`). `tools/security/native_gate_regressions.py` counts a crash or `SCAN_NOT_RUN` as a pass for those two cases and any other crash as a failure: 18 of 20 pass on v5.4.9, and the two that fail are the empty `runs` list and the leak exit with zero results. So a fix of this entry meets the whole removal condition of ADR-0003. The issue filed upstream is not changed.

No findings for v5.4.9 (538d78d) beyond FB-11. Verified on this pin on 2026-11-22: FB-7 fixed in v5.4.4, except the edges of FB-11; FB-8 fixed in v5.4.4, as QUICKSTART step 8 now turns hooks off on every Claude line; FB-9 and FB-10 fixed in v5.4.6, as `check_design_contract_gate` reports `MISSING_SECURITY_TEMPLATES` for `token-request` without its template, and `TEMPLATES_WITHOUT_BOUNDARY` for `external-routing` with one or for the frontend without `runs_in: untrusted`. The changes of v5.4.3, v5.4.5, v5.4.7 and v5.4.8 (gate caching, cost monitoring, test-first and run keys) are not yet exercised by this product at stage 4.

### FB-10 — An external interface between two external actors must name a security template that no gate can require

- **Date:** 2026-11-20
- **Framework version:** v5.4.2 @ 9f9d785b52f0b7be4e66e47dd2cee99c32dcd791
- **Status:** fixed upstream in v5.4.6
- **Issue:** https://github.com/alexxo/ASPICE_agent/issues/9

**Impact on this product** — `external-routing` names `outbound-calls` to satisfy the schema, and a placeholder test double (`stub` named "none: no product code reaches this edge"); the architecture states that no product code runs there and that its security rests on assumptions verified by configuration review. No test was invented.

**Workaround applied** — `docs/architecture/architecture.md`, interface `external-routing`: the `outbound-calls` template and the placeholder double, with prose saying what both do and do not mean. A fix upstream could allow `security_templates` to be empty or absent when neither end is a component.

**Follow-up (2026-11-22, framework bump to v5.4.9 @ 538d78d)** — The schema no longer requires templates on an external interface, and `check_design_contract_gate` reports one naming templates across no trust boundary (`TEMPLATES_WITHOUT_BOUNDARY`), verified by putting `outbound-calls` back on a copy. Workaround removed: `external-routing` names no `security_templates`, and its prose says it crosses no trust boundary of the product. Its `stub` double stays, as every interface declares its implementations.

### FB-9 — A component running in the visitor's browser makes an internal interface a trust boundary the framework cannot express

- **Date:** 2026-11-20
- **Framework version:** v5.4.2 @ 9f9d785b52f0b7be4e66e47dd2cee99c32dcd791
- **Status:** fixed upstream in v5.4.6
- **Issue:** https://github.com/alexxo/ASPICE_agent/issues/10

**Impact on this product** — `token-request` and `lead-request` declare `input-validation`, and the architecture's STRIDE tables cover them; their tests are held by the reviewer, not by a gate.

**Workaround applied** — none. A fix upstream could add a per-component `runs_in: untrusted` (or a trust-boundary mark on the interface) that verify_security_tests_gate treats like `external: true` for the trusted end.

**Follow-up (2026-11-22, framework bump to v5.4.9 @ 538d78d)** — The frontend declares `runs_in: untrusted`, so `token-request` and `lead-request` cross a trust boundary and, from stage 5 on, `verify_security_tests_gate` requires a passing `@security[input-validation]` test at token-issuer and lead-submitter, no longer held by the reviewer alone. Verified on a copy: without the template `check_design_contract_gate` reports `MISSING_SECURITY_TEMPLATES`.

No findings for v5.4.2 (9f9d785) beyond FB-7, FB-8, FB-9 and FB-10. FB-9 and FB-10 were found on this pin on 2026-11-20, while writing the architecture. FB-7 and FB-8 were re-verified open on this pin on 2026-11-19: `gates/sup/scan_security_gate.py` is unchanged since v5.2.0, and the QUICKSTART step 8 Claude lines still load user hooks with `--setting-sources user`. FB-1 and FB-2 were filed as found on v2.1.2, not re-run on this pin.

### FB-8 — Claude session lines of QUICKSTART step 8 run the person's own hooks outside the declared rights

- **Date:** 2026-11-19
- **Framework version:** v5.2.0 @ 79dee183de85cdd0c308d5d4a62311d445f3b748
- **Status:** fixed upstream in v5.4.4
- **Issue:** https://github.com/alexxo/ASPICE_agent/issues/5

**Impact on this product** — The upgrade review of PR #12 stopped and needed a diagnosis; its approval, from the session whose copy changed, stayed valid for `qf/merge` and PR #12 was merged on it (9120f75). The hook touched only `.atl/` in the copy, not the PR's content.

**Workaround applied** — Local, outside the repository: `--settings '{"disableAllHooks":true}'` added to every `QF_COMMAND_TO_START_*` line of the product's `.env` and of `~/.aspice_agent_secrets/.env`. Remove it once the step 8 lines neutralise user hooks upstream. No framework file, gate or pin is changed.

**Follow-up (2026-11-22, framework bump to v5.4.9 @ 538d78d)** — QUICKSTART step 8 now adds `--settings '{"disableAllHooks":true}'` to every Claude line, the same flag as the local workaround, which so stays as the prescribed line rather than a workaround; the watcher also withdraws an approval from a reviewer whose copy changed. The person confirms the flag on every line of both `.env` files; the agent does not read them.

No findings for v5.2.0 (79dee18) beyond FB-7, re-verified open on this pin (its 2026-11-18 follow-up, now in alexxo/ASPICE_agent#6: `gates/sup/scan_security_gate.py` unchanged since v4.0.0 and the 10 `tests/tooling` tests passing), and FB-8 above.

### FB-7 — Security gate accepts operational scanner errors and non-SARIF JSON objects

- **Date:** 2026-11-12
- **Framework version:** v4.0.0 @ 71110564c658ba39fd255e9f5368c0d16ffe7e60
- **Status:** fixed upstream in v5.4.4
- **Issue:** https://github.com/alexxo/ASPICE_agent/issues/6

**Impact on this product** — Native OSV exit1 is not inherently COMMAND_FAILED: report severity decides. The upstream defect remains open. The owner-authorized temporary adapter now protects both declared scanner commands: operational/unsupported status or invalid/incomplete SARIF leaves no published results file and the real gate blocks SCAN_NOT_RUN. Valid original findings still reach its unchanged severity policy. No ||true, fabricated clean SARIF or local result override is used; independent re-review and checkpoint approval remain pending.

**Workaround applied** — TEMPORARY, explicitly authorized by the owner on 2026-11-12; ADR-0003 compares waiting for upstream with this integration. Files: `tools/security/scan_fail_closed.py`, `tools/security/README.md`, `tools/security/vendor/sarif-schema-2.1.0.json`, `tools/security/vendor/README.md`, `tests/tooling/test_scan_fail_closed.py`, `docs/architecture/stack.yaml`, `.github/workflows/quality_gates.yml`, `.gitignore`, `docs/decisions/0003-temporary-fail-closed-scanner-integration.md`, the generated `docs/decisions/index.html`, `docs/architecture/stack-review.md`, and `docs/architecture/evidence/fail-closed-scanner-checks.json`. The adapter clears stale output, checks native status and the full vendored OASIS schema, retains private diagnostics, and publishes only exact validated original bytes. OSV accepts completed 0/1; Gitleaks uses native --exit-code3 (0/3) so partial/error exit1 cannot masquerade as completed findings. No .framework file, contract, gate or pin is modified. Removal: adopt an authorized released upstream correction, verify equivalent positive/negative regressions against it without the adapter, then remove the adapter/schema and temporary CI/tests and restore direct native commands in the same reviewed change. Keep the adapter until that evidence exists; the defect is reported upstream as alexxo/ASPICE_agent#6, with no new release, bot approval or merge claimed.

**Follow-up (2026-11-22, framework bump to v5.4.9 @ 538d78d)** — v5.4.4 checks the exit against each row's `completed_exit_codes` and requires a SARIF 2.1.0 version and runs naming their tool. The 15 regressions of this entry pass against the native gate without the adapter (`tools/security/native_gate_regressions.py`), but an empty `runs` list and a leak exit with zero results still pass as clean: filed separately as FB-11. The adapter stays, now with `completed_exit_codes` on both rows ([0, 3] Gitleaks, [0, 1] OSV), and the 10 `tests/tooling` tests pass on v5.4.9. Its removal waits for FB-11 (ADR-0003).

### FB-6 — Faro Cloud collector has no evidenced selectable public release version

- **Date:** 2026-11-12
- **Framework version:** v4.0.0 @ 71110564c658ba39fd255e9f5368c0d16ffe7e60
- **Severity:** low
- **Class:** C5
- **Status:** wontfix

**What the framework claims** — stack.v2 requires a numeric exact version on a chosen external_services row, with no provider-managed/no-public-version representation.

**What actually happens** — The documented Faro Cloud setup exposes collector configuration and SDK setup, but no independently selectable collector release has been evidenced (https://grafana.com/docs/grafana-cloud/monitor-applications/frontend-observability/instrument/). A collector row without version fails areas/0 (oneOf). SDK2.14.0 is a client version, not a hosted-service release.

**Reproduction** — See docs/architecture/stack-review.md and docs/architecture/evidence/stack-checks.json; run the documented schema fixture from the product root.

**Verification** — Executed missing-version rejection. No-public-selector conclusion is a bounded documentation inspection, not exhaustive proof about provider internals; provider evidence can resolve this row.

**Blast radius** — This Faro Cloud collector declaration; not a claim that every external service lacks a public API/deployment version.

**Impact on this product** — Keep the Faro SDK pinned and the collector row unresolved. Apps Script/Sheets is instead the versioned webhook integration: the owner selected script version 1 for its first Web App deployment. This numeric version is representable, not a reported defect; the remote deployment is not verified here.

**Workaround applied** — None. No framework, schema, gate, pin or result is patched. The draft remains honestly incomplete; no fabricated version, omitted used service or false approval.

**Follow-up (2026-11-12, ADR-0002)** — A broader source search found the official grafana/faro OpenAPI spec/gen/faro.gen.yaml: info.title Faro API, info.version 1.0.0, POST /collect/{appKey}. The earlier search was bounded to the hosted collector release and missed this API-contract layer. The owner selects v1 for the payload/API contract major, not the hosted server, SDK2.14.0 or OpenAPI format3.0.0. This resolves this product row; no claim about remotely verified Cloud implementation. Source: https://raw.githubusercontent.com/grafana/faro/main/spec/gen/faro.gen.yaml . Status wontfix corrects the selected layer, not an upstream change.


### FB-5 — Gemini Live API v1beta spelling is rejected although API v1 is accepted

- **Date:** 2026-11-12
- **Framework version:** v4.0.0 @ 71110564c658ba39fd255e9f5368c0d16ffe7e60
- **Severity:** medium
- **Class:** C4
- **Status:** wontfix

**What the framework claims** — stack.v2 permits numeric public versions with optional v prefix, but no undelimited alphabetic suffix after the number.

**What actually happens** — Current official ephemeral-token and Live examples use apiVersion v1beta (https://ai.google.dev/gemini-api/docs/ephemeral-tokens). The exact API row v1beta fails areas/0 (oneOf); controls v1 and an illustrative numeric deployment version pass. This is about the API version, NOT the model ID in the tool field.

**Reproduction** — See docs/architecture/stack-review.md and docs/architecture/evidence/stack-checks.json; run the documented schema fixture from the product root.

**Verification** — Executed schema controls and the v1beta rejection; read current official API examples. No real Gemini call or SDK runtime test.

**Blast radius** — Tools whose honest API version is v1beta (and analogous spellings), not all SaaS and not Loki API v1.

**Impact on this product** — Only the Gemini Live API row is unresolved. Model tool gemini-3.8-live with public version 3.8 and SDK3.2.0 are separate declarations. Do not rewrite v1beta as v1-beta/v1 or invent an immutable model snapshot.

**Workaround applied** — None. No framework, schema, gate, pin or result is patched. The draft remains honestly incomplete; no fabricated version, omitted used service or false approval.

**Follow-up (2026-11-12, ADR-0002)** — The owner authorizes stack label v1-beta with an explicit mapping to provider wire apiVersion v1beta (ADR-0002). The real API value and endpoints are NOT changed. v1-beta passes stack.v2 but is NOT complete strict SemVer (1.0.0-beta would have a complete numeric core), nor an official Google alias. The previous literal rejection remains historical evidence. Status wontfix records this declared normalization, not an upstream fix or a stable-v1 upgrade.


### FB-4 — Managed Vercel Node patch cannot be selected as an exact runtime version

- **Date:** 2026-11-12
- **Framework version:** v4.0.0 @ 71110564c658ba39fd255e9f5368c0d16ffe7e60
- **Severity:** medium
- **Class:** C4
- **Status:** wontfix

**What the framework claims** — `choose_stack_skill` R1 and stack.v2 require every non-given tool to carry an exact version; the version pattern does not accept 24.x.

**What actually happens** — The provider exposes Node 24.x and rolls minor/patch updates itself (https://vercel.com/docs/functions/runtimes/node-js/node-js-versions). Local/CI 24.22.3 is pin-able; it is not evidence that Vercel runs that patch. The isolated runtime row version 24.x fails schema at areas/0 (oneOf).

**Reproduction** — See docs/architecture/stack-review.md and docs/architecture/evidence/stack-checks.json; run the documented schema fixture from the product root.

**Verification** — Executed the local schema check; read provider documentation. No deployment or remote process.version measurement performed.

**Blast radius** — Products declaring a provider-managed Node runtime under this contract; observed schema behavior on this pin only.

**Impact on this product** — Only the Vercel managed runtime row is unresolved. The local/CI Node row stays 24.22.3. A numeric API version such as Loki v1 is NOT affected.

**Workaround applied** — None. No framework, schema, gate, pin or result is patched. The draft remains honestly incomplete; no fabricated version, omitted used service or false approval.

**Follow-up (2026-11-12, ADR-0002)** — The owner selects version 24 as the provider-major contract (ADR-0002). Exact local/CI Node remains 24.22.3; no remote patch is claimed frozen. The historical 24.x rejection is still reproducible, but no schema patch is required for this selected granularity. Status wontfix means an explicit product interpretation, not fixed upstream.


### FB-3 — Aclarar retornos separados frente a doble punta en una conexión

- **Date:** 2026-11-03
- **Framework version:** v4.0.0 @ 71110564c658ba39fd255e9f5368c0d16ffe7e60
- **Severity:** medium
- **Class:** C6
- **Status:** wontfix

**What the framework claims** — La etapa diagram delega dibujo en el plugin instalado y exige conservar formato, trazabilidad e imágenes renderizadas por él; no promete soporte de cualquier notación.

**What actually happens** — El cliente solicita una sola conexión con dos puntas por par de componentes; Archify 2.16 no expone bidireccionalidad en su esquema architecture y su renderer emite únicamente marker-end. Los retornos SÍ pueden dibujarse como conexiones separadas en sentido inverso, como se hizo en la versión anterior. La limitación inspeccionada se refiere únicamente a dos puntas en una misma conexión; no a representar retornos o intercambios bidireccionales.

**Reproduction** — Leer `/home/tavobecerril/.agents/skills/archify/schemas/architecture.schema.json`, propiedad connections: additionalProperties=false y ninguna propiedad de dirección doble; ejecutar `rg -n 'bidirect|marker-start|marker-end' /home/tavobecerril/.agents/skills/archify/renderers/architecture/render-architecture.mjs`: el path de conexión de la línea 968 usa sólo marker-end.

**Verification** — Inspección de esquema y renderer ejecutada; no se ha probado otra versión ni se afirma que una actualización lo resuelva. No es un fallo demostrado del gate, sino limitación verificada de capacidad del plugin integrado.

**Blast radius** — Diagramas architecture solicitados con relación bidireccional en el plugin instalado; no se ha verificado otro producto.

**Impact on this product** — El agente describió la limitación demasiado ampliamente y elevó innecesariamente la cuestión a un bloqueo. No existe un bloqueo actual: la convención nativa aceptada por el cliente representa una conexión desde el iniciador con petición/retorno en la etiqueta, y ya está implementada y validada.

**Workaround applied** — Ningún parche: no se cambió framework, plugin, pin ni HTML a mano. Se usa la convención nativa solicitada por el cliente en docs/diagrams/tbo-capture.architecture.json: una conexión por relación, etiquetas de intercambio, composition-root en card y grid de cinco columnas. Estado wontfix porque no se solicita cambiar el plugin para la notación de doble punta; esto no declara un fallo del framework ni un arreglo upstream.

**Follow-up (2026-11-03)** — El cliente mantiene Archify 2.16 y retira la exigencia de doble punta SVG: acepta una conexión desde el iniciador con retorno/intercambio en la etiqueta, composition-root en cards y grid de cinco columnas. Convención soportada nativamente, sin modificar plugin, framework ni HTML. La limitación original sigue documentada pero ya no bloquea este producto; no se afirma soporte nuevo del plugin.

Migration verification on 2026-11-01 — v4.0.0
(71110564c658ba39fd255e9f5368c0d16ffe7e60). No additional findings were
observed in that bounded configuration-migration run. This is historical
execution evidence, not a release-wide no-findings claim; FB-3 above records
the later diagram-plugin limitation.

Scope: replaced `review.sample_every` with the confirmed `review.people`,
added `review.architect` and `customer`, and copied both GitHub workflow
templates from the pinned v4.0.0 release. No existing checkpoint approvals,
diagrams, requirements or product code needed conversion. Historical findings
FB-1 and FB-2 below are preserved; this line does not close them.

Verification run with `/usr/bin/python3 -B`: `read_config_tool.py --root .`
returned `ok: true` with no problems, and `resolve_stage_tool.py --root .
--check` exited 0 with no failing findings. Stage 1 remains in progress with
`NO_DIAGRAMS` and `NO_WISHES`; no product stage was completed or approved.
Host-backed integrity and delivery-review checks were not run (`no_host`),
and later-stage gates were not run (`stage_not_reached`). These checks were
run before committing the migration; no push or GitHub Actions execution was
performed. Checks that read the committed range must be repeated after the
authorized commit and in CI.


### FB-2 — Bootstrap omits the release accounting required by its feedback gate

- **Date:** 2026-10-21
- **Framework version:** v2.1.2 @ 5afd2d7da26304ddc0b5b062316435c46624920a
- **Status:** reported
- **Issue:** https://github.com/alexxo/ASPICE_agent/issues/7

**Impact on this product** — Blocks the initial configuration PR until the
introduced release is accounted for in the product's feedback log. Tracked
with FB-1 in https://github.com/Trazodigital/TBO-STUDIO/issues/2.

**Workaround applied** — Recorded the actual v2.1.2 bootstrap findings in
`FRAMEWORK_FEEDBACK.md`; no false no-findings statement, framework patch or
gate exemption. Retain this evidence while the bootstrap documentation gap
remains open upstream.

### FB-1 — Prescribed bootstrap commit message lacks required issue traceability

- **Date:** 2026-10-21
- **Framework version:** v2.1.2 @ 5afd2d7da26304ddc0b5b062316435c46624920a
- **Status:** reported
- **Issue:** https://github.com/alexxo/ASPICE_agent/issues/8

**Impact on this product** — Blocks PR #1. Adding a later compliant commit
alone cannot repair the original message because the gate checks each commit.
The real setup issue is https://github.com/Trazodigital/TBO-STUDIO/issues/2.

**Workaround applied** — With the developer's explicit approval, replace only
the `setup/aspice-framework` branch's setup commit with a message containing
`(#2)` and this feedback record. No change to `main`, framework files or CI
rules. Publication requires a user-run, feature-branch-only force-with-lease;
the corrected commit must receive fresh reviews. Retain this record until
the bootstrap guidance is corrected upstream.

