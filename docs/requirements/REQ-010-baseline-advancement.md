---
schema: 1
id: REQ-010
priority: high
source: brief
steps:
  - STEP-002
adrs:
  - ADR-001
  - ADR-003
---

# REQ-010 — Контролируемое продвижение baseline

## Requirement

Baseline продвигается отдельным изменением только после публикации и принятия Harness release как стабильного: APPLY, необходимые reload/reconcile, validation/self-tests, review diff, явный Git workflow и merge в main.

## Rationale

Результат candidate qualification ещё не является разрешением менять стабильный baseline.

## Acceptance

- Contract требует подтверждение опубликованного release и явное решение maintainer о его стабильности; candidate qualification сама не инициирует promotion.
- До merge сохранены exact target release/revision, результаты gates и independent review изменённого состояния.
- При failure или отклонённом review main остаётся прежним; повторный запуск восстанавливается из него, без destructive reset и скрытого rollback в main.
