---
schema: 1
id: REQ-008
priority: high
source: brief
steps:
  - STEP-002
  - STEP-003
adrs:
  - ADR-003
---

# REQ-008 — Диагностика и достоверный результат

## Requirement

Каждый обязательный gate оставляет machine/human-readable evidence с exact revisions, lifecycle stage, command, exit code, stdout/stderr, migration/reload результатами и diff tracked files. Failure или отсутствие gate evidence не считается успешной qualification.

## Rationale

Maintainer должен воспроизводить failure без transcript AI-сессии.

## Acceptance

- Evidence содержит ordered результаты всех обязательных gates, aggregate result и revisions из REQ-005.
- Failed gate сохраняет stdout/stderr и exit code; незапущенные gates обозначаются явно, schema/incomplete evidence не даёт aggregate PASS.
- Tracked diff отделён от локального operational state; секреты и персональные данные не попадают в evidence.
- Maintainer-tools связывает результат с exact SHA Check; публикация и hard gate реализуются внешним owner.
