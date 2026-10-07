---
schema: 1
---
# Интерфейс внешней Release Qualification

## Назначение и граница выполнения

Это consumer contract `release-canary` для внешнего runner: семантика входов, этапов, evidence и prerequisites. Основания: [ADR-001](adr/ADR-001-stable-baseline-isolation.md), [ADR-002](adr/ADR-002-ownership-preservation.md), [ADR-003](adr/ADR-003-qualification-contract.md), REQ-003/004/005/006/007/008/009/011/012. Входные документы — [ownership inventory STEP-001](canary-state.md) и [preflight/promotion STEP-002](canary-baseline.md).

STEP-003 проверяет согласованность документации с установленным Harness и внешними issues. Candidate APPLY, runtime reload, migration, private App access и e2e qualification здесь не выполнялись. Ниже описан обязательный будущий flow; таблицы примеров не являются отчётами о реальных runs.

Общий executable entrypoint и machine evidence schema определяет Harness core. Этот Markdown не вводит альтернативную JSON schema, CLI, workflow или release engine. Установленный Harness 0.11.2 поддерживает update к release tag; предоставленный локальный protocol не содержит подтверждённого интерфейса применения произвольного candidate SHA. Реальную integration нельзя объявлять работающей до предоставления core interface и caller runner.

## Входы и точная идентичность

| Семантический вход | Значение и обязательная проверка |
| --- | --- |
| Canary repository | Private `ai-development-harness/release-canary`; qualification имеет только read-доступ |
| Accepted baseline | Ref для provenance и exact commit принятой stable history; checkout содержит только выбранный commit, без pending/untracked local additions |
| Baseline Harness | Release, source repository, source ref и exact source commit, прочитанные из manifest/lock выбранного baseline и разрешённые доверенным core |
| Candidate Harness | Source repository, предполагаемый release, исходный ref и exact candidate commit; ref разрешается один раз до mutation, последующие gates связаны с этим SHA |
| Доступ | Scoped GitHub App token внешнего caller для чтения canary и нужного core source; наличие установки App и permissions проверяется до mutation |
| Core interface | Поддерживаемый exact-candidate entrypoint, schema/version evidence, update route/horizon и обязательные gates из core, без локального переопределения |
| Execution policy | Внешний disposable environment, допустимые runtime transitions, ограничения выполнения и cleanup по core/caller contract |

Baseline при начале STEP-003: `6de39722312a3ff554be81f562f5073a2ab2d0ac`, включающий completed STEP-001/002. Это наблюдение текущей работы, а не указатель, который runner должен постоянно hardcode-ить. После отдельной Git-фиксации STEP-003 caller выбирает accepted baseline заново. Inventory в `canary-state.md` описывает bootstrap commit `50260bbe6fd19f77ae25ac86b00f2404c1af3ff1`; его hashes не заменяют новый before-snapshot выбранного baseline.

На проверенном baseline manifest/lock имеют release `0.11.2`, source repository `ai-development-harness/ai-development-harness-template`, ref `v0.11.2`; `source.commit` отсутствует. Доверенный core runner должен разрешить этот ref до exact source SHA и сохранить соответствие. Missing revision, moved tag, недоступный commit, несовпадение manifest/lock или unsupported route блокируют mutation. Подстановка SHA по предположению или изменение lock вручную недопустимы.

Одинаковая связка baseline/source/candidate identities и core contract выбирает одинаковые обязательные gates. Изменение baseline, candidate SHA или применимого contract делает прежний результат непригодным для нового запуска. Проверка candidate не требует, чтобы candidate уже был опубликован или принят stable: publication и maintainer acceptance нужны отдельно для [baseline promotion](canary-baseline.md).

## Private access и изоляция

Внешний caller проверяет чтение обоих repositories и exact commits своим scoped App token до APPLY. Отсутствие установки App, permissions или доступа к commit даёт явный отказ; последующие gates обозначаются как незапущенные. Пользовательский authenticated `gh`-доступ, которым прочитаны issues, не доказывает release App access.

