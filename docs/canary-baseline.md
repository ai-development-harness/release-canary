---
schema: 1
---
# Baseline: preflight и контролируемое продвижение

## Назначение и границы

Документ задаёт проверяемый contract для принятого canary baseline и его отдельного продвижения после публикации и принятия нового стабильного Harness release. Основания: [ADR-001](adr/ADR-001-stable-baseline-isolation.md), [ADR-002](adr/ADR-002-ownership-preservation.md), [ADR-003](adr/ADR-003-qualification-contract.md), REQ-001/003/005/006/007/008/009/010/012.

STEP-002 создаёт документацию и выполняет доступные read-only проверки. Описанные ниже APPLY, reload, migration, promotion и failure branches являются contract для будущего отдельного workflow; их выполнение этим документом не подтверждается. Общий executable qualification contract принадлежит core, orchestration и publish — maintainer-tools; расширенный consumer interface относится к STEP-003.

## Три разных состояния

1. **Accepted Git baseline.** Начальное опубликованное состояние `main` — commit `50260bbe6fd19f77ae25ac86b00f2404c1af3ff1`, bootstrap PR #1, Harness 0.11.2. [Inventory STEP-001](canary-state.md) содержит его before-state paths, ownership и hashes.
2. **Текущее рабочее состояние.** STEP-001 завершён штатно, но его inventory, customization и lifecycle reports ещё не зафиксированы отдельным Git workflow. Current working tree содержит эти изменения и документацию текущего STEP; они не представлены содержимым указанного bootstrap commit.
3. **Следующий опубликованный baseline.** После отдельного reviewed Git workflow accepted commit должен включать выбранный representative state. Его exact SHA и происхождение фиксирует тот workflow; будущую revision нельзя заранее подставить вместо текущего Git commit.

Запись выше фиксирует наблюдение при реализации STEP-002, а не автоматически обновляемый указатель на последний baseline. При последующем preflight identities читаются заново из выбранного Git commit, manifest/lock и evidence.

## Обязательные входы

| Вход | Смысл и проверка |
| --- | --- |
| Canary repository и baseline ref/commit | `ai-development-harness/release-canary`; разрешённый exact commit принятого stable `main`, доступный из Git |
| Baseline contents | Clean отдельный checkout выбранного commit, initialized project, inventory и сохранённая история; локальные pending changes не подмешиваются |
| Baseline Harness identity | Release, source repository/ref и разрешённый exact source SHA; manifest и lock согласованы |
| Target identity | Опубликованный stable release tag, source repository и разрешённый exact SHA; route допустим текущим update graph |
| Stable acceptance | Явное решение maintainer принять опубликованный release, связанное с release/tag/SHA; публикация сама не означает принятие |
| Required evidence | Результаты всех обязательных stages для этих exact inputs, preservation diff, no-op и independent review |

Текущий lock имеет `release=0.11.2`, source `ai-development-harness/ai-development-harness-template`, ref `v0.11.2`; exact source SHA в нём отсутствует. Перед реальной mutation доверенный runner/core разрешает ref до exact commit и сохраняет соответствие. Невозможность разрешения, moved tag, несовпадение identity или отсутствующая evidence блокируют дальнейшие действия. Canary docs не подменяют проверку source trust и не меняют lock вручную.

Установленный updater принимает trusted release tags, используя configured source и graph. Поддерживаемая canonical syntax:

```text
HARNESS UPDATE CHECK TO <tag>
HARNESS UPDATE APPLY TO <tag>
```

`<tag>` здесь означает опубликованный release tag, например форму `vX.Y.Z`, а не произвольный candidate SHA. Exact SHA сохраняется как проверенная identity; он не является выдуманным positional argument updater. Low-level tooling использует `--to <tag>` согласно [installed update contract](../.harness/docs/UPDATES.md); candidate qualification primitives реализует core. Эти UPDATE commands в STEP-002 не запускались.

## Local health и readiness

**Local health** проверяет доступность Python/Git/configuration, active schema/projections и Harness integrity текущего рабочего состояния. **Readiness для promotion** дополнительно требует clean выбранный accepted baseline, exact identities, опубликованный и явно принятый target, полные gates/evidence и независимый review. Никакой одиночный Doctor/validator PASS не разрешает merge.

Read-only preflight проводится в следующем порядке:

1. Выбрать accepted baseline commit и подтвердить его принадлежность stable Git history; получить отдельный clean checkout без local brief и chat memory. Сохранить Git identity и проверить dirty/untracked state.
2. Проверить configured manifest/lock: initialized project, installed release, source trust и exact identity. Pending schema, unresolved source или несовпадающая revision не считаются ready.
3. Проверить inventory выбранного baseline, immutable reports и Accepted ADR. Учитывать ownership: protocol/shared/marker/project files и отдельно updater lock. Не заменять active project hashes историческими hashes другого baseline.
4. Прочитать канонические `HARNESS STATUS` и `HARNESS DOCTOR`. Затем проверить validator, schema и command references; сохранить реальные результаты и limitations.
5. Проверить publication/acceptance target и допустимый update route. Private read-access проверяет внешний caller перед checkout; пользовательский `gh`-доступ не доказывает доступ release App.
6. Только при выполненных prerequisites перейти к отдельному promotion workflow. Required gates и review после update ещё должны состояться; preflight не является их заменой.

Производные файлы пересобираются явным `sync-projections.py` до Verification; мутирующая проверка не используется как evidence готовности. Применимые команды уже существуют:

```bash
python3 .harness/tools/validate.py --mode manual
python3 .harness/tools/migrate-project-schema.py --check --json
python3 .harness/tools/traceability-coverage.py --json
python3 .harness/tools/check-command-references.py --json
python3 .harness/tools/harness-ux.py doctor --json
```

### Реальные наблюдения STEP-002

Канонические read-only commands выполнены 2026-10-07 через dispatcher. Таблица содержит command, exit code и observed facts; текст summaries не является восстановленной terminal quote.

| Command | Exit code | Наблюдаемый результат |
| --- | ---: | --- |
| `HARNESS STATUS` | 0 | `result.status=PASS`; project initialized, Harness 0.11.2, Git branch main, `git.dirty=true` |
| `HARNESS DOCTOR` | 0 | `result.status=PASS`; required Python/Git/config/integrity/execution-state checks PASS; Python 3.12.3 |
| `python3 .harness/tools/harness-update.py apply --help` | 0 | Поддерживается `--to TARGET`; APPLY не выполнен |

Canonical local health прошёл. Полный promotion preflight этим результатом не пройден: working state ещё не опубликован, source SHA не разрешён, новый target/acceptance не предоставлены. Реальные Verification observations записывает [canonical STEP-002 Evidence](../planning/tasks/STEP-002.md); STATUS/DOCTOR stdout/stderr captured локально, durable summaries находятся здесь и в Evidence.

Отсутствие future target не препятствует завершению документационного STEP. Оно запрещает выдавать текущие проверки за e2e update, repeated APPLY/NO_UPDATE, release App test или full release qualification.

## Отдельный controlled promotion

Следующий flow выполняется только после публикации target и explicit stable acceptance, в отдельной рабочей ветке/копии accepted baseline. Для продвижения требуется отдельная авторизация canonical Git workflow; STEP-002 её не выполняет.

| Stage | Действие и условие перехода |
| --- | --- |
| Identity/access | Exact baseline/source/target SHA, publication/acceptance, trusted route и доступ подтверждены; входной baseline clean |
| APPLY | Штатный `HARNESS UPDATE APPLY TO <tag>` к выбранному опубликованному target; результат core не переопределяется reasoning |
| Reload | При `UPDATER_RELOAD_REQUIRED` действительно перезагрузить runtime, затем повторить exact APPLY; обычный retry без reload недостаточен |
| Migration | При project schema pending выполнить `PROJECT RECONCILE`, затем read-only schema check; не переписывать project-owned files updater-ом напрямую |
| Health/gates | STATUS/DOCTOR, validator, configured full self-tests и применимые core gates должны пройти; новые обязательные gates нельзя исключить |
| Preservation | Сверить paths/content и допустимые migration изменения; Accepted ADR и immutable reports сохраняются, необъяснённые потери запрещены |
| Idempotence | Повторный exact APPLY возвращает штатный `NO_UPDATE`; сравнение canonical tracked bytes не показывает новой mutation. Повторная migration, если требовалась, также no-op |
| Review | Независимый review полного diff и evidence для exact target; stale/неполный/отклонённый review не разрешает merge |
| Publication | Отдельный canonical Git workflow фиксирует reviewed state и явно продвигает main; candidate qualification не запускает этот этап автоматически |

Configured suite обязателен при реальном продвижении. Windows, minimum Python и stress gates остаются обязанностью core/release qualification; локальный Python 3.12.3 не доказывает их прохождение. Private access, Check и hard publish gate реализуются в maintainer-tools, не новым canary engine.

## Failure decision table

Таблица описывает **contract cases**, а не перечень реально выполненных failure experiments. Значения «остановить»/«ожидать»/«продолжить» — семантические решения, не новый competing machine result schema. Во всех незавершённых cases merge запрещён.

