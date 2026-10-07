---
schema: 1
id: REQ-003
priority: high
source: brief
steps:
  - STEP-001
  - STEP-002
  - STEP-003
adrs:
  - ADR-002
---

# REQ-003 — Разделение ответственности репозиториев

## Requirement

Canary хранит downstream state и contract его использования. Harness core владеет общими qualification primitives. Maintainer-tools владеет release orchestration, private checkout, GitHub Check и hard publish gate.

## Rationale

Дублирование release engine и специальные canary-ветки в core создают несовместимые источники истины.

## Acceptance

- Документы явно назначают owner каждому действию lifecycle и каждому external prerequisite.
- Canary не содержит отдельный release engine, product runtime, дубликаты synthetic/stress/Windows suites и обходы core protocol.
- Внешние реализации имеют ссылки на core issues 261/263/264 и maintainer-tools issues 7/8; их готовность не объявляется результатом локального INIT.
