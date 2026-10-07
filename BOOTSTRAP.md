# Release Canary — первичный bootstrap

Эта инструкция нужна только до первого успешного `PROJECT INIT`.

## Подготовлено

В repository добавлен tracked brief:

```text
PROJECT_BRIEF.canary.md
```

Он описывает назначение release-canary и должен быть исходным входом первого PROJECT INIT.

## Что сделать локально

Работай в ветке:

```text
chore/bootstrap-release-canary
```

Создай штатный local brief:

```bash
cp PROJECT_BRIEF.canary.md PROJECT_BRIEF.local.md
```

`PROJECT_BRIEF.local.md` уже исключён из Git и коммитить его не нужно.

После этого открой repository в поддерживаемом runtime (Codex или Claude Code) и выполни:

```text
PROJECT INIT
```

Важно: не выставляй `.harness/manifest.yaml → project.initialized=true` вручную. INIT должен завершиться штатным `finalize-project-init.py` после deterministic и semantic gates.

## После PROJECT INIT

Проверь состояние:

```text
PROJECT STATUS
STEP NEXT
```

И дополнительно выполни deterministic checks:

```bash
python3 .harness/tools/validate.py --mode manual
python3 .harness/tools/run-self-tests.py
```

Затем закоммить **сгенерированные PROJECT INIT artifacts** в ту же ветку и push.

Draft PR bootstrap уже должен существовать; после push его diff будет содержать фактический initialized canary state.

## Что не делать

- не merge'ить bootstrap PR до успешного PROJECT INIT;
- не коммитить `PROJECT_BRIEF.local.md`;
- не переносить state из Schemor;
- не создавать fake historical reports вручную;
- не добавлять отдельный product application только ради реалистичности;
- не изменять Harness-owned files вручную, если это не часть штатного INIT.

После INIT дальнейшее representative project-owned state должно появляться отдельными STEP через normal Harness workflow.