Qualification работает только в disposable checkout/worktree/copy выбранного baseline во внешнем environment. Если используется worktree, его Git metadata и refs не должны находиться в canonical canary checkout; caller обеспечивает независимую Git boundary. До выполнения сохраняется fingerprint canonical tracked paths/content и refs; после success и failure он сравнивается снова. Candidate state не переносится обратно, commit/push/merge и продвижение main не являются qualification stages.

Caller владеет credentials и разделением доступа к GitHub и execution candidate tooling. Token не помещается в repository, command arguments, captured stdout/stderr или durable evidence. Отдельные permissions для GitHub Check/publish принадлежат maintainer-tools и не дают qualification права писать в canary. Candidate code исполняется только в предназначенной для него disposable boundary; точные mechanics предоставляют core и внешний runner.

## Ordered lifecycle

| Порядок / stage | Обязательное действие и переход | Evidence |
| --- | --- | --- |
| 1. Identity/access preflight | Разрешить exact identities, проверить source trust/route, private scoped read и готовность core interface. При отсутствии prerequisite остановиться до APPLY | Expected/observed identities, access outcome без token, core contract/version, причина отказа |
| 2. Disposable baseline | Восстановить clean отдельную копию exact accepted commit; проверить initialized state, manifest/lock и ownership; снять before-snapshot и canonical isolation fingerprint | Baseline commit, paths/modes/content inventory, refs, clean/untracked state, provenance копии |
| 3. Candidate APPLY | Применить exact candidate штатным core primitive с update semantics. Arbitrary SHA не подставляется в tag-only installed updater | Exact request, ordered hops, actual core result, command/exit/stdout/stderr |
| 4. Reload, если требуется | При `UPDATER_RELOAD_REQUIRED` сохранить достигнутый hop и исходный target; реально перезагрузить runtime и повторить APPLY к тому же exact target. Повтор без reload не закрывает stage | До/после runtime observation, release/hop, transition и repeat result |
| 5. Migration, если требуется | При pending active project schema выполнить штатный `PROJECT RECONCILE`, затем schema check. Project-owned state не переписывается вручную или updater-ом | Pending state, RECONCILE result/report, actual changed paths и schema outcome |
| 6. STATUS/DOCTOR | После разрешения reload/migration выполнить `HARNESS STATUS` и `HARNESS DOCTOR` и проверить actual results | Отдельные результаты обоих commands; unresolved prerequisite не скрывается |
| 7. Validation/suite | Выполнить validator и полный configured discoverable self-test suite; все mandatory gates действующего core contract сохраняются | По каждому gate command/exit/stdout/stderr и результат; skipped gate не становится PASS |
| 8. Preservation | Сопоставить before/after paths, modes и content по ownership; объяснить каждую допустимую migration и сохранить immutable history/смысл Accepted ADR | Полный tracked diff, new/deleted paths, hashes, migration mapping и outcome |
| 9. Repeated migration, если применялась | Повторить штатную migration и доказать отсутствие новой canonical mutation и нового migration report без изменений | Repeat result, before/after canonical snapshot; local journals отдельно |
| 10. Repeated APPLY | Повторить APPLY того же exact candidate; нужен actual штатный `NO_UPDATE` и отсутствие новой canonical mutation | Повторный request/result, canonical bytes/paths/modes до/после |
| 11. Isolation/result | Проверить unchanged canonical canary tracked state и refs; собрать полный итог для exact inputs, перечислить failed/not-run stages | Isolation comparison, aggregate outcome и durable evidence reference |
| 12. Evidence/cleanup | Сохранить diagnostics вне удаляемой копии, дождаться завершения всех writers/processes и только затем удалить disposable state; записать cleanup outcome в сохранённую evidence | Durable evidence location, writers termination и cleanup result |

Применимые установленные команды: `HARNESS UPDATE APPLY TO <tag>`, `PROJECT RECONCILE`, `HARNESS STATUS`, `HARNESS DOCTOR`; локальные tooling checks — `python3 .harness/tools/validate.py --mode manual`, `python3 .harness/tools/migrate-project-schema.py --check --json`, `python3 .harness/tools/run-self-tests.py`. `<tag>` — release tag, а не SHA; точный способ qualification неопубликованного candidate должен предоставить core #261. Caller вызывает эти boundaries по актуальному executable interface, не создаёт обход через ручную замену tools/source policy. Full release entrypoint/core #260 дополнительно определяет CI validation, minimum/current Python и Windows gates.

