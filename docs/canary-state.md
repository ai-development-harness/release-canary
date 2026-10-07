---
schema: 1
---
# Накопленное состояние Release Canary

## Происхождение baseline

Исходное accepted bootstrap состояние — Git commit `50260bbe6fd19f77ae25ac86b00f2404c1af3ff1` из PR #1. Это **before-state STEP-001**, а не snapshot будущего candidate или итоговый commit текущего STEP.

Установленный Harness: `0.11.2`; source repository `ai-development-harness/ai-development-harness-template`, lock ref `v0.11.2`. Lock не содержит exact source SHA: source ref нельзя выдавать за уже разрешённый immutable commit. Разрешение источника относится к отдельному preflight/qualification contract STEP-002/003.

Snapshot включает все 381 tracked blob baseline, их Git mode, ownership и SHA-256 содержимого. Он вычислен из Git objects; текущие plan/evidence/review mutations не подменяют before-state. Приведены counts/digests всех групп и representative paths, включая всю immutable INIT history.

## Ownership inventory

| Группа baseline | Files | SHA-256 группы |
| --- | ---: | --- |
| Harness-owned protocol | 286 | `9f1bc6201219e66441d74f94561d7437b1a545160110edf0fc021cc196b9bf8b` |
| Shared files | 35 | `418cc71dac4e5d227bc7791d94650049c483f399a0482e59d048c013aaca94c0` |
| Marker-merge files | 2 | `3fcb2bb2ccac68c48f4b58f4c9d9b535f76f91223de1196984638d05124de8cb` |
| Updater state lock | 1 | `cdfb0c64edbdcbd9c72f603f5e3b315129f2e137f02958defea176669613cecf` |
| Project-owned artifacts | 57 | `a2e4e8e1f31269a9e6f859032d42d0c6419c9241de9c065464575717ff08a5dc` |

Классификация следует baseline `.harness/harness-update.toml`: `harness_owned`, затем `shared`, затем `marker_merge`; остальные tracked files — project-owned. Отдельно выделен `state.lock_file`, управляемый updater, хотя он не входит в `ownership.harness_owned`.

Group digest — SHA-256 UTF-8 строки, составленной для paths группы в лексикографическом порядке. Каждая запись содержит `path`, NUL, Git `mode`, NUL, hex SHA-256 содержимого, LF. Git object bytes хэшируются без изменения line endings. Этот digest — inventory snapshot, не executable release qualification schema и не обещание неизменности всех active project documents.

- Harness-owned protocol меняет только updater; STEP-001 сохраняет его bytes.
- Shared files обновляются с общей policy/3-way semantics; project settings не являются полностью protocol-owned.
- `AGENTS.md`/`README.md` имеют project-owned marked blocks внутри marker-merge files; STEP-001 их не меняет.
- Project-owned REQ/ADR/STEP/templates изменяются нормальными project workflows, migrations — PROJECT RECONCILE.
- Три INIT reports ниже — immutable subset project-owned history. Они остаются byte-for-byte неизменными; новые reports не заменяют старые.

## Конкретные baseline artifacts

Все значения таблицы относятся к исходному commit. Active STEP/projections позднее могут штатно меняться; immutable report или Accepted ADR нельзя переписывать для прохождения проверки.

