# Stack proposal — evidence and unresolved inputs

Status: **proposal with schema-representable version labels; checkpoint 3 approval still required** (2026-11-12). Read the machine-readable
[stack](stack.yaml), [decision](../decisions/0001-personal-framework-test-stack.md),
[version-granularity decision](../decisions/0002-provider-contract-version-granularity.md),
and [framework feedback](../../FRAMEWORK_FEEDBACK.md). No product code, packages,
provider settings, deployment or Git commit were created by this proposal.

## Scope and classification

- Personal, non-commercial framework experiment; no production launch. Budget:
  0 MXN/month, free plans only, low volume not yet estimated. A quota ceiling is
  not a guarantee of availability. No automatic upgrade, paid fallback or paid
  grounding is authorized.
- Use synthetic contact/project data in Gemini tests. Do not send real personal,
  confidential or sensitive information to unpaid Gemini services.
- `data_stores` is not needed under REQ-0028. The external receiving integration
  is **Apps Script lead webhook / Google Sheets destination**, in
  `external_services`. Its version means the immutable **script version number**
  assigned to the deployed receiver, not its long deployment ID or the hosted
  Sheets implementation. The owner selected **script version 1** for the first
  Web App deployment. This is a supplied version selection, not evidence of a
  remotely verified deployment; no deployment was created or inspected here.
- Do not assume the script uses Sheets REST API v4: `SpreadsheetApp`, an advanced
  Sheets service and direct REST are distinct choices. The product calls the
  external webhook, not Sheets directly. If its contract later changes, update
  this inventory explicitly. No provider-owned internal dependency is claimed
  to have been frozen by pinning a webhook or an API boundary.
- The framework's GitHub/Actions/Issues and configured requirements/diagram tools
  are retained. No additional database, LLM framework or HTTP server framework
  is proposed.

## Compatibility evidence, not an installation report

The prototype lockfile was read at
`/home/tavobecerril/Leadwebsite/package-lock.json`. Published npm metadata was
consulted read-only on 2026-11-12; selected direct package versions appear in
`stack.yaml`. A product lockfile and installed compatibility checks are still
pending permission and the appropriate stage; transitive resolution is not yet
frozen in this repository.

| Check | Evidence | Limit |
|---|---|---|
| plugin-react 4.7.0 + Vite 7.3.8 | Release tag declares `^4.2.0 \|\| ^5.0.0 \|\| ^6.0.0 \|\| ^7.0.0`; `semver.satisfies('7.3.8', range)` returned true | Declared compatibility, not a migrated build/HMR test |
| Vite 7.3.8 + Vitest 5.1.0 + Node 24.22.3 | Published engines/peers accept these versions; Vite 7.3 is a supported branch | Packages not installed together here |
| React/DOM 18.3.1 + thinking-orbs 0.3.1 | Peer React >=18; existing installed modules rendered solving/listening through ReactDOM server successfully | Not a browser/animation or microphone test |
| mp4box 0.5.4 | No React peer; existing module imported and exposed createFile, appendBuffer, flush, setExtractionOptions, start, stop, getTrackById and DataStream | No actual media decode; prototype has manual `src/mp4box.d.ts`; do not jump to 2.x |
| Tailwind 3.4.19 | Official npm `v3-lts` tag points to 3.4.19; keep it with PostCSS and Autoprefixer | Do not infer an unlimited future maintenance commitment |
| TypeScript 5.9.3 | Selected typescript-eslint 8.72.2 declares TS >=4.8.4 <6.1.0 | Do not select latest TypeScript 7 automatically |

