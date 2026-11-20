# Architecture — TBO capture

Stage 3 draft (SWE.2). Derived from the approved architecture diagram
[tbo-capture](../diagrams/tbo-capture.architecture.html) and the approved
requirements; built on the stack approved at checkpoint 3
([stack](stack.yaml)). One component per node, one interface per edge.

## External actors

Actors and systems outside the product. They carry no budget, size, modes,
concurrency or composition root, and meet no requirement: the product does not
control them, it only depends on them through the interfaces below.

```yaml component
id: visitor
derived_from: tbo-capture#visitor
role: external
name: Visitor
responsibility: Starts a project inquiry, provides contact and project data by form or voice, and decides when to confirm the request.
```

```yaml component
id: gemini-live
derived_from: tbo-capture#gemini-live
role: external
name: Gemini Live
responsibility: Hosts the real-time voice conversation and calls the field-filling tool exposed by the frontend.
```

```yaml component
id: lead-webhook
derived_from: tbo-capture#lead-webhook
role: external
name: Lead webhook
responsibility: Receives the validated lead over HTTPS and forwards it to the commercial destination.
```

```yaml component
id: commercial-destination
derived_from: tbo-capture#commercial-destination
role: external
name: Commercial destination
responsibility: Stores the delivered lead where the commercial team reviews it.
```

```yaml component
id: grafana-faro
derived_from: tbo-capture#grafana-faro
role: external
name: Grafana Faro
responsibility: Collects browser telemetry events sent by the frontend.
```

```yaml component
id: grafana-loki
derived_from: tbo-capture#grafana-loki
role: external
name: Grafana Loki
responsibility: Stores the structured logs emitted by the backend functions.
```

## Product components

Composition roots are written as dotted module paths, as the code-to-design
gate reads them: `src.api.voice-token` is `src/api/voice-token.ts`,
`src.api.lead` is `src/api/lead.ts` and `src.main` is `src/main.tsx`, all
inside `code_dir`. Vercel requires function entries under `api/`, so
`api/voice-token.ts` and `api/lead.ts` hold only a one-line re-export of the
handler built in `src/api/`, with no logic of their own.

REQ-0133 is met by frontend, token-issuer and lead-submitter on purpose: its obligations are disjoint (frontend sends to Faro, both backends to Loki, none replaces the commercial destination), so sharing it is not an overlap of responsibilities.

### token-issuer

A stateless Vercel Function. Its budget counts provider quota it can control
(one session per credential, one upstream call per issuance), not latency: no
requirement sets a threshold for it, and REQ-0086 forbids assuming provider
quotas or expirations. The per-activation limit belongs to the frontend, which
is the only component that sees voice activations.

No degraded mode: Loki and Gemini failures are handled per request (fail-open
logging, an error response) and never change the state of the instance. A
missing Gemini API key is `unconfigured`: fail-closed, every request gets an
error answer without a credential, and Gemini is never called.

Its wait for the upstream token request has no requirement threshold; the
value is an open item of detailed design (see *Open items*), so the "bounded
wait" of the threat table is a promise the detailed design must number.

```yaml component
id: token-issuer
derived_from: tbo-capture#token-issuer
role: component
name: Token issuer
responsibility: Issues a single-use Gemini Live credential to the browser while keeping the permanent API key on the server.
budget:
  - {resource: Gemini Live sessions authorized per issued credential, value: 1, unit: session}
  - {resource: upstream Gemini token requests per issuance without silent SDK retries, value: 1, unit: call}
size: S
meets: [REQ-0086, REQ-0087, REQ-0124, REQ-0133, REQ-0150, REQ-0157, REQ-0161, REQ-0181, REQ-0193, REQ-0198, REQ-0199, REQ-0201]
decisions: [ADR-0001, ADR-0002, ADR-0004]
modes:
  - {mode: cold-start, to: [ready, unconfigured]}
  - {mode: ready, to: []}
  - {mode: unconfigured, to: []}
concurrency: Invocations are stateless and may share one function instance, so only read-only configuration and the provider client live at module scope, and log delivery runs after the response via waitUntil.
composition_root: src.api.voice-token
```