| Path | Ownership | Baseline SHA-256 |
| --- | --- | --- |
| `.codex/config.toml` | Shared files | `a8970c2aa8ed1836468bb75c164db6a581792ddfc5e306d19f9834ffcc3a82f3` |
| `.github/workflows/harness-integrity.yml` | Shared files | `4903a0eba775fb039b200bbdeca2d6ced3a83b87e593c98e18c6aeded2e68d7e` |
| `.harness/docs/UPDATES.md` | Harness-owned protocol | `7297a54be286ddf92552b6a61717c76a55f0123909573fd5ed26462e00cd5d26` |
| `.harness/harness-policy.toml` | Harness-owned protocol | `17bd20ba6e36a610cba82c470966cb937cd5347e9134fea7e4d60a4ed06c6a29` |
| `.harness/harness-update.toml` | Harness-owned protocol | `f10fe6bf5ac1f9a078b83c4b59b3e155cfaa5836c47eda380e99a18375b46f4e` |
| `.harness/harness.lock.json` | Updater state lock | `20d78059907ae70cc59e1c8d3f90aac5dd4b6f944d6d622d522d1244426969ae` |
| `.harness/manifest.yaml` | Shared files | `14a88536794102867a32c34415a36df1401dbb88db415b6aa96b96cb2764f3c2` |
| `.harness/tools/self_test_fixture.py` | Harness-owned protocol | `4d4f1eda7eaf3561836f7e948955822a81ea40aed7bb4f0df9b93160ac3b2c52` |
| `.harness/tools/validate.py` | Harness-owned protocol | `6549adfed3a9f1d020bb0fe3b0b59129f530c5b18e1ceffa66a537cac7a2fcc2` |
| `AGENTS.md` | Marker-merge files | `59455aba2fc84a8fb6af97937c192af4beea066cf36b4b63104740a25cfc1b1e` |
| `BOOTSTRAP.md` | Project-owned artifacts | `c9169fc3e2332f8dab046da9e159d60c1c5546fcd856c8eab31fd6a2788dfc23` |
| `PROJECT_BRIEF.canary.md` | Project-owned artifacts | `c04a1347876865cddc3f765659fa2df1fd18b181eec4b6758234192a0351d09a` |
| `README.md` | Marker-merge files | `9c07b41ff8aff7ec6deb79215553d1bd9eec1f187284331ffbb0ba8d4bbbfefc` |
| `docs/PROJECT.md` | Project-owned artifacts | `12ea22ab9487469f390fb19d87ca5e057277e448ad9819bebd0ab800bd0bb88c` |
| `docs/adr/ADR-001-stable-baseline-isolation.md` | Project-owned artifacts | `ea4774f0fc7b7d92d9cae1db433b85795a033333818b4edbacb08cc9cd725687` |
| `docs/adr/ADR-002-ownership-preservation.md` | Project-owned artifacts | `5f697f72af33d0a0448e07a969be3a62a48f3b6e95637b7f3cfdcb8030f05c13` |
| `docs/adr/ADR-003-qualification-contract.md` | Project-owned artifacts | `16b3f3572cac8cea1db12174da531aea01c0e920faf50f67b03c7099780c3401` |
| `docs/architecture.md` | Project-owned artifacts | `4fbc5538512a68b469ffe8a8096a5e19725786b67efa9c4b567504035446ed09` |
| `docs/requirements/REQ-002-representative-state.md` | Project-owned artifacts | `303223c2063ea9b2ffa116f5b1329798a35d57904e4694c90fe3239f4cf0ab45` |
| `planning/init-reviews/INIT-REVIEW-20261007T074134Z.md` | Project-owned artifacts; immutable report | `5010e93c6a9b83fa4b9bf1c723853b7b7027b091c3c11adb537b9a7017059478` |
| `planning/init-reviews/INIT-REVIEW-20261007T074454Z.md` | Project-owned artifacts; immutable report | `e152a21ac9ff64b2a3291ad79a1f84764f2140ed82570b13d1a41cdf0a701ade` |
| `planning/init-reviews/INIT-REVIEW-20261007T074700Z.md` | Project-owned artifacts; immutable report | `908683825a9d42ff7655b6e5302ba954a4153781032a22194ad32313d2a39edf` |
| `planning/plan-reviews/TEMPLATE.md` | Project-owned artifacts | `606f24e72d28479ac6fceb50de2a4542a8a9d7a7d478199f62f3e51b79bb4c66` |
| `planning/reviews/TEMPLATE.md` | Project-owned artifacts | `1e91504d7c571b3b34a3bdf8d7e7a535306bbc75dd2cbec5c0fb5f6cdffc632b` |
| `planning/tasks/STEP-001.md` | Project-owned artifacts | `12f8025bccafb907380da317d1495bf693b5ea038992e41e687a7620d06e64a6` |
| `planning/tasks/STEP-002.md` | Project-owned artifacts | `8f8f3c46af6a1d47d825eae947ba43a6489c459a4706cead18b5e106f92d4bb4` |
| `planning/tasks/STEP-003.md` | Project-owned artifacts | `b7527d9201843d13bf45cbde57f644b45bb25e076a54cd12e76c17bef23331dc` |

