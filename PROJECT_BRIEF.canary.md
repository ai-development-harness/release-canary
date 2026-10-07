# Project Brief — AI Development Harness Release Canary

## Что я хочу сделать

Создать служебный downstream-проект **AI Development Harness Release Canary**.

Это должен быть обычный, долгоживущий, initialized Harness-проект, который используется как реалистичная контрольная точка перед публикацией новых релизов AI Development Harness.

Репозиторий не является примером приложения и не должен содержать выдуманный product runtime. Его ценность — в накопленном project-owned состоянии и в том, что новый Harness release проверяется не только на чистом template, но и на проекте, который уже пережил предыдущие версии и миграции.

Основные связанные репозитории:

- Harness core/template: https://github.com/ai-development-harness/ai-development-harness-template
- Release automation: https://github.com/ai-development-harness/maintainer-tools
- Canary: https://github.com/ai-development-harness/release-canary

Связанный release-hardening epic:

- https://github.com/ai-development-harness/ai-development-harness-template/issues/264
- canary contract: https://github.com/ai-development-harness/ai-development-harness-template/issues/263

## Зачем

Текущий Harness Integrity хорошо проверяет внутренние invariants самого template, но этого недостаточно для безопасного релиза.

После v0.11.0 реальные downstream-обновления обнаружили два разных класса проблем:

1. дефект, который проявлялся только при обновлении уже initialized проекта с project-owned состоянием;
2. intermittent race в synthetic/process lifecycle.

Release Canary должен закрыть первую границу: до публикации release candidate необходимо доказать, что **реальный initialized downstream-проект предыдущего стабильного состояния корректно обновляется до exact candidate revision**.

Canary не заменяет synthetic/unit/stress/Windows compatibility tests. Он дополняет их release-level проверкой жизненного цикла обновления.

## Пользователи / участники

Основные пользователи:

1. **Release automation** из `ai-development-harness/maintainer-tools`.
2. **Maintainer AI Development Harness**, который анализирует failed qualification.
3. Разработчики Harness, которым нужен воспроизводимый downstream fixture для regression/debugging.

Конечных пользователей у canary как у продукта нет.

## Основные сценарии

### 1. Хранение стабильного downstream baseline

Ветка `main` должна представлять **последнее принятое стабильное состояние canary**, а не текущий release candidate.

После PROJECT INIT canary становится обычным initialized Harness-проектом и дальше обновляется только штатным Harness update/reconcile flow.

Canonical baseline должен быть воспроизводим из Git без chat/session memory и без внешней БД.

### 2. Проверка release candidate

Release Qualification создаёт disposable checkout/копию canary baseline и применяет к ней exact candidate revision Harness.

Минимальный сценарий:

```text
stable canary state
        ↓
exact candidate SHA
        ↓
HARNESS UPDATE APPLY
        ↓
reload / повторный APPLY, если этого требует transition
        ↓
PROJECT RECONCILE, если требуется migration
        ↓
HARNESS STATUS
HARNESS DOCTOR
        ↓
validate
        ↓
configured synthetic/self-tests
        ↓
повторный HARNESS UPDATE APPLY
        ↓
NO_UPDATE / idempotent state
```

Никакие изменения candidate qualification не должны автоматически попадать обратно в `main` canary.

### 3. Продвижение baseline после успешного релиза

Когда Harness release уже опубликован и признан стабильным, canary baseline обновляется до него отдельным контролируемым изменением:

1. штатный `HARNESS UPDATE APPLY`;
2. необходимые migration/reconcile;
3. validation;
4. review diff;
5. merge в `main`.

Release candidate нельзя заранее делать новым canonical baseline.

### 4. Реалистичное project-owned состояние

Canary должен постепенно содержать допустимое состояние, характерное для долгоживущего Harness-проекта, а не оставаться почти чистым template.

После INIT отдельными STEP через поддерживаемые Harness workflows нужно сформировать representative state, например:

- реальные REQ / ADR / STEP / OQ / PRN;
- project-owned templates после допустимых schema migrations/customization;
- historical immutable reports, появившиеся естественно через Harness workflows;
- resolved/open lifecycle state;
- project configuration, отличающийся от стерильного template там, где это допустимо;
- артефакты, которые должны переживать Harness update без потери или переписывания.

Нельзя создавать «сломанный fixture» ручной порчей файлов только ради теста. State должен быть валидным для той стабильной версии Harness, которой соответствует baseline.

### 5. Диагностика failed qualification

При ошибке release automation должна иметь достаточно фактов, чтобы понять:

- baseline Harness release/revision;
- candidate release/revision;
- какой lifecycle step упал;
- stdout/stderr и exit code deterministic команды;
- возник ли schema migration;
- был ли transition reload-required;
- какие tracked files изменились.

Canary не должен зависеть от сохранённого transcript AI-сессии как от evidence.

## Ограничения и обязательные условия

### Repository / visibility

- Repository: `ai-development-harness/release-canary`.
- Visibility: private.
- Release GitHub App / automation token должен иметь read-доступ к этому private repository.

### Source of truth

- Git repository — единственный durable source of canary baseline.
- `main` — accepted stable baseline.
- Candidate test выполняется в disposable checkout/worktree/copy.
- Не использовать Schemor или другой продуктовый repository как скрытый canary.

### Harness ownership

Нужно сохранять границу ownership:

- Harness-owned protocol files обновляются штатным updater;
- project-owned files не должны переписываться release automation напрямую;
- migration выполняется через предусмотренный Harness lifecycle.