### lead-submitter

A stateless Vercel Function. The 8 s upstream wait (ADR-0006) is an allocation of its own
inside the 10 s ceiling of REQ-0079 (envio INV-13 leaves the operating value to
design), keeping about 2 s of margin before the browser gives up at 10 s
(REQ-0144). The margin is an assumption to measure once code exists, since cold
start is not under the product's control, and it reduces duplicated leads
without preventing them: envio INV-2 and INV-7 promise no deduplication.

No degraded mode: Loki and webhook failures are handled per request (fail-open
logging, an error response) and never change the state of the instance. A
missing webhook URL is `unconfigured`: fail-closed, the webhook is never called.

```yaml component
id: lead-submitter
derived_from: tbo-capture#lead-submitter
role: component
name: Lead submitter
responsibility: Validates the submitted brief on the server and delivers it once to the configured lead webhook, answering 202 only after the integration confirms receipt.
budget:
  - {resource: upstream lead webhook wait per call including redirects, value: 8, unit: s}
  - {resource: lead webhook invocations per submission request without automatic retries, value: 1, unit: call}
size: M
meets: [REQ-0069, REQ-0071, REQ-0074, REQ-0076, REQ-0078, REQ-0079, REQ-0080, REQ-0127, REQ-0133, REQ-0145, REQ-0146, REQ-0147, REQ-0163, REQ-0164, REQ-0178, REQ-0195, REQ-0196, REQ-0200, REQ-0204]
decisions: [ADR-0001, ADR-0002, ADR-0004, ADR-0005, ADR-0006, ADR-0007]
modes:
  - {mode: cold-start, to: [ready, unconfigured]}
  - {mode: ready, to: []}
  - {mode: unconfigured, to: []}
concurrency: Submissions are stateless and independent, with no shared deduplication state, so concurrent or retried submissions may both reach the webhook, and log delivery runs after the response via waitUntil.
composition_root: src.api.lead
```

### frontend

The browser application. Its budget holds the limits only it can see: one
credential request and one WSS attempt per explicit voice activation (REQ-0083,
REQ-0088, REQ-0118) and the 10 s wait per submission attempt (REQ-0144). No
bundle-size or load-time budget: no requirement sets one.

Its modes are the phases of the glossary (capture, review, pending submission),
with voice as a path inside capture. Entering review while voice is starting
goes straight from `voice-starting` to `review`, aborting the start and
releasing every partially acquired resource before the brief is shown
(REQ-0207, REQ-0142); a failed start returns to `capture` with the data kept.
How long `voice-starting` may wait for the credential and the WSS handshake
before it fails back to `capture` is an open item of detailed design (see
*Open items*).

REQ-0086 is shared with token-issuer, with disjoint obligations: the server
does not fix the credential window, the browser does not blame a 429 on a
session count.

