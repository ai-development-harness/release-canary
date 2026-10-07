---
schema: 1
id: STEP-001
status: planned
type: implementation
priority: high
phase: canary-bootstrap
depends_on: []
requirements:
  - REQ-001
  - REQ-002
  - REQ-003
  - REQ-007
  - REQ-012
adrs:
  - ADR-001
  - ADR-002
architecture_refs:
  - docs/architecture.md#ownership
  - docs/architecture.md#baseline-state
  - docs/architecture.md#preservation-and-migration
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

# STEP-001 — Сформировать representative project-owned состояние

## Goal

Получить небольшой валидный downstream state с естественной историей workflows и допустимой project-owned customization.

## Context

INIT создал canonical REQ/ADR и реальные INIT reviews на Harness 0.11.2. У initialized template ещё нет representative post-INIT state, который должен переживать последующие releases (core #263).

## Scope

- Составить ownership inventory baseline: protocol-owned, project-owned, immutable reports и local operational state.
- Через normal Harness workflows выполнить допустимую customization project-owned template/config с пояснением реального назначения; выбранные fields/sections согласовать с установленным schema contract.
- Зафиксировать реальные planning/implementation/review lifecycle evidence этого STEP; сохранять исходные INIT reports.
- OQ/PRN добавлять только при реальном основании, без искусственной незавершённости ради fixture.

## Mutation policy

### Allowed

- Project-owned docs/ и planning/ внутри scope STEP, кроме immutable historical reports; шаблоны — только совместимая customization после INIT.
- Разрешённые generated project blocks README.md/AGENTS.md; projections только sync-projections.

### Conditional

- Project configuration в manifest — только обоснованная supported настройка; не менять project.initialized/name или Harness version.
- Новые OQ/PRN/REQ — только по подтверждённой необходимости и штатным workflows с обратными refs.

### Forbidden

- Harness-owned tools/protocol/runtime adapters, version lock и updater policy.
- Перезапись Accepted ADR/immutable reports, fake history, ручная порча fixture, копирование другого продукта.
- Candidate update, GitHub mutation и release orchestration.

## Out of scope

- Baseline advancement и release qualification integration; product runtime, БД и CI extensions.

## Acceptance criteria

- Inventory объясняет ownership и содержит конкретные paths/hash baseline artifacts.
- Есть schema-compatible project-owned template/config customization, отличающаяся от чистого template, и объяснение её назначения; нет выдуманных reports/OQ/PRN.
- Завершение этого STEP даёт естественный completion proof и independent review; исходная INIT history сохранена.
- Validator и configured self-tests проходят на initialized customized состоянии; результат не объявляется candidate qualification.

## Verification

- command: `python3 .harness/tools/validate.py --mode manual`
- command: `python3 .harness/tools/traceability-coverage.py --json`
- command: `python3 .harness/tools/check-command-references.py --json`
- command: `python3 .harness/tools/run-self-tests.py`
- manual: Сравнить inventory до/после; подтвердить сохранность immutable reports и отсутствие unrelated changes.

## Deliverables

- docs/canary-state.md: inventory, происхождение state и customization rationale.
- Допустимая project-owned customization и реальные PLAN/REVIEW/Evidence этого STEP.

## Implementation plan

Заполняется командой STEP PLAN STEP-001. До independent planning-review PASS план не имеет status ready. Конкретные customization и executable proof выбираются по current installed contract, а не угадываются в INIT.

## Evidence

INIT фиксирует только contract будущей работы. Команды, результаты и review evidence появятся при выполнении этого STEP; generated Verification evidence пишет deterministic runner.

## Blocker / Failure reason

—
