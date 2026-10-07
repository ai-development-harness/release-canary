---
schema: 1
id: STEP-002
status: planned
type: documentation
priority: high
phase: canary-bootstrap
depends_on:
  - STEP-001
requirements:
  - REQ-001
  - REQ-003
  - REQ-005
  - REQ-006
  - REQ-007
  - REQ-008
  - REQ-009
  - REQ-010
  - REQ-012
adrs:
  - ADR-001
  - ADR-002
  - ADR-003
architecture_refs:
  - docs/architecture.md#ownership
  - docs/architecture.md#baseline-state
  - docs/architecture.md#preservation-and-migration
  - docs/architecture.md#baseline-advancement-and-recovery
  - docs/architecture.md#qualification-lifecycle
  - docs/architecture.md#compatibility-and-operations
risk_flags:
  - release-critical
plan:
  status: not_planned
  revision: 0
  context_basis: null
  content_hash: null
  reviewed_report: null
  planned_at: null
---

# STEP-002 — Определить preflight и продвижение stable baseline

## Goal

Получить проверяемый contract baseline preflight/promotion с bounded proof на фактическом representative state.

## Context

STEP-001 supplies inventory/customization и завершённую history. Main нельзя автоматически продвигать после candidate PASS; release publication и принятие maintainer — отдельные prerequisites.

## Scope

- Описать preflight: exact baseline commit, manifest/lock/source identities, initialized state, schema/projections, ownership inventory, STATUS/DOCTOR и gates.
- Описать controlled promotion опубликованного/принятого stable release: рабочая ветка, APPLY, reload/reconcile, validation/self-tests, review diff и отдельно authorized canonical Git merge.
- Описать failure/recovery, повторный APPLY/NO_UPDATE и различие local journal/canonical no-op.
- Проверить доступные read-only preflight commands на текущем baseline и decision table для missing revision/failed gate/unpublished release; не применять неизвестный future release.

## Mutation policy

### Allowed

- docs/canary-baseline.md, docs/development.md, relevant project navigation blocks.
- Собственный STEP Evidence и штатные review artifacts; projections через deterministic tools.

### Conditional

- Небольшие consumer examples в docs/ без executable release engine, если они проясняют поля evidence.
- Исправление task-local contract этого STEP через supported planning workflow; Accepted ADR не переписываются.

### Forbidden

- Promotion main, реальный candidate APPLY или GitHub mutation в рамках подготовки contract.
- Changes core/maintainer-tools, Harness-owned files, immutable reports и результат STEP-001.
- Обход update graph/migration gates и произвольный destructive rollback.

## Out of scope

- Выпуск или продвижение нового release, настройка external App, reusable workflow/publish gate, full cross-platform qualification.

## Acceptance criteria

- Preflight описывает exact identities и проверяемую принадлежность stable baseline; фактически доступные команды проверены на state STEP-001.
- Promotion требует published release и явное stable acceptance; failed gate/review оставляет main прежним.
- Contract покрывает reload-required, migration-required, unknown transition, preservation inventory и canonical idempotence.
- Для каждой failure branch указан stage/result/evidence/recovery; отсутствие future candidate не заменяется выдуманным e2e PASS.
- Target release/SHA и Git publication остаются отдельным explicit workflow; schema/current и command references валидны.

## Verification

- command: `python3 .harness/tools/validate.py --mode manual`
- command: `python3 .harness/tools/migrate-project-schema.py --check --json`
- command: `python3 .harness/tools/traceability-coverage.py --json`
- command: `python3 .harness/tools/check-command-references.py --json`
- manual: Прочитать фактические HARNESS STATUS/DOCTOR через canonical dispatcher и сохранить результат preflight без candidate mutation.
- manual: Проверить decision table: unpublished target, missing exact SHA, failed migration/gate и отклонённый review не разрешают promotion.

## Deliverables

- docs/canary-baseline.md: preflight, promotion и failure/recovery contract.
- Evidence реальных read-only checks и independent review документа.

## Implementation plan

Заполняется командой STEP PLAN STEP-002. До independent planning-review PASS план не имеет status ready. Конкретные customization и executable proof выбираются по current installed contract, а не угадываются в INIT.

## Evidence

INIT фиксирует только contract будущей работы. Команды, результаты и review evidence появятся при выполнении этого STEP; generated Verification evidence пишет deterministic runner.

## Blocker / Failure reason

—
