---
schema: 1
id: REQ-007
priority: high
source: brief
steps:
  - STEP-001
  - STEP-002
  - STEP-003
adrs:
  - ADR-002
---

# REQ-007 — Сохранность project-owned артефактов

## Requirement

Updater меняет Harness-owned protocol layer; project-owned REQ/ADR/STEP/config/templates меняются только допустимым Harness lifecycle и явными project workflows. Immutable historical reports и смысл Accepted ADR сохраняются.

## Rationale

Сохранность накопленного состояния является основной ценностью canary.

## Acceptance

- Inventory отделяет protocol-owned, project-owned и immutable historical artifacts; до/после update сравниваются paths и содержимое.
- Project schema migration допускается через PROJECT RECONCILE с проверкой результата и повторного no-op; updater не переписывает project-owned документы напрямую.
- Необъяснённая потеря, перезапись immutable report или смысловое изменение Accepted ADR блокирует приёмку, а допустимые migrations отражаются в evidence.
