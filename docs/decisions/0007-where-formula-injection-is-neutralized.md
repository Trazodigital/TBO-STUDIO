# ADR-0007 — Where formula injection is neutralized

```yaml decision
id: ADR-0007
title: Neutralize spreadsheet formulas in lead-submitter and declare it in the validated-delivery contract
status: accepted
date: '2026-11-20'
decided_by: person
requirements:
- REQ-0057
- REQ-0163
- REQ-0164
question: Should the formula-injection neutralization live in lead-submitter, declared in the validated-delivery contract, or in the Apps Script receiver?
why_you: It places a security mitigation of the server validation and delivery requirements, both rated high.
context: 'Brief values end up as cells in a Google Sheet. A value starting with =, +, -, @, tab, CR or LF can be read as a formula. The mitigation prefixes such a value with an apostrophe so it stays text, never refusing it: a phone such as +52 stays valid and line breaks inside the message stay (REQ-0057). The review found the architecture claimed the product was decoupled from the receiver while lead-submitter applied a Sheets-specific rule the validated-delivery data did not show.'
options:
- name: In lead-submitter, declared in validated-delivery
  pros:
  - Tested in the product under @security[input-validation].
  - The contract shows exactly what the receiver gets.
  cons:
  - Couples the product to a spreadsheet receiver; any future receiver also gets the apostrophe.
- name: In the Apps Script receiver, writing values as plain text
  pros:
  - The product sends the values unchanged and stays receiver-agnostic.
  cons:
  - The mitigation lives outside the repository and is verified only by configuration review.
  - A receiver change can silently drop it.
choice: In lead-submitter, declared in validated-delivery
consequences: validated-delivery data states that text values starting with =, +, -, @, tab, CR or LF arrive prefixed with an apostrophe. The architecture no longer claims the product is decoupled from the receiver. Replacing the sheet with another receiver needs a new record that supersedes this one.
```