```yaml component
id: frontend
derived_from: tbo-capture#frontend
role: component
name: Frontend
responsibility: Guides the visitor through capture by form or voice, review of the brief and submission, holding the brief in local memory without commercial storage and sending the commercial request to the backend only after the visitor's explicit confirmation.
budget:
  - {resource: token issuance requests per explicit voice activation, value: 1, unit: request}
  - {resource: Gemini Live WSS connection attempts per explicit voice activation, value: 1, unit: attempt}
  - {resource: client wait per submission attempt, value: 10, unit: s}
size: XL
meets: [REQ-0030, REQ-0031, REQ-0032, REQ-0033, REQ-0034, REQ-0035, REQ-0036, REQ-0037, REQ-0038, REQ-0039, REQ-0040, REQ-0041, REQ-0042, REQ-0043, REQ-0044, REQ-0045, REQ-0046, REQ-0047, REQ-0048, REQ-0049, REQ-0050, REQ-0051, REQ-0052, REQ-0053, REQ-0054, REQ-0055, REQ-0056, REQ-0057, REQ-0058, REQ-0059, REQ-0060, REQ-0061, REQ-0062, REQ-0063, REQ-0064, REQ-0065, REQ-0066, REQ-0067, REQ-0068, REQ-0070, REQ-0072, REQ-0073, REQ-0075, REQ-0077, REQ-0081, REQ-0082, REQ-0083, REQ-0084, REQ-0085, REQ-0086, REQ-0088, REQ-0089, REQ-0090, REQ-0091, REQ-0092, REQ-0093, REQ-0094, REQ-0095, REQ-0096, REQ-0097, REQ-0098, REQ-0099, REQ-0100, REQ-0101, REQ-0102, REQ-0103, REQ-0104, REQ-0105, REQ-0106, REQ-0107, REQ-0108, REQ-0109, REQ-0110, REQ-0111, REQ-0112, REQ-0113, REQ-0114, REQ-0115, REQ-0116, REQ-0117, REQ-0118, REQ-0119, REQ-0120, REQ-0121, REQ-0122, REQ-0123, REQ-0125, REQ-0126, REQ-0128, REQ-0129, REQ-0130, REQ-0131, REQ-0132, REQ-0133, REQ-0134, REQ-0135, REQ-0136, REQ-0137, REQ-0138, REQ-0139, REQ-0140, REQ-0141, REQ-0142, REQ-0143, REQ-0144, REQ-0148, REQ-0149, REQ-0151, REQ-0152, REQ-0153, REQ-0154, REQ-0155, REQ-0156, REQ-0158, REQ-0159, REQ-0160, REQ-0162, REQ-0165, REQ-0166, REQ-0167, REQ-0168, REQ-0169, REQ-0170, REQ-0171, REQ-0172, REQ-0173, REQ-0174, REQ-0175, REQ-0176, REQ-0177, REQ-0179, REQ-0180, REQ-0182, REQ-0183, REQ-0184, REQ-0185, REQ-0186, REQ-0187, REQ-0188, REQ-0189, REQ-0190, REQ-0191, REQ-0192, REQ-0194, REQ-0197, REQ-0202, REQ-0203, REQ-0205, REQ-0206, REQ-0207]
decisions: [ADR-0001, ADR-0002]
modes:
  - {mode: capture, to: [voice-starting, review]}
  - {mode: voice-starting, to: [voice-active, capture, review]}
  - {mode: voice-active, to: [capture, review]}
  - {mode: review, to: [capture, submitting]}
  - {mode: submitting, to: [accepted, review]}
  - {mode: accepted, to: []}
concurrency: One browser event loop interleaves visitor input, voice tool calls, the submission request and telemetry, coordinated by the voice start lock, the pending-submission lock, explicit confirmation of voice proposals that conflict with manual edits, discarding voice events that arrive after the channel closed, and discarding late responses of superseded submission attempts.
composition_root: src.main
```

## Interfaces

One per edge of the diagram. Versions follow the approved stack and ADR-0002:
the Gemini stack label v1-beta is sent on the wire as v1beta.

**Browser-facing internal interfaces.** `token-request` and `lead-request` are
internal (both ends are product components), yet their `from` end runs in the
visitor's browser, which the product does not control: the diagram's trust
boundary wraps only the backend. Both declare `input-validation` although
verify_security_tests_gate checks external interfaces only; the reviewer holds
them to it (create_security_tests_skill, *Not checkable*).

**Gemini (token-source, voice-channel).** token-issuer locks every credential
with `liveConnectConstraints` (model gemini-3.8-live, response modalities, the
base system instruction and the llenar_campo declaration), so a leaked
credential cannot open a session with another model or prompt. The browser
sends only audio and the captured values as conversation context (REQ-0119),
never a system instruction of its own. Open, to verify in detailed design:

- the official API documents `POST /v1beta/auth_tokens` and v1beta for
  ephemeral-token sessions, while the @google/genai typedoc of `tokens.create`
  says v1alpha only; check empirically with 3.2.0, and if v1alpha is required,
  record a decision that supersedes ADR-0002.

The API documents a reconnection every 10 minutes through `sessionResumption`.
The product does not use it: when Gemini closes the channel at its duration
limit (GoAway), INV-6 of voz-inicio holds, there is no automatic reconnection,
the frontend returns to `capture` with the data kept (REQ-0112), and the
visitor may reactivate voice by hand with a new credential and the kept
context (REQ-0157, REQ-0158).

