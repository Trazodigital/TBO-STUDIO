# ADR-0002 — Provider selection and API contract versions

```yaml decision
id: ADR-0002
title: Declare provider selection and API contract versions with explicit wire mappings
status: proposed
date: "2026-11-12"
context: >-
  The owner requests Node24, Gemini label v1-beta and Faro API v1 so the stack
  describes the selected contracts rather than inventing managed server builds.
  stack.v2 accepts these strings but does not define their granularity.
options:
  - name: Declare selected provider major and API contracts with explicit mappings
    pros:
      - Node24 matches the provider-major selection while local/CI remains 24.22.3.
      - Gemini v1-beta is a documented stack-only label mapping to actual wire v1beta.
      - Faro v1 names the public API major whose OpenAPI info.version is 1.0.0.
    cons:
      - These labels do not pin provider minor/patch releases or immutable implementations.
      - The Gemini label needs a recorded mapping and must never be copied into SDK apiVersion.
      - Short labels are not complete strict SemVer versions and must not be advertised as such.
  - name: Require literal provider identifiers and exact managed runtime builds
    pros:
      - Avoids normalized-label interpretation and preserves literal API spelling in version.
      - Makes any missing immutable provider build conspicuous.
    cons:
      - Literal v1beta is rejected by the current schema.
      - Vercel does not let the product freeze its managed Node patch.
      - Requiring a hosted build overlooks Faro's separately published API contract version.
choice: Declare selected provider major and API contracts with explicit mappings
consequences: >-
  Use version strings 24, v1-beta and v1 in the three stack rows. Send v1beta
  to Gemini unchanged. Faro v1 is the major of API info.version1.0.0, not the
  OpenAPI document format3.0.0 or SDK2.14.0. Retain Node24.22.3 for local/CI.
  Preserve the historical literal-schema reproductions and append FB4–6
  follow-ups; do not claim an upstream schema fix. This user-authorized
  interpretation does not approve checkpoint3, prove provider availability,
  remove FB7's security assurance gap, authorize installation or deploy code.
```

Sources: [Vercel selection](https://vercel.com/docs/functions/runtimes/node-js/node-js-versions),
[Gemini wire API](https://ai.google.dev/gemini-api/docs/ephemeral-tokens),
[Faro API specification](https://raw.githubusercontent.com/grafana/faro/main/spec/gen/faro.gen.yaml),
[strict SemVer grammar](https://semver.org/).