## Project-owned customization

`planning/reviews/TEMPLATE.md` дополнен короткими prompts в `Scope checked` и `Verification observations`: проверять baseline/source identities, ownership и сохранность истории; различать реальные local gates и невыполненные external gates. Это рабочая подсказка для последующих canary reviews, а не выдуманная история или новый machine contract.

Frontmatter/schema/kind, обязательные headings, finding example и machine finding contract сохранены. Manifest/lock, Accepted ADR и INIT reports не меняются. Configuration искусственно не отклоняется от template; representative state получается полезной customization и реальным lifecycle STEP-001.

| Template state | SHA-256 |
| --- | --- |
| До STEP-001, Git baseline | `1e91504d7c571b3b34a3bdf8d7e7a535306bbc75dd2cbec5c0fb5f6cdffc632b` |
| После prose customization | `5a49ab336acdfb20e005211fb9fb2a4f840b5404a80b100260bc80d13da8d3f7` |

## Реальная история workflows

Исходные immutable reviews PROJECT INIT:

- [INIT-REVIEW-20261007T074134Z.md](../planning/init-reviews/INIT-REVIEW-20261007T074134Z.md)
- [INIT-REVIEW-20261007T074454Z.md](../planning/init-reviews/INIT-REVIEW-20261007T074454Z.md)
- [INIT-REVIEW-20261007T074700Z.md](../planning/init-reviews/INIT-REVIEW-20261007T074700Z.md)

Текущий workflow STEP-001 использует настоящий [Ready planning-review](../planning/plan-reviews/STEP-001/PLAN-REVIEW-20261007T081021Z.md), [canonical STEP с generated Evidence](../planning/tasks/STEP-001.md) и штатный каталог `planning/reviews/STEP-001/`. Implementation review и `completed` создаёт deterministic writer только после independent PASS и доказанного completion; inventory не создаёт reports задним числом и не заменяет результат review.

Остальные STEP остаются отдельными planned contracts. OQ/PRN не добавляются без реальной неопределённости или сквозного инженерного инварианта.

## Восстановление и проверки

Полный before-state восстанавливается из Git: clone repository с history, затем checkout exact commit `50260bbe6fd19f77ae25ac86b00f2404c1af3ff1` в отдельной копии. `git ls-tree -rz --full-tree <commit>` задаёт tracked paths/mode/blob OID, `git cat-file blob <OID>` — исходные bytes для hashes. Использовать ownership policy из того же commit.

После INIT не нужны local brief, chat transcript, внешняя БД и приватные локальные файлы. `.harness/local/**`, `PROJECT_BRIEF.local.md`, runtime transcripts и credentials не входят в baseline inventory; их содержимое не сохраняется и не хэшируется здесь. Они могут обслуживать текущий orchestration, но durable state и proof остаются Git artifacts.

Совместимость customized initialized state доказывают существующие validator/schema check и configured full self-tests; synthetic fixtures принадлежат core. Сохранность protocol/shared control plane, Accepted ADR и исходной INIT history проверяет explicit STEP Verification command:

```text
git diff --exit-code 50260bbe6fd19f77ae25ac86b00f2404c1af3ff1 -- .harness .agents .codex .claude docs/adr planning/init-reviews .github .gitignore .gitmessage AGENTS.local.example.md PROJECT_BRIEF.example.md README.md AGENTS.md
```

Git guard сравнивает tracked baseline bytes и не выдаётся за доказательство отсутствия любого нового untracked file; весь фактический implementation diff проверяется independent review. Inventory ownership/counts/path hashes и допустимость template prose дополнительно сверяются manual check из STEP Verification.

## Границы доказательства

STEP-001 не выполняет candidate upgrade, promotion main, private release App preflight, release engine или publish gate. Local Harness integrity/self-tests не равны full release qualification. Minimum Python 3.11 и Windows coverage остаются configured core CI gates; локальный Python 3.12.3 не является доказательством их выполнения. После завершения STEP отдельная Git-команда фиксирует и публикует accumulated state; commit не создаётся автоматически.