**Apps Script (validated-delivery).** Three platform limits shape the adapter
of lead-submitter:

- `doPost(e)` cannot read HTTP headers, so a shared secret, if one is added to
  the URL, travels in the JSON body and falls under `stored-data`;
- a Web App answers HTTP 200 even for application errors, and may return HTML
  on permission errors or exceptions, so the adapter (ADR-0005) rejects a 2xx carrying
  `text/html` and a 2xx carrying a JSON application error, and accepts a 2xx
  with an empty body or a JSON success, as REQ-0074, REQ-0146 and REQ-0164
  require ("HTTP 2xx, even without a body"). Operating assumption: the receiver
  always answers a JSON success or error. Refusing an empty 2xx would need a
  change request to those requirements;
- the answer comes through a 302 to `script.googleusercontent.com`, so the
  call follows redirects and the 8 s budget covers the whole chain.

**Loki (token-logs, lead-logs).** The Grafana Cloud Basic Auth credential is a
secret under `stored-data`. `correlation_id` travels in the JSON log line,
never as a stream label (unbounded label values multiply Loki streams).
`waitUntil` shares the function's timeout and is cancelled with it, so each
function's `maxDuration` must leave room for its own work (8 s upstream for
lead-submitter) plus a bounded push to Loki, measured with `getDeadline()`.

**Faro (browser-events).** Zero PII (REQ-0179, REQ-0182, REQ-0189 and the
other flow-level event rules) needs an allowlist of events enforced in a
`beforeSend` hook that drops anything else; no automatic instrumentation sends
unfiltered. Restricting the collector's allowed origins in Grafana Cloud is
still to verify in detailed design.

**lead-webhook stays external.** The Apps Script receiver lives outside this
repository. The product is not receiver-agnostic: lead-submitter neutralizes
spreadsheet formulas before delivery (ADR-0007), and `validated-delivery`
declares it in its data, so another receiver needs a superseding record.

**external-routing (lead-webhook → commercial-destination).** No product code
runs on this edge: both ends are external, so verify_security_tests_gate finds
no product end to test. It names `outbound-calls` because the schema requires
a template on every external interface; its security rests on assumptions
verified by configuration review, not by tests:

- the spreadsheet is shared only with the commercial team;
- the script runs as the owner and is deployed from script version 1;
- cell values are neutralized against formula injection before they leave,
  in lead-submitter (ADR-0007; `lead-request`, `input-validation`).

```yaml interface
id: capture
derived_from: tbo-capture#capture
from: visitor
to: frontend
external: true
protocol: Browser UI with keyboard, pointer and microphone via getUserMedia
data: contact and project fields, voice audio and explicit confirmations
security_templates: [input-validation]
implementations:
  real: React 18 application in the visitor's browser
  double: {kind: fake, name: scripted visitor}
```

```yaml interface
id: token-request
derived_from: tbo-capture#token-request
from: frontend
to: token-issuer
external: false
protocol: HTTPS + JSON POST to a Vercel Function on Node 24
data: a credential request carrying no visitor data; the single-use ephemeral credential or an error
security_templates: [input-validation]
implementations:
  real: token-issuer function at /api/voice-token
  double: {kind: stub, name: stub token issuer}
```

```yaml interface
id: token-source
derived_from: tbo-capture#token-source
from: token-issuer
to: gemini-live
external: true
protocol: HTTPS POST /v1beta/auth_tokens via @google/genai 3.2.0, wire version v1beta per ADR-0002
data: the permanent API key as server-side auth and the token request (uses 1, configured expiry, liveConnectConstraints locking model gemini-3.8-live, response modalities, base system instruction and the llenar_campo declaration); the ephemeral token
security_templates: [outbound-calls, stored-data]
implementations:
  real: Gemini API auth tokens through @google/genai 3.2.0
  double: {kind: fake, name: fake Gemini token source}
```

