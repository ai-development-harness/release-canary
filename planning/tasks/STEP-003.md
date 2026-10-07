---
schema: 1
id: STEP-003
status: planned
type: documentation
priority: high
phase: canary-bootstrap
depends_on:
  - STEP-001
  - STEP-002
requirements:
  - REQ-003
  - REQ-004
  - REQ-005
  - REQ-006
  - REQ-007
  - REQ-008
  - REQ-009
  - REQ-011
  - REQ-012
adrs:
  - ADR-001
  - ADR-002
  - ADR-003
architecture_refs:
  - docs/architecture.md#ownership
  - docs/architecture.md#preservation-and-migration
  - docs/architecture.md#qualification-lifecycle
  - docs/architecture.md#security-boundaries
  - docs/architecture.md#compatibility-and-operations
risk_flags:
  - release-critical
  - external-integration
plan:
  status: not_planned
  revision: 0
  context_basis: null
  content_hash: null
  reviewed_report: null
  planned_at: null
---

# STEP-003 — Подготовить интерфейс внешней qualification

## Goal

Получить непротиворечивый canary consumer contract для external Release Qualification, с isolation/evidence и explicit integration prerequisites.

## Context

State STEP-001 и contract STEP-002 являются входами. Core #261 owns executable primitives, maintainer-tools #7/#8 — external workflow/Check/publish gate; их реализация не является mutation scope canary.

## Scope

- Описать semantic inputs/outputs baseline commit, source identities и exact candidate SHA, private access и ordered update flow.
- Определить evidence field meanings, aggregate failure/incomplete/stale semantics, tracked diff и preservation proof; concrete executable schema/entrypoint брать из core, когда доступны.
- Зафиксировать external owner/issues для private scoped checkout, core entrypoint, exact-SHA Check/publish, stress/Windows и cleanup.
- Подготовить непретендующие на реальные runs примеры success/failure/reload/migration/no-op; bounded proof сопоставляет docs с доступным installed protocol, без отдельного release engine.

## Mutation policy

### Allowed

- docs/canary-qualification.md и navigation links в project docs/README.
- Собственный STEP Evidence и штатные review artifacts; projections через tools.

### Conditional

- Уточнение examples после появления опубликованного shared core schema; не создавать competing machine schema.
- Ссылки на фактические external issues/contracts и evidence предоставленного caller run, если доступен, без изменения внешних repositories.

### Forbidden

- Изменение core/maintainer-tools или собственный reusable release workflow/engine в canary.
- Qualification в canonical checkout, candidate push/merge или изменение stable baseline.
- Credentials, выдуманная evidence/history, изменение Harness-owned tools и immutable reports.

## Out of scope

- Проверка App credentials, внешняя реализация Publish gate/Check, выпуск релиза, полная e2e qualification при отсутствии runner.

## Acceptance criteria

- Consumer contract связывает exact baseline/candidate identities, private read preflight, isolation и все ordered lifecycle gates.
- Evidence requirements включают stage/command/exit/stdout/stderr, reload/migration, preservation diff и repeated APPLY/NO_UPDATE; incomplete/stale evidence не даёт PASS.
- Success/failure/reload/migration examples явно помечены как contract examples, не реальные runs; неизвестный transition fail-closed.
- Реализация каждого external prerequisite имеет owner/issue; отсутствие core runner/App access отмечено честно, локальные docs не объявляются working release integration.
- Independent review подтверждает consistency с REQ/ADR, STEP-001 inventory и STEP-002 preflight; нет duplicating engine или main mutation.

## Verification

- command: `python3 .harness/tools/validate.py --mode manual`
- command: `python3 .harness/tools/traceability-coverage.py --json`
- command: `python3 .harness/tools/check-command-references.py --json`
- manual: Сопоставить contract с installed updater/EXECUTION_PROTOCOL/ownership и external issues; отметить unavailable executable interface.
- manual: Проверить таблицу missing-access, stale-SHA, skipped-gate, reload-required, migration-required и failure-before-cleanup; отличить contract review от e2e run.

## Deliverables

- docs/canary-qualification.md: semantic inputs/outputs, lifecycle, evidence и ownership/prerequisite table.
- Independent contract review и bounded proof без external mutation.

## Implementation plan

Заполняется командой STEP PLAN STEP-003. До independent planning-review PASS план не имеет status ready. Конкретные customization и executable proof выбираются по current installed contract, а не угадываются в INIT.

## Evidence

INIT фиксирует только contract будущей работы. Команды, результаты и review evidence появятся при выполнении этого STEP; generated Verification evidence пишет deterministic runner.

## Blocker / Failure reason

—
