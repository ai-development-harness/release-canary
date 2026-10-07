---
schema: 1
---
# AI Development Harness Release Canary

## Название

AI Development Harness Release Canary (`release-canary`).

## Краткое описание

Private долгоживущий downstream Harness-проект для проверки обновления предыдущего stable состояния до exact candidate SHA. Ценность проекта — накопленная валидная история, а не product runtime.

## Проблема и цель

Harness Integrity чистого template не покрывает все initialized downstream regressions. Canary добавляет isolated upgrade boundary к release qualification; не заменяет core synthetic, stress и compatibility gates. Первичный bootstrap остаётся на установленном Harness 0.11.2.

## Пользователи / участники

- Maintainer-tools: external release orchestration и scoped private checkout.
- Maintainer Harness: принятие stable baseline и диагностика failed gates.
- Разработчик Harness: воспроизводимый downstream fixture для regression.

## Ключевые сценарии

1. Восстановить accepted baseline из exact Git commit.
2. Проверить exact candidate в disposable copy штатным update/reload/reconcile flow.
3. Сохранить diagnostics, validate/self-tests и повторный APPLY/NO_UPDATE.
4. После публикации и признания release стабильным отдельно продвинуть baseline reviewed изменением.
5. Накопить representative project-owned state через normal Harness STEP/workflows.

## Границы продукта

### In scope

Downstream state, ownership inventory, baseline/preflight/promotion contract и consumer interface для внешней automation.

### Out of scope

Product UI/runtime/БД, release engine, publish automation, дублирование synthetic/stress/Windows suites, копирование Schemor и ручная порча fixture.

## Ограничения

Private repository; main — accepted stable baseline; candidate не push/merge в canary. Без secrets, персональных данных, внешней БД и зависимости от chat/local brief после INIT. Harness-owned изменения делает updater, project migrations — PROJECT RECONCILE. Указание release в lock не подменяет exact source SHA для qualification.

## Нефункциональные ожидания

Воспроизводимость по baseline commit/candidate SHA; идемпотентность; изоляция canonical state; fail-closed diagnostics и сохранение истории. Минимальный стек Git/Python 3.11+ и текстовые артефакты; compatibility horizon следует core.

## Референсы и внешние источники

- [Canary contract, core #263](https://github.com/ai-development-harness/ai-development-harness-template/issues/263).
- [Release hardening epic, core #264](https://github.com/ai-development-harness/ai-development-harness-template/issues/264).
- [Upgrade primitive, core #261](https://github.com/ai-development-harness/ai-development-harness-template/issues/261).
- [Reusable qualification, maintainer-tools #7](https://github.com/ai-development-harness/maintainer-tools/issues/7).
- [Exact-SHA publish gate, maintainer-tools #8](https://github.com/ai-development-harness/maintainer-tools/issues/8).
- [Initialized fixture regression, core #254](https://github.com/ai-development-harness/ai-development-harness-template/issues/254).
- [Отдельный cleanup race, core #256](https://github.com/ai-development-harness/ai-development-harness-template/issues/256).

Тексты issues прочитаны через authenticated GitHub CLI 2026-10-07. Внешняя реализация qualification пока не является результатом этого INIT. Private repository visibility и доступ конкретного release App требуют отдельного operational preflight; пользовательский gh-доступ не доказывает доступ App.

## Основные риски и неопределённости

Материальных нерешённых project-level решений для INIT нет. См. [architecture](architecture.md), [ADR](adr/README.md), [OQ projection](OPEN_QUESTIONS.md). PRN не создаются искусственно: текущие обязательства покрывают REQ/ADR. Baseline SHA появится после отдельной Git-фиксации; release App access и внешние engine gates проверяются в следующих workflows, не объявляются выполненными.