```yaml interface
id: voice-channel
derived_from: tbo-capture#voice-channel
from: frontend
to: gemini-live
external: true
protocol: WSS Gemini Live API via @google/genai 3.2.0 with the ephemeral token, wire version v1beta, model gemini-3.8-live
data: out, microphone audio and the captured field values as conversation context, never a free system instruction; in, audio and llenar_campo tool calls
security_templates: [input-validation, outbound-calls]
implementations:
  real: Gemini Live session through @google/genai 3.2.0
  double: {kind: fake, name: scripted Gemini Live session}
```

```yaml interface
id: lead-request
derived_from: tbo-capture#lead-request
from: frontend
to: lead-submitter
external: false
protocol: HTTPS + JSON POST to a Vercel Function on Node 24
data: the nine brief fields; 202 Accepted or an error status
security_templates: [input-validation]
implementations:
  real: lead-submitter function at /api/lead
  double: {kind: stub, name: stub lead submitter}
```

```yaml interface
id: validated-delivery
derived_from: tbo-capture#validated-delivery
from: lead-submitter
to: lead-webhook
external: true
protocol: HTTPS + JSON POST to the Apps Script Web App, script version 1, following its 302 redirect to script.googleusercontent.com
data: the validated brief fields, text values starting with =, +, -, @, tab, CR or LF prefixed with an apostrophe (ADR-0007), with any shared secret in the JSON body; a 2xx with an empty body or a JSON success as receipt, or a JSON error, text/html or failure status as failure
security_templates: [outbound-calls, stored-data]
implementations:
  real: Apps Script Web App, script version 1
  double: {kind: fake, name: fake lead webhook}
```

```yaml interface
id: external-routing
derived_from: tbo-capture#external-routing
from: lead-webhook
to: commercial-destination
external: true
protocol: Apps Script write to Google Sheets, inside Google
data: the delivered lead as a sheet row
security_templates: [outbound-calls]
implementations:
  real: Google Sheets spreadsheet written by the Apps Script receiver
  double: {kind: stub, name: "none: no product code reaches this edge; verified by configuration review"}
```

```yaml interface
id: browser-events
derived_from: tbo-capture#browser-events
from: frontend
to: grafana-faro
external: true
protocol: HTTPS via @grafana/faro-web-sdk 2.14.0 to the Faro Cloud collector, API v1
data: allowlisted technical events passed by a beforeSend hook, without PII, field values, audio or credentials
security_templates: [outbound-calls, stored-data]
implementations:
  real: Grafana Faro Cloud collector, API v1
  double: {kind: in-memory, name: in-memory telemetry sink}
```

```yaml interface
id: token-logs
derived_from: tbo-capture#token-logs
from: token-issuer
to: grafana-loki
external: true
protocol: HTTPS + JSON push with Basic Auth to the Loki HTTP ingestion API v1, Pino and a bounded fetch in waitUntil
data: structured issuance events with correlation_id in the body, without PII, token or key; the Grafana Cloud Basic Auth credential
security_templates: [outbound-calls, stored-data]
implementations:
  real: Grafana Loki HTTP ingestion API v1
  double: {kind: in-memory, name: in-memory log sink}
```

```yaml interface
id: lead-logs
derived_from: tbo-capture#lead-logs
from: lead-submitter
to: grafana-loki
external: true
protocol: HTTPS + JSON push with Basic Auth to the Loki HTTP ingestion API v1, Pino and a bounded fetch in waitUntil
data: structured delivery events with correlation_id in the body, without PII or commercial data; the Grafana Cloud Basic Auth credential
security_templates: [outbound-calls, stored-data]
implementations:
  real: Grafana Loki HTTP ingestion API v1
  double: {kind: in-memory, name: in-memory log sink}
```

## Threats

STRIDE for every external interface, and for the two internal interfaces whose
`from` end runs in the visitor's browser. **Test** names the product end and
the template its test is marked with, `@security[<template>]`; *config* means
verified by configuration review, with no product test; *TLS* means covered by
the transport of the platform or SDK, with no test of its own.

**Quota abuse and spam (ADR-0004).** The two browser-facing functions carry no
identity, by design. Mitigations, all without a data store:

- one Vercel Firewall WAF rate limiting rule (Fixed Window, answering 429) on
  `/api/*`; the Hobby plan allows one rate limiting rule among its three
  custom rules;
- the same-origin policy: neither function sends
  `Access-Control-Allow-Origin: *`, so other sites cannot call them from a
  visitor's browser; this does not stop non-browser clients such as curl, which
  the rate limit covers;
- single-use, constrained credentials, one upstream call per request, server
  validation and a body size limit.

Residual risk, accepted for a personal, non-production experiment on free
plans (stack-review.md): a distributed attack from many addresses can still
exhaust the free Gemini quota, which disables voice while the manual form keeps
working; and rate limiting is a usage-priced WAF feature, so on Hobby, which is
never billed, exhausting its included usage may suspend the rule until the
usage window resets.

### capture

| | Status | Mitigation | Test |
|---|---|---|---|
| S | N/A | The visitor is anonymous by design (no account); there is nobody to impersonate | — |
| T | Applicable | Each field is validated; React renders values as text, never through `dangerouslySetInnerHTML` | frontend `input-validation` |
| R | N/A | No identity; the explicit confirmation is the only commitment | — |
| I | Applicable | Captured values leaking into telemetry, covered on `browser-events` | see browser-events |
| D | N/A | A visitor can only block their own tab; server abuse is analysed on token-request and lead-request | — |
| E | Applicable | Injected script, prevented by the same text rendering as T | frontend `input-validation` |

### token-request

| | Status | Mitigation | Test |
|---|---|---|---|
| S | Applicable | Any client may call it. Same-origin policy against other sites in browsers; rate limit against scripts; the credential only opens the constrained session | config (CORS headers, WAF rule) |
| T | Applicable | Only an empty, size-bounded POST is accepted; anything else is refused | token-issuer `input-validation` |
| R | N/A | No identities; each issuance is logged with a correlation_id (REQ-0198) | — |
| I | Applicable | The response carries only the ephemeral credential, never the permanent key (REQ-0161, REQ-0199) | token-issuer `stored-data` |
| D | Applicable | Scripted calls burning the free quota: rate limit, single-use credentials; residual risk accepted above | config (WAF rule) |
| E | Applicable | A leaked credential reused with another model or prompt, blocked by `liveConnectConstraints` | token-issuer `outbound-calls` |

### token-source

| | Status | Mitigation | Test |
|---|---|---|---|
| S | Applicable | The SDK calls Google's fixed endpoint over HTTPS | TLS |
| T | Applicable | HTTPS | TLS |
| R | N/A | Server to provider, no user identity | — |
| I | Applicable | The API key is never logged nor placed in an error | token-issuer `stored-data` |
| D | Applicable | Slow, 429 or failing provider: bounded wait (value an open item), one call without retry, fail-closed error | token-issuer `outbound-calls` |
| E | Applicable | Every request carries `uses: 1` and the constraints | token-issuer `outbound-calls` |

### voice-channel

| | Status | Mitigation | Test |
|---|---|---|---|
| S | Applicable | The SDK opens WSS to Google's endpoint | TLS |
| T | Applicable | Spoken prompt injection or model error: each `llenar_campo` call is validated (known field, type and length); proposals that conflict with manual edits need confirmation; calls after close are discarded (REQ-0115) | frontend `input-validation` |
| R | N/A | No identity | — |
| I | Applicable | Only audio and the declared captured context leave | frontend `outbound-calls` |
| D | Applicable | Handshake failure, 429 or GoAway: one attempt, back to capture with the data kept (REQ-0112) | frontend `outbound-calls` |
| E | Applicable | A call to an undeclared tool: only `llenar_campo` exists, locked by the server; unknown calls are ignored | frontend `input-validation` |

### lead-request

