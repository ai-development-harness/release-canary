---
schema: 1
id: REQ-005
priority: high
source: brief
steps:
  - STEP-002
  - STEP-003
adrs:
  - ADR-001
  - ADR-003
---

# REQ-005 — Точная идентичность входов qualification

## Requirement

Preflight и evidence однозначно связывают baseline commit, baseline Harness release/source revision и candidate Harness release/exact SHA. Mutable ref разрешается до запуска; отсутствие exact revision не заменяется предположением.

## Rationale

Проверка старого SHA не доказывает безопасность изменённого candidate.

## Acceptance

- Набор входов включает canary repository, baseline commit, baseline Harness version/ref/revision и candidate repository/release/SHA.
- Если lock содержит release tag без SHA, runner разрешает его до exact commit и сохраняет соответствие; невозможность разрешения блокирует запуск.
- Evidence для другого candidate SHA считается stale и не даёт PASS; одинаковые входы выбирают одинаковую последовательность lifecycle gates.