Если primary APPLY сразу даёт `NO_UPDATE`, это отдельный no-op case, который не доказывает переход previous stable → нового candidate. Success upgrade требует реального первичного transition и последующего `NO_UPDATE`. Уже применённый candidate → тот же candidate относится к отдельному варианту core suite. Fresh project и поддерживаемый более старый migration horizon из core #261 также не подменяются одним canary run.

Неизвестный result/transition останавливает flow до проверки актуального core contract. Допустимая reload/migration branch является продолжением того же exact request, а blind retry/sleep до зелёного — нет. Failure на любом mandatory stage сохраняет диагностику и явные not-run результаты остальных gates. При bounded termination/cleanup error итог остаётся неуспешным; причина не подавляется.

## Сохранность, failure и recovery

Before-snapshot относится к выбранному baseline, включая review template customization, canonical REQ/ADR/STEP, completed history и immutable reports. Protocol/shared/marker/project paths и updater-owned lock разделяются по действующей ownership policy. Сравнение учитывает не только изменённые bytes, но и исчезнувшие/новые paths, mode changes и relevant untracked files; необъяснённое создание или потеря project state блокирует приёмку.

Разрешённые update и PROJECT RECONCILE mutations отражаются отдельно: paths, причина, migration report/pins и сохранение project prose/values по core contract. Исторические immutable reports сохраняются byte-for-byte; legacy pins используются только если действующая core migration требует их. Accepted ADR не переписываются для зелёного validator. Generated projections должны соответствовать canonical state после штатного reconcile.

Транзакция updater относится к отдельному hop. Success предыдущих hops может сохраниться после failure следующего; PROJECT RECONCILE не является общей atomic transaction вместе со всеми hops. Evidence фиксирует last successful stage, достигнутый release и фактический partial diff. Recovery следует core journal/protocol либо начинает новый run из сохранённого accepted baseline; предыдущий failed run не превращается в PASS после скрытого retry. Canonical main сохраняется изоляцией, а не обещанием полного rollback disposable state.

Для repeated APPLY/migration сравниваются canonical tracked paths/content/modes и соответствующая immutable history. `.harness/local/**`, execution journals и runtime logs учитываются отдельно, их изменение само по себе не нарушает canonical no-op. Пустой diff без actual `NO_UPDATE` недостаточен; `NO_UPDATE` с новой canonical mutation тоже недостаточен.

## Выходы и значение evidence

Это семантика полей, **не отдельная machine schema**. Имена/формат/version/entrypoint окончательно задаёт core; caller обязан валидировать artifact по общему contract, когда он предоставлен.

| Группа | Обязательный смысл |
| --- | --- |
| Provenance | Идентификатор конкретного run, применимый core/evidence contract, canary/baseline release/source identities, candidate repository/release/ref/exact SHA |
| Ordered stages | Порядок и stage, фактический command с безопасными аргументами, exit code, actual result и stdout/stderr или доступные captured artifact references |
| Branches | Выполненные hops, reload-required/runtime observation/repeat и migration pending/result/report/repeat; неприменимость branch объясняется |
| Coverage | Все mandatory gates и их статусы; not-run/skipped/incomplete явно отличаются от executed PASS; last successful stage и primary failure |
| Preservation/isolation | Before/after snapshots, tracked diff и path/mode/content comparisons, допустимые migration changes, immutable history proof и unchanged canonical state/refs |
| Idempotence | Exact repeated APPLY/actual `NO_UPDATE`, repeated migration при применимости и proof canonical no-op; local state отдельно |
| Aggregate/cleanup | Итог для exact inputs, ограничения и причины неуспеха, durable evidence location, завершение writers и cleanup outcome |