Primary sources: [plugin release package.json](https://raw.githubusercontent.com/vitejs/vite-plugin-react/plugin-react@4.7.0/packages/plugin-react/package.json),
[Vite maintenance](https://vite.dev/releases), [Vitest metadata](https://registry.npmjs.org/vitest/5.1.0),
[Tailwind tags](https://registry.npmjs.org/-/package/tailwindcss/dist-tags),
[typescript-eslint metadata](https://registry.npmjs.org/typescript-eslint/8.72.2),
[Node release](https://nodejs.org/en/blog/release/v24.22.3).

## Version granularity and provider wire values

`stack.v2` accepts `v1` and a numeric script version. A direct schema check
accepted both controls, and accepted model tool `gemini-3.8-live` with its public
version `3.8`. Therefore none of those is reported as an unrepresentable row.
The model code is exact but is not represented as an immutable weights snapshot.
The owner subsequently selected the provider/API granularity in ADR-0002;
passing this schema is not strict SemVer validation or provider verification.

| Row | Stack declaration | Exact scope / wire value | Tracking |
|---|---|---|---|
| Node local/CI | 24.22.3 | Exact toolchain reference, not yet installed here (machine was 24.17.0) | No feedback |
| Vercel managed Node runtime | 24 | Provider-major selection only; Vercel owns minor/patch, remote process.version not frozen | ADR-0002; FB-4 follow-up |
| Gemini Live API | v1-beta | Owner-approved stack-only label; SDK apiVersion and HTTP/WSS API spelling remain **v1beta** | ADR-0002; FB-5 follow-up |
| Apps Script / Sheets receiver | Script version 1 | Selected by owner for the first Web App deployment; accepted by schema, not remotely verified | No feedback |
| Loki ingestion boundary | API v1 | Actual endpoint `/loki/api/v1/push`; schema accepts v1 | No feedback |
| Faro Cloud collector | v1 | Major of the public Faro API/payload contract, OpenAPI info.version **1.0.0**, not its internal Cloud build | ADR-0002; FB-6 follow-up |

The public Faro specification was found in a broader search after the original
collector-release inspection: [Faro API specification](https://raw.githubusercontent.com/grafana/faro/main/spec/gen/faro.gen.yaml)
declares `info.version: 1.0.0` and POST `/collect/{appKey}`. The requested `v1`
is its **contract major**. It is not the OpenAPI format version `3.0.0`, SDK
version `2.14.0`, or an immutable Grafana Cloud server build. This corrects
the earlier layer selection; FB-6 retains that inspection as history.

`24`, `v1-beta` and `v1` are accepted stack.v2 labels, not complete strict
SemVer strings: full SemVer requires a major.minor.patch numeric core. Local
SemVer checks returned null for these short labels and 1.0.0-beta for that
complete example. No unsupported provider equivalence is implied. The Gemini
label is a **local documented normalization**, not a Google alias: configuration
and endpoint paths must still use **v1beta**.

Do not substitute CLI versions, invent managed patches, use the normalized
Gemini label on the wire, or mark used services unnecessary. Public contract
versions do not freeze provider internals. FB-4/5/6 follow-ups record the
owner-approved version-grain resolution without modifying framework code.

Sources: [Vercel Node selection](https://vercel.com/docs/functions/runtimes/node-js/node-js-versions),
[Gemini tokens/Live v1beta](https://ai.google.dev/gemini-api/docs/ephemeral-tokens),
[Apps Script deployments versus versions](https://developers.google.com/apps-script/concepts/deployments),
[Loki HTTP API](https://grafana.com/docs/loki/latest/reference/loki-http-api/),
[Faro setup](https://grafana.com/docs/grafana-cloud/monitor-applications/frontend-observability/instrument/).

The candidate model is `gemini-3.8-live`, published with a free tier in
[Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing#gemini-3.8-live).
No request has established account/region availability or usable quota.
`@google/genai` 3.2.0 is separately pinned. Enforce one token request and one
connection attempt per authorized activation: verify the SDK's effective retry
configuration, do not silently use its defaults, and do not enable reconnection
merely because an SDK supports it.

## Commands and artifact boundaries

All executable npm tools use local binaries and fixed direct versions; no
`npx ...@latest` is proposed. `run` and `version_command` are concrete in the
stack for the tools that run. Libraries expose installed version evidence via
`npm ls --depth=0 <package>`; they do not have invented standalone functional
commands. The provider APIs/model are not shell executables.

- Static analysis: **`./node_modules/.bin/tsc -b`**, version command
  `./node_modules/.bin/tsc --version`. The later solution tsconfig must cover
  browser, server, tests and adapters; generated outputs/cache must be ignored.
  Do not claim a passing type check before these inputs exist.
- Browser build: `./node_modules/.bin/vite build` to `dist`, after type checks.
  Full Functions/static packaging: `./node_modules/.bin/vercel build` to
  `.vercel/output`; neither command has been run on this future product.
- Deployment: `./node_modules/.bin/vercel deploy --prebuilt`, **Preview only**, by
  separate authorization. No `--prod`, account changes, automatic deploy or
  production migration. No deployment command was executed.
- Gitleaks writes `reports/secrets.sarif`; OSV writes
  `reports/dependencies.sarif`. Their commands preserve native status and never
  use `|| true`, fabricate clean reports or reuse an earlier tree's report.
- Test-suite commands and JUnit/Cobertura/measurement settings belong in the
  verification plan at their appropriate later stages; test code is not
  implemented by this stack proposal.

Sources: [Vercel build](https://vercel.com/docs/cli/build),
[Preview deployment](https://vercel.com/docs/cli/deploy),
[OSV source scanning](https://google.github.io/osv-scanner/usage/scan-source),
[OSV SARIF and exit codes](https://google.github.io/osv-scanner/output/).

## OSV exit code versus framework interpretation

Official OSV documentation distinguishes 0 (packages, no findings), 1
(findings), 127 (general error), and 128 (no packages); 1–126 are reserved for
result-related errors and 129–255 for non-result errors. Do not describe 2 as
OSV's general-error code.

The framework's `scan_security_gate` validates the scanner version, then judges
the report rather than `run.exit_code`. High/critical (score >=7.0) and unscored
results block. A medium 6.9 finding can pass even when the scanner exits 1.
Missing or unreadable JSON produces `SCAN_NOT_RUN`. `run_command` removes old
matching reports before each fresh command, so the fixture below is not a
stale-file demonstration.

An isolated execution of the **real gate**, with fresh synthetic scanner
processes (not a patched gate, not real OSV), produced:

| Fixture | Gate |
|---|---|
| exit 0, clean SARIF 2.1.0 | pass |
| exit 1, SARIF score 6.9 | pass |
| exit 1, SARIF score 7.0 | SECURITY_FINDING |
| exit 1, unscored SARIF result | SECURITY_FINDING |
| exit 127, freshly generated clean SARIF | pass — operational-error gap |
| exit 128, freshly generated clean SARIF | pass — no-packages gap |
| exit 127, freshly generated JSON `{}` | pass — `_read` only requires a dictionary |
| exit 127, missing report or invalid JSON | SCAN_NOT_RUN |

This is FB-7, distinct from version grammar. No real OSV binary was installed
or run; it is not a vulnerability scan of this product. The stack preserves
OSV's raw status/report, but that alone does not fix the gate. Do not claim the
security assurance complete until the upstream behavior or an explicitly
approved fail-closed integration is resolved. No workaround is applied here.

Reproduce the version grammar without installation:

```sh
/usr/bin/python3 -B - <<'PY'
import sys
sys.path.insert(0, '.framework')
from tools.validate_contract_tool import validate
base = dict(contract='stack.v2', code_files=['**/*.ts'], env_read_patterns=[],
            decision_record='docs/decisions/0001-personal-framework-test-stack.md')
for version in ['v1', '17', 'v1beta', '24.x']:
    row = dict(area='external_services', tool='schema-fixture', version=version)
    print(version, not validate(dict(base, areas=[row]), 'stack'))
PY
```

`17` is an illustrative valid number, **not** the selected Apps Script version
`1`. The selected row also passes the current full-schema inspection.
The full synthetic scanner experiment is reproduced from the script in
`evidence/security-gate-reproduction.md`; its observed results are recorded as
documentation in `evidence/stack-checks.json`, not as a product test suite.

## Planned CI doubles and provider checks

- Gemini: fake token endpoint and scripted Live connection; count attempts and
  exercise rejection, malformed responses, disconnect and late events.
- Apps Script/Sheets: fake receiver for acceptance, rejection, timeout and
  ambiguous/tardy responses; no real sheet writes in ordinary CI.
- Loki: fake sink that accepts, rejects, throws or never settles; prove that
  logs contain no protected data and do not change the functional outcome.
- Faro likewise has a controlled sink. Provider business calls are denied in
  ordinary tests; dependency installation/security advisory lookups are distinct
  CI network uses, not Gemini/Sheets/Loki business calls.
- Real free-tier smoke checks require explicit authorization, synthetic data,
  bounded attempts and account-specific quota checks. Passing doubles do not
  prove real provider delivery or quota availability.

These are stack-level verification intentions, not constructed component
contracts. Components/interfaces and actual tests follow the approved stack;
no checkpoint or later-stage completion is claimed.

## Current local validation

The latest results and official generated table are refreshed after each change:

- [Official stack table](stack-table.md), generated only by
  `write_stack_table_tool.py`; not hand-authored. A rendered row marked chosen
  does not mean checkpoint approval.
- [Current schema diagnostics](evidence/draft-validation.json).
- [Version-label evidence](evidence/version-normalization.json).

Historical `stack-checks.json` retains the rejected literal 24.x/v1beta and
missing-version fixtures; those are not the current proposed rows. The
scanner assurance finding FB-7 remains open. No installation, migrated build,
real provider verification, component/test implementation, commit, push or
deployment is claimed. Host checks still require their configured access.

Latest local result (2026-11-12): `check_stack_decision_gate`,
`verify_decision_records_gate`, and `check_framework_feedback_gate` **pass**;
full schema diagnostics are empty. The official stack table was generated
successfully. The resolver's checkpoint status is reported below; local pass
is not approval, integration verification, or evidence that a remote service
runs a selected patch.

Resolver: stage `architecture`, status `awaiting_checkpoint`.
