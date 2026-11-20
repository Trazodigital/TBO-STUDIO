# ADR-0006 — Upstream wait for the lead webhook

```yaml decision
id: ADR-0006
title: Bound the upstream lead webhook wait at 8 seconds including redirects
status: accepted
date: '2026-11-20'
decided_by: person
requirements:
- REQ-0079
- REQ-0144
question: How long may lead-submitter wait for the lead webhook, including the Apps Script redirect, before it answers a failure?
why_you: It fixes the operating value of the high-criticality upstream wait ceiling and its margin against the client's wait limit.
context: 'REQ-0079 caps the upstream wait at ten seconds and envio INV-13 leaves the operating value to design. REQ-0144 ends the client wait at ten seconds. If the server waited the full 10 s, the browser could give up while the lead is still being stored, and a retry would duplicate it: INV-2 and INV-7 promise no deduplication. Cold start and the Apps Script 302 redirect both spend part of the window.'
options:
- name: 10 s
  pros:
  - The most time for a slow Apps Script execution.
  cons:
  - No margin before the client's 10 s limit; client timeouts while the lead is stored become likely.
- name: 8 s
  pros:
  - About 2 s of margin for cold start and the response to reach the browser.
  - Still generous for an Apps Script append to a sheet.
  cons:
  - The 2 s margin is an assumption until measured.
- name: 6 s
  pros:
  - A wide margin against client timeouts.
  cons:
  - More false failures on slow but successful Apps Script runs, which also produce duplicates on retry.
choice: 8 s
consequences: lead-submitter aborts the webhook call, redirects included, after 8 s and answers a failure; one call, no automatic retry. The function's maxDuration must cover the 8 s plus a bounded Loki push. The 2 s margin is measured in detailed design; duplicates are reduced, not prevented.
```