### Безопасность

- Никаких production secrets.
- Никаких персональных данных.
- Никакой зависимости от приватных локальных файлов кроме штатного local brief во время первоначального INIT.
- Qualification не должна push/merge candidate state в canary.
- Любая mutation GitHub должна быть отдельным явным release/baseline advancement шагом.

### Совместимость

Canary должен оставаться пригодным минимум для документированной нижней границы Harness, включая Python 3.11, если core contract её сохраняет.

Platform-specific Windows coverage остаётся отдельной обязанностью Harness release qualification; canary не обязан дублировать весь Windows matrix внутри своего repository.

## Предпочтительный стек

Canary не должен вводить отдельный product stack без необходимости.

Предпочтения:

- Git;
- Python из Harness tooling;
- GitHub Actions / release automation там, где orchestration действительно должна жить;
- Markdown/YAML/TOML/JSON как project/Harness artifacts.

Не добавлять Node.js, frontend/backend framework, database или сервис только для того, чтобы canary выглядел как «настоящий продукт».

Automation ownership предпочтительно разделить так:

- **release-canary** хранит реалистичный downstream state и его contract;
- **ai-development-harness-template** хранит canonical Harness qualification primitives;
- **maintainer-tools** оркестрирует release candidate и hard publish gate.

Не дублировать release engine внутри canary.

## Что точно не нужно

- Публичное demo-приложение.
- Synthetic replacement для существующих Harness self-tests.
- Benchmark suite общего назначения.
- Auto-merge release.
- Автоматическое изменение `main` canary во время qualification.
- Хранение credentials/secrets в репозитории.
- Копирование Schemor state.
- Специальные обходы validator/update contract ради зелёного CI.
- Blind sleep/retry для сокрытия race conditions.
- Chat history как источник истины.

## Референсы

### Release hardening

- Epic: https://github.com/ai-development-harness/ai-development-harness-template/issues/264
- Canary contract: https://github.com/ai-development-harness/ai-development-harness-template/issues/263
- Upgrade qualification: https://github.com/ai-development-harness/ai-development-harness-template/issues/261
- Release Qualification workflow: https://github.com/ai-development-harness/maintainer-tools/issues/7
- Publish hard gate: https://github.com/ai-development-harness/maintainer-tools/issues/8

### Escaped regressions, которые мотивировали canary

- Downstream/pre-INIT fixture drift: https://github.com/ai-development-harness/ai-development-harness-template/issues/254
- Synthetic Git cleanup race: https://github.com/ai-development-harness/ai-development-harness-template/issues/256

## Нефункциональные ожидания

### Reproducibility

Один и тот же baseline commit + candidate SHA должны приводить к одному deterministic qualification flow.

### Idempotence

Повторное применение уже применённого candidate должно давать корректный no-op / `NO_UPDATE`, а не дополнительную mutation.

### Observability

Каждый release-level gate должен оставлять понятный machine/human-readable результат с exact revisions.

### Isolation

Qualification работает с disposable copy. После failed run canonical canary repository остаётся неизменным.

### Maintainability

Canary должен быть небольшим. Его сложность должна происходить из накопленного валидного Harness state, а не из собственного приложения или большого количества custom scripts.

### Longevity

Project-owned state не следует регулярно «сбрасывать к template». Ценность canary растёт по мере того, как он проходит реальные обновления Harness.

## Решения, которые считаются заданными для PROJECT INIT

Инициализатор не должен превращать следующие положения в Open Questions без обнаруженного противоречия:

1. Canary остаётся private.
2. `main` хранит accepted stable baseline.
3. Candidate qualification работает на disposable copy и не push'ит candidate state.
4. Release orchestration принадлежит `maintainer-tools`, а не canary.
5. Harness qualification primitives принадлежат Harness core.
6. Canary должен накапливать валидный project-owned state между релизами.
7. Baseline продвигается только после выпуска/принятия нового стабильного Harness release.
8. Initial bootstrap выполняется на Harness release, уже находящемся в repository на момент PROJECT INIT.

Если для реализации этих решений требуется durable architecture rationale, создай ADR.

## Ожидания от initial roadmap

PROJECT INIT должен сформировать компактный roadmap, ориентировочно из нескольких STEP, а не большой продуктовый backlog.

После самого INIT ожидаются задачи уровня:

1. сформировать representative project-owned canary state штатными Harness workflows;
2. определить/проверить deterministic contract baseline advancement и canary preflight;
3. подготовить интерфейс использования canary внешним Release Qualification workflow без дублирования release orchestration.

Точный STEP decomposition должен следовать REQ/ADR и текущему Harness protocol.

## Неопределённости

Material uncertainty нужно оформлять OQ только если ответ действительно нужен для корректного roadmap/architecture.

Не требуется блокировать INIT вопросами о:

- UI;
- database;
- deployment;
- product runtime;
- пользовательской бизнес-логике,

поскольку они не относятся к назначению canary.

Если появится архитектурная неопределённость на границе canary ↔ maintainer-tools ↔ Harness core, предпочтительно зафиксировать ownership и interface contract, а реализацию внешнего repository оставить соответствующему issue.

## Дополнительные заметки

Canary специально должен вести себя как **обычный downstream Harness project**. Не добавляй в Harness core специальные ветки логики вида «если repository == release-canary».

Если canary требует специальной обработки, это сигнал проверить, является ли механизм общим release/update contract, а не canary-specific исключением.