| Условие | Stage / решение | Обязательная evidence | Recovery и условие продолжения |
| --- | --- | --- | --- |
| Dirty baseline или unpublished representative state | Identity: остановить | Выбранный commit, tracked/untracked state и происхождение pending files | Отдельно review/фиксировать/публиковать state авторизованным Git workflow либо выбрать существующий clean accepted baseline; не скрывать изменения |
| Source/target SHA отсутствует или ref нельзя разрешить | Identity: остановить | Repository/ref, разрешение identity или явная ошибка | Разрешить trusted ref, сохранить exact SHA; не угадывать его по tag или chat |
| Tag moved, SHA не совпал, route недопустим | Identity/APPLY: остановить | Actual identities и core diagnostic | Разобрать source/graph conflict отдельным поддерживаемым workflow; не force/обходить trust gate |
| Target не опубликован или не принят stable | Acceptance: ожидать | Publication status и наличие/отсутствие решения maintainer для exact release/SHA | Дождаться обоих prerequisites; successful candidate qualification сама не даёт acceptance |
| Evidence относится к другому SHA | Любой gate/review: остановить | Expected/observed identities и stale evidence reference | Получить evidence для exact inputs; старый PASS не переносится на новый commit |
| Failed, skipped или incomplete mandatory gate | Gates: остановить | Command, exit/stdout/stderr и not-run stages | Исправить реальную причину в её scope и получить все required results; не blind retry до зелёного |
| APPLY возвращает `UPDATER_RELOAD_REQUIRED` | Reload: ожидать | Exact requested tag/SHA, completed hop, transition и runtime observation | Реальный reload, затем exact repeat APPLY; main ещё не меняется |
| Project schema migration pending | Migration: ожидать | Current release/schema и core pending result | Штатный PROJECT RECONCILE и schema check; не ручной rewrite templates/ADR |
| Migration failure | Migration: остановить | Preflight/I/O failure, фактический diff и remaining pending state | Сохранить diagnostics/working copy; использовать поддерживаемый recovery или новую копию accepted baseline, без обещания общей atomic migration |
| Неизвестный transition | Переход: остановить | Raw core result, last successful stage и next stages not-run | Проверить действующий core contract/prerequisite; не придумывать next action |
| Необъяснённая потеря/перезапись исторического state | Preservation: остановить | Before/after paths/hashes, migration evidence | Сохранить failure evidence и устранить причину; не переписывать immutable report/Accepted ADR для зелёного validator |
| Repeat APPLY/migration меняет canonical state либо нет `NO_UPDATE` | Idempotence: остановить | Exact command/result и before/after canonical diff | Разобрать незавершённый transition/defect в его owner; local journals не подменяют canonical no-op |
| Review отклонён, отсутствует или stale | Review: остановить | Exact reviewed revision, findings и required review status | Исправить в допустимом scope и получить matching independent PASS; main остаётся прежним |
| Git/publication gate отказал | Publication: остановить | Canonical Git result и actual refs/provider facts | Следовать exact Git recovery/preflight; не force/rebase/reset/merge вручную в обход gate |

## Граница rollback и сохранение main

Core updater обеспечивает транзакцию **отдельного hop**. Уже successful prior hops не откатываются автоматически вместе с последующим failure. PROJECT RECONCILE также не следует трактовать как часть общей транзакции всех update hops: предварительно обнаружимые blockers проверяются до записи, но I/O failure во время mutation не означает гарантированный полный rollback.

Неизменность accepted main обеспечивается работой в отдельной копии/ветке и запретом merge до полного PASS. При failure сохраняются exact identities, last successful stage, фактический diff и диагностика до cleanup; writers должны завершиться прежде удаления disposable state. Возобновление следует штатному core journal/recovery, либо создаётся новая копия saved accepted baseline. Destructive reset и скрытый rollback main не используются.

## Evidence и canonical no-op

Каждый stage сохраняет semantic fields: baseline/source/target repository/ref/SHA, release, command, exit code, stdout/stderr либо captured artifact reference, stage/result, reload/migration outcome, before/after tracked diff и явные not-run stages. Credentials и персональные данные не включаются. Format общей executable evidence schema определяет core; canary не создаёт второй release engine.

`NO_UPDATE` проверяется по actual core result и отсутствию новой canonical mutation. `.harness/local/**` journals/execution/transcripts учитываются отдельно и не обязаны совпадать byte-for-byte. Наличие нового local log не является canonical update; отсутствие tracked diff само по себе не подменяет обязательный `NO_UPDATE` result.

Изменившийся baseline/target commit делает прежнюю qualification/review evidence stale. Полный release PASS включает внешние gates и exact-SHA Check/publish contract; локальная документация и Doctor не подтверждают его.