Captured output хранится до cleanup; summary сопровождается command, exit code и observed facts и не выдаётся за буквальный terminal quote. Отсутствующий stdout/stderr либо потерянный reference делает обязательную диагностику неполной. Credential-bearing вывод не публикуется; caller сохраняет безопасную диагностику без секретов и не замалчивает ограничение evidence.

Aggregate PASS возможен только для совпадающих exact inputs, когда все применимые обязательные gates реально завершены успешно, reload/migration resolved, preservation/isolation/no-op доказаны и evidence/cleanup завершены. Failed stage даёт неуспех; missing/skipped/incomplete/unknown outcome, malformed evidence, stale identities или cleanup failure запрещают PASS. Конкретные machine enums этих причин определяет core, а не этот Markdown.

Canary PASS является одним gate внешней Release Qualification. Он не означает full release PASS, successful Check, publish permission или принятие baseline. Maintainer-tools отдельно связывает Check с exact SHA, а publish после merge требует evidence именно exact merge SHA и mandatory Harness Integrity; результат для другого commit не переносится.

## Contract examples и таблица решений

**Все строки ниже — условные contract examples, не выполненные runs.** Используются символические «выбранный baseline» и «exact candidate»; реальные SHA, exit codes, timestamps и captured outputs runner заполняет только после выполнения.

| Case | Условный flow / результат | Необходимая evidence и завершение |
| --- | --- | --- |
| Success upgrade | Preflight → disposable exact baseline → реальный APPLY transition → health/validation/suite → preservation → repeated APPLY/`NO_UPDATE` → isolation → durable evidence/cleanup | Все exact identities и ordered gates; PASS возможен только после их выполнения, full release gates остаются внешними |
| Missing-access | Scoped App не может читать canary или core; отказ до APPLY, дальнейшие stages not-run | Безопасная access diagnostic, expected repository/commit и отсутствие qualification mutation; cleanup только созданных ресурсов |
| Stale-SHA | Result получен для другого baseline/candidate/contract | Expected/observed identities и stale reference; старый PASS не используется, нужен новый run |
| Skipped-gate | Один mandatory suite/gate не запущен либо его output потерян | Явный not-run/incomplete; aggregate PASS запрещён даже при прочих зелёных stages |
| Reload-required | APPLY достигает hop и возвращает `UPDATER_RELOAD_REQUIRED` → настоящий reload → repeat exact target → оставшиеся gates | Runtime transition и оба APPLY results; до reload/remainder run незавершён, простой retry не считается reload |
| Migration-required | Pending schema → `PROJECT RECONCILE` → schema/gates/preservation → повтор migration no-op → repeated APPLY | Migration report, объяснённый diff и no-op proof; conflict/failure останавливает run |
| No-op | Уже применённый exact candidate → APPLY/`NO_UPDATE` без canonical diff | Отдельный candidate→candidate case; не доказательство previous stable→candidate upgrade |
| Failure-before-cleanup | APPLY/gate падает, writers ещё активны или cleanup не может завершиться | Сначала сохранить primary failure/partial diff/not-run вне копии, bounded завершить writers; очистить только затем, cleanup failure сохранить и не выдавать PASS |
| Preservation failure | Исчез project path, изменён immutable report/ADR или repeat даёт canonical diff | Before/after path/hash evidence, неуспех; не чинить fixture вручную для зелёного результата |
| Unknown transition | Core result не распознан действующим interface | Raw безопасный result, last successful stage, not-run remainder; остановка до подтверждённого supported transition |

## External prerequisites и owners

Ссылки и статусы прочитаны через authenticated GitHub CLI 2026-10-07. Все перечисленные issues `OPEN`; это состояние issue, а не аудит всех удалённых branches/реализаций. Shared executable schema/runner не предоставлены проверенному installed contract; App access и caller e2e run не проверены. Отсутствие этих prerequisites запрещает объявлять working integration, но не препятствует документированию принятого consumer contract (ADR-003).

