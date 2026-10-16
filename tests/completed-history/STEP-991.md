---
schema: 1
id: STEP-991
status: planned
type: implementation
priority: medium
phase: P1
depends_on:
  - STEP-003
requirements:
  - REQ-991
adrs: []
architecture_refs:
  - docs/architecture.md#ownership
risk_flags:
  - none
plan:
  status: not_planned
  revision: 0
  context_basis: null
  content_hash: null
  reviewed_report: null
  planned_at: null
---

# STEP-991 — Сценарий новой зависимой работы

## Goal

Проверить исполнение новой задачи после принятой истории.

## Context

Изолированный тестовый вход, не задача основной истории canary.

## Scope

- Выполнить тестовый consumer.

## Mutation policy

### Allowed

- src/

### Conditional

- none

### Forbidden

- Несвязанные изменения.

## Out of scope

- Продуктовая реализация.

## Acceptance criteria

- Новая работа использует принятую историю без повторной приёмки completed STEP.

## Verification

- manual: проверить тестовый сценарий

## Deliverables

- Результат изолированного теста.

## Implementation plan

- План создаёт runner через deterministic writer.

## Evidence

—

## Blocker / Failure reason

—
