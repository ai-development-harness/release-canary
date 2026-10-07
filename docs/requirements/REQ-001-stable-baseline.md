---
schema: 1
id: REQ-001
priority: high
source: brief
steps:
  - STEP-001
  - STEP-002
adrs:
  - ADR-001
---

# REQ-001 — Воспроизводимый стабильный baseline

## Requirement

Git repository ai-development-harness/release-canary хранит долгоживущий initialized downstream baseline. Ветка main представляет последнее принятое стабильное состояние; первичный INIT использует уже установленный Harness 0.11.2, без обновления до candidate.

## Rationale

Контроль обновления требует реального предыдущего состояния, воспроизводимого независимо от локальной сессии.

## Acceptance

- Baseline восстанавливается из exact Git commit без local brief, chat history, внешней БД и приватных локальных файлов.
- Версия bootstrap подтверждается manifest и lock: 0.11.2, source ref v0.11.2; baseline commit фиксируется после отдельной Git-публикации.
- До принятия нового стабильного релиза main сохраняет предыдущий accepted baseline.
