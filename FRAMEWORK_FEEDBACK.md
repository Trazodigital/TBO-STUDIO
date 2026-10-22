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

### FB-2 — Bootstrap omits the release accounting required by its feedback gate

- **Date:** 2026-10-21
- **Framework version:** v2.1.2 @ 5afd2d7da26304ddc0b5b062316435c46624920a
- **Severity:** medium
- **Class:** C6
- **Status:** open

**What the framework claims** — `.framework/agent/start_product.md`, steps 3–4,
directs the agent to run the setup, review its files and commit them. The setup
copies the feedback template unchanged in
`.framework/tools/create_product_tool.py:249–253`; the bootstrap instructions
do not explicitly add a release-accounting entry before that first commit.

**What actually happens** — Setup exited 0, but the first PR's quality-gates
run, https://github.com/Trazodigital/TBO-STUDIO/actions/runs/39631453516,
reported `UNACCOUNTED_FRAMEWORK_BUMP`: "The framework moved to 5afd2d7 / v2.1.2
in this pull request, but the log does not name it; record what you found, or
a line such as 'No findings for v2.1.2'."

**Reproduction** — Run the v2.1.2 setup in a product without an existing
feedback log, commit the generated files and introduce the framework pin in a
PR without adding an entry under this file's Log heading. This occurred in
Trazodigital/TBO-STUDIO PR #1 at commit addf83b. Retrieve the observed output
with `gh run view 39631453516 --repo Trazodigital/TBO-STUDIO --log-failed`.

**Verification** — Run: the setup completed locally and the failure occurred
in the linked CI run. The setup source and feedback gate were also read.
Other products were not executed.

**Blast radius** — Observed in this product; the same template-copying path
and bootstrap instructions are shared by new products on v2.1.2.

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
- **Severity:** medium
- **Class:** C6
- **Status:** open

**What the framework claims** — `.framework/agent/start_product.md:80–82`
prescribes the first commit message
`chore: start the product with the ASPICE framework <release>` without a
requirement or issue reference in its header or body.

**What actually happens** — The prescribed message became commit addf83b,
`chore: start the product with the ASPICE framework v2.1.2`. CI run
https://github.com/Trazodigital/TBO-STUDIO/actions/runs/39631453516 reported
`MISSING_REQUIREMENT_TOKEN`: "Commit addf83b 'chore: start the product with the
ASPICE framework v2.1.2' names no requirement or issue; add the REQ-<n> or #<n>
it serves to its header or body."

**Reproduction** — Follow the v2.1.2 bootstrap instructions, use their exact
commit message with the release substituted, then open a PR. The always-on
commit-conventions gate checks every non-merge commit in the PR and rejects
that message. Retrieve this product's observed output with
`gh run view 39631453516 --repo Trazodigital/TBO-STUDIO --log-failed`.

**Verification** — Run: the prescribed commit was created and the linked CI
run rejected it. The instructions and
`.framework/gates/sup/check_commit_conventions_gate.py` were also read.
Other products were not executed.

**Blast radius** — Observed in this product; every new product using that
unmodified prescribed message on v2.1.2 is subject to the same gate rule.

**Impact on this product** — Blocks PR #1. Adding a later compliant commit
alone cannot repair the original message because the gate checks each commit.
The real setup issue is https://github.com/Trazodigital/TBO-STUDIO/issues/2.

**Workaround applied** — With the developer's explicit approval, replace only
the `setup/aspice-framework` branch's setup commit with a message containing
`(#2)` and this feedback record. No change to `main`, framework files or CI
rules. Publication requires a user-run, feature-branch-only force-with-lease;
the corrected commit must receive fresh reviews. Retain this record until
the bootstrap guidance is corrected upstream.
