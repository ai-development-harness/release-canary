---
schema: 1
id: REQ-006
priority: high
source: brief
steps:
  - STEP-002
  - STEP-003
adrs:
  - ADR-002
  - ADR-003
---

# REQ-006 — Штатный lifecycle обновления и восстановления

## Requirement

Обновление выполняется canonical HARNESS UPDATE APPLY. При UPDATER_RELOAD_REQUIRED runner перезагружает runtime и повторяет APPLY; pending project schema migration обрабатывается PROJECT RECONCILE. После перехода выполняются HARNESS STATUS, HARNESS DOCTOR, validator и configured self-tests.

## Rationale

Реальные переходы release graph должны пройти общую границу update/reconcile.

## Acceptance

- Contract покрывает обычный APPLY, reload-required и migration-required результаты, а также failure на каждой стадии.
- Неизвестный transition, unresolved prerequisite или failed mandatory gate останавливает qualification; слепые retry/sleep и подавление ошибок не дают PASS.
- В baseline advancement используются те же поддерживаемые переходы; recovery сохраняет прежний main и диагностику неуспеха.
