---
schema: 1
---
# Development

## Prerequisites

Git и Python 3.11+ согласно Harness dependencies. Локальный INIT выполнен Python 3.12.3; minimum-version и Windows jobs определены в baseline Harness Integrity, локальный PASS не доказывает их выполнение. Codex или Claude Code — для semantic workflows. GitHub CLI нужен только для поддерживаемой GitHub integration; credentials не хранятся в project state.

## Local setup

Использовать clone exact baseline commit. После INIT восстановление не требует PROJECT_BRIEF.local.md или chat history. Bootstrap инструкция сохранена в BOOTSTRAP.md как исторический вход; повторный INIT не требуется. Не выполнять candidate APPLY в canonical checkout во время qualification.

## Development commands

```text
PROJECT STATUS
STEP NEXT
HARNESS STATUS
HARNESS DOCTOR
```

STEP-001 формирует representative state; STEP-002 — preflight/promotion contract; STEP-003 — consumer interface external qualification. Plan и independent review обязательны до mutation соответствующего STEP.

См. [inventory и происхождение STEP-001](canary-state.md) и [baseline preflight/promotion contract](canary-baseline.md). Local health PASS проверяет tooling/integrity рабочего состояния; promotion дополнительно требует clean accepted baseline, exact source/target identities, published/accepted stable release и полного review/gates. Pending project changes не становятся опубликованным baseline без отдельного canonical Git workflow.

## Testing

Существующие deterministic команды:

```bash
python3 .harness/tools/sync-projections.py
python3 .harness/tools/validate.py --mode manual
python3 .harness/tools/migrate-project-schema.py --check --json
python3 .harness/tools/traceability-coverage.py --json
python3 .harness/tools/check-command-references.py --json
python3 .harness/tools/harness-ux.py doctor --json
python3 .harness/tools/run-self-tests.py
```

sync-projections выполняется перед проверкой, поскольку это явная mutation projections; validate не заменяет semantic review. Self-tests используют временные fixtures; не объявлять их PASS доказательством уже реализованной external candidate qualification.

## Lint / formatting / type checking

Отдельного product lint/typecheck/formatter нет. Structural Markdown/YAML contract и projections проверяет Harness validator.

## Build

Product build отсутствует: проект состоит из Git state, core Python tooling и текстовых артефактов.

## Environment / configuration

Paths и language задаёт .harness/manifest.yaml, version/source — manifest и .harness/harness.lock.json, ownership/source policy — .harness/harness-update.toml. Private release App access подтверждает внешний caller, пользовательский gh-доступ не заменяет его preflight.

## Database / migrations

БД нет. Project document schema migrations выполняются PROJECT RECONCILE по core protocol, с сохранением Accepted ADR и immutable history. Update reload transition требует штатного reload/repeat APPLY.

## CI/CD

Существующий .github/workflows/harness-integrity.yml проверяет core validator/self-tests, Python minimum и Windows boundaries. Собственного CI/release engine INIT не создаёт. Release qualification, scoped private checkout и exact-SHA Check/publish gate принадлежат внешнему maintainer-tools.

## Git и CI

Git workflow задают .harness/docs/GIT_WORKFLOW.md и .harness/git-policy.toml. Commit/push/PR выполняются только по отдельной авторизованной canonical Git command; PROJECT INIT их не запускает. main продвигается отдельно после published/accepted stable release и review diff.
