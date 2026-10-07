---
schema: 1
id: REQ-009
priority: high
source: brief
steps:
  - STEP-002
  - STEP-003
adrs:
  - ADR-003
---

# REQ-009 — Идемпотентное повторное применение

## Requirement

Повторный HARNESS UPDATE APPLY уже применённого exact candidate возвращает штатный NO_UPDATE/no-op без новой canonical mutation. Повторная project migration, если она потребовалась, также не меняет уже migrated state.

## Rationale

Повтор операции выявляет незавершённые migrations и скрытые изменения состояния.

## Acceptance

- Evidence включает результат повторного APPLY и сравнение canonical tracked files до/после него.
- Первичный APPLY имеет реальный transition, повторный после успешного update возвращает штатный NO_UPDATE.
- Локальные execution/journal записи учитываются отдельно; они не подменяют сравнение canonical state.