| Prerequisite / действие | Owner и issue | Что нужно подтвердить перед working integration |
| --- | --- | --- |
| Общий entrypoint и machine evidence contract; minimum/current Python, Windows и discoverable suite | Harness core [#260](https://github.com/ai-development-harness/ai-development-harness-template/issues/260), epic [#264](https://github.com/ai-development-harness/ai-development-harness-template/issues/264) | Опубликованный exact-candidate executable interface, валидируемая общая evidence schema и реальные обязательные compatibility results |
| Exact candidate upgrade из initialized stable, reload/reconcile/no-op, supported horizon и host isolation | Harness core [#261](https://github.com/ai-development-harness/ai-development-harness-template/issues/261) | Поддерживаемый primitive для unpublished SHA, preservation и repeated-APPLY proof, не обход tag-only updater |
| Canary baseline/state и consumer docs | release-canary / Harness core [#263](https://github.com/ai-development-harness/ai-development-harness-template/issues/263) | Accepted exact Git baseline с representative state; STEP-003 фиксируется только отдельным authorized Git workflow |
| Private scoped checkout/App access и вызов core runner | Maintainer-tools [#7](https://github.com/ai-development-harness/maintainer-tools/issues/7) | App installation/permissions и fail-fast read обоих repositories actual automation token; доступ пользователя не заменяет это |
| GitHub Check для exact SHA, диагностика и aggregate qualification | Maintainer-tools [#7](https://github.com/ai-development-harness/maintainer-tools/issues/7) | Реальный Check, полный набор core gates без duplication, failed/incomplete/stale не становятся success |
| Publish hard gate после merge | Maintainer-tools [#8](https://github.com/ai-development-harness/maintainer-tools/issues/8) | Exact merge SHA самостоятельно qualified, successful Check и mandatory Integrity; no stale reuse |
| Stress-sensitive execution и termination/cleanup primitives | Harness core [#262](https://github.com/ai-development-harness/ai-development-harness-template/issues/262), [#261](https://github.com/ai-development-harness/ai-development-harness-template/issues/261) | Bounded process/stress contract с сохранением intermittent failure и диагностикой, без blind retries |
| Disposable orchestration, durable artifacts и окончательный cleanup | Maintainer-tools [#7](https://github.com/ai-development-harness/maintainer-tools/issues/7), core primitives [#261](https://github.com/ai-development-harness/ai-development-harness-template/issues/261)/[#262](https://github.com/ai-development-harness/ai-development-harness-template/issues/262) | Evidence вне disposable copy, writers завершены до удаления; cleanup failure не подавлен |

## Bounded proof STEP-003

Реальные read-only наблюдения; значения ниже являются summaries, а не восстановленными terminal quotes.

| Выполненная команда / источник | Exit code | Наблюдение |
| --- | ---: | --- |
| `gh issue view <N> --repo ai-development-harness/ai-development-harness-template --json number,title,state,url,body`, N=260/261/262/263/264 | 0 для каждой | Прочитаны actual external contracts; issues OPEN; #263 подтверждает baseline `6de39722312a3ff554be81f562f5073a2ab2d0ac` с completed STEP-001/002 |
| `gh issue view <N> --repo ai-development-harness/maintainer-tools --json number,title,state,url,body`, N=7/8 | 0 для каждой | Private scoped App read, reusable qualification, exact-SHA Check и publish gate имеют внешнего owner |
| `python3 .harness/tools/harness-update.py apply --help` | 0 | `--to TARGET` и configured source/local mirror; help совместно с installed UPDATES описывает tag-target updater; APPLY не запускался |
| Installed [UPDATES](../.harness/docs/UPDATES.md) и [EXECUTION_PROTOCOL](../.harness/docs/EXECUTION_PROTOCOL.md) | чтение файлов | Reload/repeat, per-hop transaction, отдельный reconcile и documentation RUN согласованы с consumer contract |

[STEP-003 Evidence](../planning/tasks/STEP-003.md) содержит реальные generated verification результаты и manual observations; independent review — отдельный штатный immutable artifact. Эти проверки доказывают локальную contract consistency и сохранность разрешённого scope. Они не доказывают candidate upgrade, App access, Windows/minimum Python/stress, Check/publish или e2e внешнего runner. Для фактической qualification caller должен предоставить все inputs/interfaces и сохранить evidence описанных stages по shared core schema.
