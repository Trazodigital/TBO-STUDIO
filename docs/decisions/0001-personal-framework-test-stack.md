# ADR-0001 — Personal framework test stack

```yaml decision
id: ADR-0001
title: Preserve the prototype UI while updating the supported build toolchain
status: proposed
date: "2026-11-12"
context: >-
  REQ-0028 prohibits product-owned commercial storage. The owner wants a personal,
  non-production framework experiment costing 0 MXN per month, retaining React,
  Vite, TypeScript, Tailwind, thinking-orbs, mp4box and lucide-react, a TypeScript
  server, Vercel and an external Apps Script/Sheets receiver. Versions must be
  honest; a passing schema is not evidence of provider availability.
options:
  - name: Preserve React 18 and Tailwind 3; use Vite 7
    pros:
      - Retains React 18.3.1, Tailwind 3.4.19 and the prototype library APIs.
      - Vite 7.3.8 remains supported and fits plugin-react 4.7.0 and Vitest 5.1.0 declared ranges.
      - Node Functions avoid introducing a second application-server framework.
    cons:
      - Keeps an older supported Vite branch rather than its newest major.
      - Managed implementation patches are not frozen; migrated-build tests remain pending.
  - name: Upgrade the frontend toolchain to Vite 8
    pros:
      - Uses the current Vite major, with candidate Vite 8.3.8 and plugin-react 6.3.0.
      - Can still retain React 18 and Tailwind 3 rather than bundling unrelated visual migrations.
    cons:
      - Changes the bundler/plugin major and introduces more migration validation for this learning exercise.
      - Does not resolve managed-service versioning or account free-tier constraints.
  - name: Reproduce the prototype with Vite 5 unchanged
    pros:
      - Closest dependency baseline to the existing prototype.
    cons:
      - Vite 5 no longer receives support and does not satisfy current Vitest peer requirements.
choice: Preserve React 18 and Tailwind 3; use Vite 7
consequences: >-
  Keep storage external; use synthetic data and provider doubles in ordinary CI.
  Pin installable tools and later lock transitive dependencies. Use tsc -b,
  Vitest, Playwright, ESLint, Prettier and native SARIF scanners. Loki uses Pino
  plus bounded Node fetch/waitUntil rather than an additional batching transport.
  No production/data migration is needed because none is being operated.
  Apps Script script version 1 is selected for the first Web App deployment;
  remote deployment has not been verified. This is a proposal, not checkpoint
  approval: apply ADR-0002's explicit provider/API version interpretation and
  verify the installed/migrated toolchain before
  claiming readiness. Do not change requirements, gates, provider accounts or
  deploy through this decision alone.
```

Evidence, source links and operational limits: [stack review](../architecture/stack-review.md).
