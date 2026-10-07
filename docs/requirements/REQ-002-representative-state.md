---
schema: 1
id: REQ-002
priority: high
source: brief
steps:
  - STEP-001
adrs:
  - ADR-001
  - ADR-002
---

# REQ-002 — Реалистичное накопленное состояние

## Requirement

После INIT проект накапливает валидные project-owned REQ/ADR/STEP, допустимые настройки и шаблоны, естественные lifecycle transitions и immutable reports через поддерживаемые Harness workflows. OQ и PRN создаются лишь при реальной неопределённости или сквозном инженерном инварианте.

## Rationale

Чистый template не покрывает regression на уже initialized downstream state.

## Acceptance

- Инвентаризация различает исходный INIT state и результаты последующих штатных workflows; присутствуют допустимая customization template/config и завершённая история хотя бы одного STEP.
- Reports имеют реальные команды/reviews и не создаются задним числом как выдуманная история.
- State проходит validator своей стабильной версии; отсутствуют ручная порча fixture, копирование продуктового repository и регулярный сброс к template.