| | Status | Mitigation | Test |
|---|---|---|---|
| S | Applicable | Bots posting without the UI. Same-origin policy against other sites in browsers; rate limit against scripts; server validation is authoritative (REQ-0163) | config (CORS headers, WAF rule) |
| T | Applicable | Client validation bypassed: the server validates every field against its schema. Formula injection: a value starting with `=`, `+`, `-`, `@`, tab (0x09), CR (0x0D) or LF (0x0A) is neutralized as text with a leading apostrophe, never refused, so a phone such as `+52…` stays valid and line breaks inside the message (REQ-0057) are untouched | lead-submitter `input-validation` |
| R | N/A | No accounts; the 202 and the logs carry only a correlation_id | — |
| I | Applicable | Error answers never echo the input or a stack trace | lead-submitter `input-validation` |
| D | Applicable | Spam and oversized bodies: body size limit, one webhook call per request, rate limit; residual risk accepted above | lead-submitter `input-validation`; config (WAF rule) |
| E | N/A | One action, nothing privileged to reach | — |

### validated-delivery

| | Status | Mitigation | Test |
|---|---|---|---|
| S | Applicable | The webhook URL comes from configuration, `https://` only; a missing one is `unconfigured` | lead-submitter `outbound-calls` |
| T | Applicable | HTTPS end to end: the 302 is followed only to an `https://` location, never downgraded to `http://` | lead-submitter `outbound-calls` |
| R | Applicable | The receiver denying receipt: each outcome is logged (REQ-0071) | functional test of REQ-0071 |
| I | Applicable | The URL and any shared secret are never logged; the secret travels in the JSON body, never in the query string; only the declared fields leave | lead-submitter `stored-data` |
| D | Applicable | Slow webhook, HTML, JSON error or Apps Script quotas: 8 s budget, one call, classified answer | lead-submitter `outbound-calls` |
| E | N/A | The call carries no authority beyond writing one lead | — |

### external-routing

No product code runs here (see *Interfaces*); every entry is verified by
configuration review.

| | Status | Mitigation | Test |
|---|---|---|---|
| S | N/A | Google-internal hop | — |
| T | Applicable | A formula executed in Sheets, neutralized upstream on `lead-request` | see lead-request |
| R | N/A | No product party on this edge | — |
| I | Applicable | The sheet shared beyond the commercial team | config |
| D | Applicable | Apps Script or Sheets quotas, surfacing as failures on `validated-delivery` | config |
| E | Applicable | The script runs as its owner: minimal OAuth scopes and a pinned script version | config |

### browser-events

| | Status | Mitigation | Test |
|---|---|---|---|
| S | Applicable | Anyone can post fake telemetry to the public collector: allowed origins restricted (to verify in detailed design); telemetry drives no business decision | config |
| T | Applicable | HTTPS | TLS |
| R | N/A | Technical events, no identity | — |
| I | Applicable | PII in events: an allowlist enforced by a `beforeSend` hook that drops everything else | frontend `stored-data` |
| D | Applicable | Collector down: fail-open (REQ-0114 and the flow-level rules) | frontend `outbound-calls` |
| E | N/A | Nothing privileged behind the collector | — |

### token-logs and lead-logs

Same mitigations on both; the product end is token-issuer, respectively
lead-submitter.

| | Status | Mitigation | Test |
|---|---|---|---|
| S | Applicable | A stolen Basic Auth credential lets others push to the product's Loki: it lives only in the server environment and is never logged | `stored-data` |
| T | Applicable | HTTPS | TLS |
| R | N/A | Technical traces, not audit records | — |
| I | Applicable | PII, credential, key or commercial data in a log line (REQ-0076, REQ-0178, REQ-0181); correlation_id in the body | `stored-data` |
| D | Applicable | Loki slow or down: waitUntil, a fetch bounded by `getDeadline()`, fail-open | `outbound-calls` |
| E | N/A | Nothing privileged behind the push API | — |

## Open items

Carried to detailed design, each to be fixed with a value or a verified fact:

- token-issuer's timeout for the upstream Gemini token request;
- the frontend's maximum wait in `voice-starting` for the credential and the
  WSS handshake;
- whether @google/genai 3.2.0 creates ephemeral tokens on v1beta, as ADR-0002
  pins, or still requires v1alpha;
- restricting the Faro collector's allowed origins in Grafana Cloud;
- the measured margin of the 8 s webhook wait against the 10 s client wait
  (ADR-0006);
- the Vercel WAF rate limiting rule of ADR-0004, configured and reviewed.
