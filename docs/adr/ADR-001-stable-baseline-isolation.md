---
schema: 1
id: ADR-001
status: accepted
date: 2026-10-07
deciders:
  - "Maintainer (подтверждённый brief PROJECT INIT)"
supersedes: []
superseded_by: []
requirements:
  - REQ-001
  - REQ-002
  - REQ-004
  - REQ-005
  - REQ-010
  - REQ-011
steps:
  - STEP-001
  - STEP-002
  - STEP-003
---

# ADR-001 — Стабильный baseline и изолированный candidate

## Context

Canary должен переживать реальные релизы, сохраняя накопленное initialized состояние. Brief прямо задаёт private visibility, stable main, disposable candidate и bootstrap на установленном release.

## Problem

Как отделить принятую историю baseline от временного candidate и обеспечить воспроизводимость?

## Decision

Private Git repository является единственным durable source baseline; main хранит accepted stable state. Первичный INIT использует установленный Harness 0.11.2 (lock source ref v0.11.2). Qualification разрешает baseline commit и candidate до exact SHA и работает только с disposable copy. Продвижение после публикации/принятия стабильного release — отдельное reviewed изменение через canonical Git workflow. INIT и qualification не разрешают commit/push/merge сами по себе.

## Alternatives considered

### Candidate сразу в main

Упрощает checkout, но теряет предыдущий stable и нарушает изоляцию.

### Чистый template на каждый запуск

Проще пересоздать, но исчезает накопленный downstream state.

### Продуктовый repository как fixture

Даёт историю, но связывает release infrastructure с посторонним продуктом и данными.

## Consequences

Baseline может отставать от свежего release до явного принятия. Нужен отдельный promotion review; provenance нельзя восстановить только из mutable branch/tag.

## Security implications

Read token получает только нужные repository permissions; qualification не имеет права менять main. Credentials и персональные данные не хранятся.

## Data / migration implications

Git хранит canonical state и immutable reports. Нет внешней БД; failed disposable state не переносится обратно.

## Compatibility / operational implications

Проверка core transition не отменяет существующие release graph constraints. При неуспехе baseline остаётся прежним; bootstrap SHA появится только после отдельно авторизованной Git-фиксации.
