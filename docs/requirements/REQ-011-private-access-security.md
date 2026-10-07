---
schema: 1
id: REQ-011
priority: high
source: brief
steps:
  - STEP-003
adrs:
  - ADR-001
  - ADR-003
---

# REQ-011 — Приватный доступ и безопасные границы

## Requirement

Canary остаётся private. Release automation использует scoped GitHub App token с read-доступом к canary и нужному core source; отсутствие доступа выявляется preflight. Repository и evidence не хранят credentials, production secrets или персональные данные.

## Rationale

Приватность baseline совместима с автоматической qualification при явном trust boundary.

## Acceptance

- Внешний runner проверяет private checkout/read до mutation и fail-fast объясняет отсутствие app installation/permissions.
- Contract не требует write permissions на canary для qualification; GitHub Check/publish принадлежат отдельным внешним действиям.
- Credentials предоставляются окружением automation, не выводятся в logs/evidence и не сохраняются в project artifacts.
