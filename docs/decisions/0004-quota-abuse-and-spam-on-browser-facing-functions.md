# ADR-0004 — Quota abuse and spam on the browser-facing functions

```yaml decision
id: ADR-0004
title: Limit anonymous abuse of the two functions with a WAF rate limit and same-origin, accepting the residual risk
status: accepted
date: '2026-11-20'
decided_by: person
requirements:
- REQ-0086
- REQ-0161
- REQ-0163
question: How should the product limit scripted abuse of the anonymous token and lead functions on free plans?
why_you: It sets what protects the Gemini key quota and the server validation, both high-criticality requirements, and it accepts a residual risk only the owner can accept.
context: token-request and lead-request carry no identity by design, so any client can call /api/voice-token and /api/lead. Scripts can burn the free Gemini quota and spam the commercial sheet. REQ-0086 forbids assuming unverified quotas, REQ-0161 keeps the key on the server, REQ-0163 makes server validation authoritative. Free plans, no data store.
options:
- name: WAF rate limit, same-origin and accepted residual risk
  pros:
  - One Vercel Firewall rate limiting rule (Fixed Window, answers 429) on /api/* is available on Hobby, with no code and no data store.
  - Neither function sends Access-Control-Allow-Origin *, so other sites cannot call them from a visitor's browser.
  cons:
  - A distributed attack from many addresses still passes a per-IP limit.
  - Rate limiting is usage-priced; on Hobby, which is never billed, exhausting its included usage may suspend the rule until the window resets.
- name: Application-level rate limit with a shared store
  pros:
  - Per-client limits independent of the WAF usage allowance.
  cons:
  - Adds a store (for example Redis) the approved stack does not have.
  - Still per-IP, so it does not stop a distributed attack either.
- name: CAPTCHA or proof of work before each call
  pros:
  - Raises the cost of every scripted call, distributed or not.
  cons:
  - Adds a provider, friction and visitor signals sent to a third party.
choice: WAF rate limit, same-origin and accepted residual risk
consequences: 'The rule is configured in the Vercel dashboard and verified by configuration review. Server validation, a body size limit, single-use credentials and one upstream call per request stay in the product. A distributed attack can still exhaust the quota or spam the sheet: accepted by the owner for this experiment, to revisit before any production use.'
```

Sources: [Vercel WAF rate limiting](https://vercel.com/docs/vercel-firewall/vercel-waf/rate-limiting),
[Custom rules and plan limits](https://vercel.com/docs/vercel-firewall/vercel-waf/custom-rules),
[WAF usage and pricing](https://vercel.com/docs/vercel-firewall/vercel-waf/usage-and-pricing),
[Hobby plan](https://vercel.com/docs/plans/hobby).
