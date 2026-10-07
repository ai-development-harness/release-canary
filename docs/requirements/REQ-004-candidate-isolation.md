---
schema: 1
id: REQ-004
priority: high
source: brief
steps:
  - STEP-003
adrs:
  - ADR-001
  - ADR-003
---

# REQ-004 — Изоляция проверки candidate

## Requirement

Qualification использует disposable checkout/worktree/copy exact accepted baseline commit и применяет к нему exact candidate SHA. Успех и failure не меняют canonical canary checkout/main и не push/merge candidate state.

## Rationale

Candidate не должен преждевременно становиться baseline или портить исходную историю.

## Acceptance

- Contract требует зафиксировать baseline commit и candidate SHA до начала mutation.
- Успешный и неуспешный сценарии проверяют сохранность canonical tracked state и refs; изменения остаются в disposable copy.
- Qualification не содержит GitHub mutation и сохраняет failure evidence до cleanup временной копии.
