# ADR-0005 — Classification of the lead webhook's 2xx answers

```yaml decision
id: ADR-0005
title: Treat a 2xx carrying text/html or a JSON error as a failed delivery
status: accepted
date: '2026-11-20'
decided_by: person
requirements:
- REQ-0074
- REQ-0146
- REQ-0164
question: Should lead-submitter treat an Apps Script 2xx that carries an HTML page or a JSON error as a failed delivery?
why_you: It decides when a lead counts as received, which three high-criticality receipt requirements govern.
context: REQ-0074, REQ-0146 and REQ-0164 accept "HTTP 2xx, even without a body" as receipt. An Apps Script Web App answers 200 for application errors and may return an HTML page on permission errors or exceptions, so the status code alone cannot tell a stored lead from a lost one. The requirements say nothing about a 2xx whose body reports an error.
options:
- name: Reject 2xx with text/html or a JSON error; accept empty or JSON success
  pros:
  - Keeps the literal criteria, an empty 2xx is still receipt.
  - Turns the receiver's silent failures into an error answer the visitor can retry.
  cons:
  - Adds a classification step the requirements do not spell out.
  - Relies on the operating assumption that the receiver always answers JSON.
- name: Accept every 2xx as receipt
  pros:
  - The simplest reading of the criteria, no body inspection.
  cons:
  - Answers 202 for leads lost by a failing script, a silent data loss.
- name: Require a JSON success body through a change request
  pros:
  - The strictest proof of receipt.
  cons:
  - Contradicts the approved receipt criteria; needs a change request to the three requirements.
choice: Reject 2xx with text/html or a JSON error; accept empty or JSON success
consequences: 'The validated-delivery adapter classifies each answer: an empty 2xx or a JSON success is receipt (202 to the browser); a 2xx with text/html, a JSON error, a non-2xx status or a timeout is a failure. The receiver script must answer JSON for both outcomes; that is an assumption verified by configuration review. No change request is needed.'
```
