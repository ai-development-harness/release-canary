---
schema: 1
id: ADR-002
status: accepted
date: 2026-10-07
deciders:
  - "Maintainer (подтверждённый brief PROJECT INIT)"
supersedes: []
superseded_by: []
requirements:
  - REQ-002
  - REQ-003
  - REQ-006
  - REQ-007
  - REQ-012
steps:
  - STEP-001
  - STEP-002
  - STEP-003
---

# ADR-002 — Ownership и сохранение downstream истории

## Context

Regression initialized downstream не ловится стерильным template. При этом реальный canary не должен становиться вторым release engine.

## Problem

Как сохранить допустимое project-owned состояние без специальных исключений в Harness core?

## Decision

Canary хранит state и consumer contract; core содержит общие update/qualification primitives и synthetic/stress/compatibility tests; maintainer-tools оркестрирует qualification и публикацию. Protocol layer обновляет штатный updater. Project schema/templates migrates через PROJECT RECONCILE; Accepted ADR и immutable historical reports не переписываются. Representative state создаётся отдельными normal STEP/workflows после INIT, включая допустимые template/config customization. PRN/OQ создаются только по фактической необходимости, а не для заполнения списка типов.

## Alternatives considered

### Release engine внутри canary

Локальная автономность ценой duplication и расхождения core contract.

### Ручная порча fixture

Быстро воспроизводит ошибку, но проверяет невалидный state вместо обещанного update contract.

### Регулярный reset к template

Сокращает историю, но удаляет саму ценность долгоживущего canary.

## Consequences

Canary зависит от external core/maintainer-tools interfaces. Изменения в этих repositories выполняются по соответствующим issues, а локальный roadmap обеспечивает документы и bounded proof, не внешнюю реализацию.

## Security implications

Отсутствует product runtime; trust boundary проходит между automation credentials, disposable checkout и canonical Git state. Unknown/failed operations не подавляются.

## Data / migration implications

Ownership inventory отличает protocol-owned, project-owned и historical immutable paths. Migration сохраняет смысл Accepted ADR и pin/bytes исторических evidence согласно core protocol.

## Compatibility / operational implications

Python/Git следуют documented core minimum; сейчас Python 3.11+. Canary не вводит Node.js/БД и не дублирует Windows coverage. Отсутствующий external primitive фиксируется как prerequisite, без canary-specific обхода.
