---
schema: 1
id: ADR-003
status: accepted
date: 2026-10-07
deciders:
  - "Maintainer (подтверждённый brief PROJECT INIT)"
supersedes: []
superseded_by: []
requirements:
  - REQ-004
  - REQ-005
  - REQ-006
  - REQ-008
  - REQ-009
  - REQ-010
  - REQ-011
steps:
  - STEP-002
  - STEP-003
---

# ADR-003 — Exact revisions и fail-closed evidence lifecycle

## Context

Новый candidate SHA требует собственного доказательства; update может потребовать reload или project schema migration. Для failure нужны воспроизводимые факты.

## Problem

Как определить интерфейс canary для внешнего runner, не дублируя его engine и publish policy?

## Decision

Consumer contract фиксирует canary baseline commit, baseline Harness release/ref/exact source revision и candidate repository/release/exact SHA. Runner разрешает tag/ref до immutable commit перед mutation. Ordered flow: access/preflight → disposable checkout → APPLY → explicit reload/repeat APPLY при UPDATER_RELOAD_REQUIRED → RECONCILE при pending migration → STATUS/DOCTOR → validate → configured self-tests → повторный APPLY/NO_UPDATE и сравнение canonical state. Неизвестный transition и любой failed/incomplete mandatory gate дают неуспех. Evidence сохраняет exact identities, stage/command/exit/stdout/stderr, migration/reload и tracked diff до cleanup. Durable machine schema определяется общим core contract, canary документирует semantic fields и примеры; reusable workflow/Check/exact-SHA publish gate принадлежат maintainer-tools.

## Alternatives considered

### PASS по одному validator

Дёшево, но не доказывает update, сохранность истории и idempotence.

### Evidence только в chat

Не воспроизводится из Git/artifact и не подходит automation.

### Повтор failed gate до зелёного

Скрывает race/ошибку и не даёт достоверной qualification.

## Consequences

Локальный consumer contract можно завершить до появления внешнего runner; end-to-end автоматизация остаётся prerequisite core #261 и maintainer-tools #7/#8 и не объявляется выполненной. Baseline promotion отдельно требует release publication и maintainer acceptance.

## Security implications

Private checkout fail-fast предшествует mutation. Tokens не включаются в captured output; caller credentials и candidate code исполняются в границе внешней automation, не в canonical canary.

## Data / migration implications

Повтор APPLY и migration должны быть no-op для canonical state; локальные journals рассматриваются отдельно. При failure сохраняется evidence, disposable copy удаляется после завершения writers.

## Compatibility / operational implications

Нельзя считать reload простым повтором без runtime transition; runner следует актуальному core protocol. Отсутствующие exact identities, stale evidence и пропущенные gates не дают PASS. Полный release qualification также включает внешние compatibility/stress/Windows gates.
