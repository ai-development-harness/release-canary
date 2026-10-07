---
schema: 1
id: STEP-002
status: completed
type: documentation
priority: high
phase: canary-bootstrap
depends_on:
  - STEP-001
requirements:
  - REQ-001
  - REQ-003
  - REQ-005
  - REQ-006
  - REQ-007
  - REQ-008
  - REQ-009
  - REQ-010
  - REQ-012
adrs:
  - ADR-001
  - ADR-002
  - ADR-003
architecture_refs:
  - docs/architecture.md#ownership
  - docs/architecture.md#baseline-state
  - docs/architecture.md#preservation-and-migration
  - docs/architecture.md#baseline-advancement-and-recovery
  - docs/architecture.md#qualification-lifecycle
  - docs/architecture.md#compatibility-and-operations
risk_flags:
  - release-critical
plan:
  status: ready
  revision: 1
  context_basis: sha256:c8146b51953d522c00cb4a6da4fc0899fddd9adc6422da229b36f4f58ddcc490
  content_hash: sha256:3c2dad5f604d240b3de166549bf740b444f84b37633d0588bfc4771368cc669b
  reviewed_report: planning/plan-reviews/STEP-002/PLAN-REVIEW-20261007T083142Z.md
  planned_at: 2026-10-07T08:31:42+00:00
  execution_groups:
  context_components:
    - "ADR@ADR-001=sha256:7051cb5cc51b1ef418ed9dc52b207dc567a5b0aa18928111f36d1310e88f65cc"
    - "ADR@ADR-002=sha256:8d7e3c2ac25da6d759bf551d577fc327690e0f77ca8dd80823315efe627b44cc"
    - "ADR@ADR-003=sha256:739050183e5225e76c067ff076dcde089e17d7df32f04365bb633a75ada228d9"
    - "ARCH@docs/architecture.md#baseline-advancement-and-recovery=sha256:beadf74233e500756378d9593ad43efb761048faca7a09adc0b17fd1c819c93c"
    - "ARCH@docs/architecture.md#baseline-state=sha256:d0a365cccbc8c996dd8a591bcb5735c7d9878cf1182fb59fc8284e948954409f"
    - "ARCH@docs/architecture.md#compatibility-and-operations=sha256:1082dc1397e504a684f2fc196ee6d2e2e8ba4c4ef217025090b894b87b3f9cf9"
    - "ARCH@docs/architecture.md#ownership=sha256:bbfc4b08f6f79828df2eace5c73541f57249896e2e4472787358de213902b41d"
    - "ARCH@docs/architecture.md#preservation-and-migration=sha256:feb228cf301013681755368b9bc33da4880b637dc09fd3b10d8a7674e0a5a821"
    - "ARCH@docs/architecture.md#qualification-lifecycle=sha256:6ce2f2708d84370c7d3fa6b4166136baa49440601ae7077ec528e1e59b0e0b49"
    - "REQ@REQ-001=sha256:c01bcd92194d3c08b56debc16b338ce879dbca59eb25632e04a1d7d0cb99b829"
    - "REQ@REQ-003=sha256:bfa54ce5b092120005f24b0ed1474a1e39b54d4d811674c7ac682bef98b51ac6"
    - "REQ@REQ-005=sha256:60c1ef9d2498de7c2196db5a77c1c6e26e3bf302f72ae4ae486733c82a572c7e"
    - "REQ@REQ-006=sha256:c3a21412cbcb8ed91d643cf17a02306cb2bc6fa5ee29eb80115d573d97bcc778"
    - "REQ@REQ-007=sha256:fcb11bc49239c0ce51251c2d21ae8d7186e0983731b7a06ab3c98e86c9437365"
    - "REQ@REQ-008=sha256:1eb337ca2050d452bbf2e44a2aa108cc17f0bff2d0bcc796edbdfbb6c3ed4b9c"
    - "REQ@REQ-009=sha256:9e2f0a7ae6bf6aba1782464e270eda02f23fa734f9d95228b3ec7788d422ac2b"
    - "REQ@REQ-010=sha256:abca9846e0563dc326d6620a6c6f6cb48a4731ec7f695908d7629827c3a4d876"
    - "REQ@REQ-012=sha256:6337e108cbb3c5cd305eade249c773c7d3e9c35b59f409606dad40f2cb7dc1b6"
    - "STEP@STEP-001=sha256:7ed21ae346ee9f4a92b39d7907478e59f2e322cdbe864959d13f9381ebd9e09b"
    - "STEP@STEP-002=sha256:4ec8002300960e523ce0c26973c136d4a099f16389e96f0243413ad531602f6a"
---

# STEP-002 — Определить preflight и продвижение stable baseline

## Goal

Получить проверяемый contract baseline preflight/promotion с bounded proof на фактическом representative state.

## Context

STEP-001 supplies inventory/customization и завершённую history. Main нельзя автоматически продвигать после candidate PASS; release publication и принятие maintainer — отдельные prerequisites.

## Scope

- Описать preflight: exact baseline commit, manifest/lock/source identities, initialized state, schema/projections, ownership inventory, STATUS/DOCTOR и gates.
- Описать controlled promotion опубликованного/принятого stable release: рабочая ветка, APPLY, reload/reconcile, validation/self-tests, review diff и отдельно authorized canonical Git merge.
- Описать failure/recovery, повторный APPLY/NO_UPDATE и различие local journal/canonical no-op.
- Проверить доступные read-only preflight commands на текущем baseline и decision table для missing revision/failed gate/unpublished release; не применять неизвестный future release.

## Mutation policy

### Allowed

- docs/canary-baseline.md, docs/development.md, relevant project navigation blocks.
- Собственный STEP Evidence и штатные review artifacts; projections через deterministic tools.

### Conditional

- Небольшие consumer examples в docs/ без executable release engine, если они проясняют поля evidence.
- Исправление task-local contract этого STEP через supported planning workflow; Accepted ADR не переписываются.

### Forbidden

- Promotion main, реальный candidate APPLY или GitHub mutation в рамках подготовки contract.
- Changes core/maintainer-tools, Harness-owned files, immutable reports и результат STEP-001.
- Обход update graph/migration gates и произвольный destructive rollback.

## Out of scope

- Выпуск или продвижение нового release, настройка external App, reusable workflow/publish gate, full cross-platform qualification.

## Acceptance criteria

- Preflight описывает exact identities и проверяемую принадлежность stable baseline; фактически доступные команды проверены на state STEP-001.
- Promotion требует published release и явное stable acceptance; failed gate/review оставляет main прежним.
- Contract покрывает reload-required, migration-required, unknown transition, preservation inventory и canonical idempotence.
- Для каждой failure branch указан stage/result/evidence/recovery; отсутствие future candidate не заменяется выдуманным e2e PASS.
- Target release/SHA и Git publication остаются отдельным explicit workflow; schema/current и command references валидны.

## Verification

- command: `python3 .harness/tools/validate.py --mode manual`
- command: `python3 .harness/tools/migrate-project-schema.py --check --json`
- command: `python3 .harness/tools/traceability-coverage.py --json`
- command: `python3 .harness/tools/check-command-references.py --json`
- command: `python3 .harness/tools/harness-ux.py doctor --json`
- command: `git diff --exit-code 50260bbe6fd19f77ae25ac86b00f2404c1af3ff1 -- .harness .agents .codex .claude .github .gitignore .gitmessage docs/adr planning/init-reviews`
- manual: Прочитать фактические HARNESS STATUS/DOCTOR через canonical dispatcher и сохранить command/exit/result; отдельно отметить dirty/unpublished/source-ref-only readiness без candidate mutation и без promotion PASS.
- manual: Семантически проверить decision table и failure/recovery: dirty/unpublished/missing SHA/unaccepted release/stale evidence/failed или skipped gate/reload/migration/unknown transition/preservation gap/rejected review не разрешают merge; contract examples отделены от actual runs.
- manual: Сравнить before/after результат STEP-001 (inventory/template/task/immutable reports), соответствие docs actual supported tooling, отсутствие UPDATE APPLY/GitHub/core mutation и unrelated changes.

## Deliverables

- docs/canary-baseline.md: preflight, promotion и failure/recovery contract.
- Evidence реальных read-only checks и independent review документа.

## Implementation plan

### 1. Разделить baseline identities, рабочее состояние и promotion readiness

- Создать docs/canary-baseline.md со ссылкой на inventory STEP-001 и provenance accepted bootstrap Git commit50260bb. Отделить точный baseline commit от Harness source ref/revision и будущего target release/SHA.
- Зафиксировать обязательные inputs: canary repository/ref/exact baseline commit, installed release/lock source identity, target published release и разрешённый SHA, explicit maintainer stable acceptance, ownership inventory и required gate evidence. Source tag без SHA не считать immutable revision до разрешения.
- Объяснить, что completed STEP-001 сейчас находится в незакоммиченном working tree: health PASS не делает это accepted/published representative baseline. До реального promotion отдельный Git workflow публикует и выбирает exact clean stable baseline; текущий documentation STEP этого не делает.
- Current installed updater использует trusted release tags/graph. Не добавлять выдуманный candidate-SHA flag/API, competing machine schema или release engine.

**Files:**
- docs/canary-baseline.md

**Risks:**
- Без exact identity и pristine выбранного baseline promotion не разрешён, даже если local validator/Doctor PASS.

### 2. Описать и проверить read-only preflight и decision table

- Описать preflight по этапам: Git identity/clean state, initialized manifest+source lock, schema/projections/inventory, canonical HARNESS STATUS/DOCTOR, validator и existing gates. Actual read-only commands доступны на representative working state; их result отделён от полного baseline readiness.
- При реализации прочитать HARNESS STATUS/DOCTOR через canonical dispatcher и сохранить command/exit/result/evidence. Записать фактический dirty/unpublished/source-ref-only state без claimed promotion PASS и без рассуждений о неисполненном future target.
- Создать semantic decision table с cases: dirty или unpublished state, missing/unresolvable SHA, unpublished/unaccepted release, stale evidence, failed/skipped gate, reload-required, migration-required/failed, unknown transition, preservation failure и rejected review. Для каждого case определить stage/result/evidence/recovery и prohibition merge.
- Случаи, которые не выполнены реально, явно обозначить contract examples. Manual review проверяет решения, executable Doctor/validator/refs проверяют только доступный local tooling; они не выдают e2e proof отрицательных future update branches.

**Files:**
- docs/canary-baseline.md

**Tests:**
- python3 .harness/tools/harness-ux.py doctor --json
- Semantic manual decision table review + actual canonical STATUS/DOCTOR observations.

### 3. Описать controlled promotion, failure recovery и no-op contract

- Описать отдельный будущий workflow после published release и explicit stable acceptance: рабочая ветка/копия accepted baseline → штатный APPLY exact published tag/SHA → explicit runtime reload/repeat при UPDATER_RELOAD_REQUIRED → PROJECT RECONCILE при pending migration → STATUS/DOCTOR/validate/configured suite → preservation diff → repeated APPLY/NO_UPDATE и повторная migration/no-op при необходимости → independent review → separately authorized canonical Git workflow/merge.
- Для каждого этапа сохранять exact baseline/source/target identities, command/exit/stdout/stderr, reload/migration outcome, tracked diff и not-run stages. Evidence schema/qualification engine оставляются core; canary задаёт semantic contract и объяснения.
- Failure, unknown transition, failed review или preservation gap сохраняет прежний main и evidence; recovery начинает с saved accepted baseline в отдельной копии/ветке без destructive reset, скрытого rollback main, blind retries или suppression. Before/after canonical comparison отделить от local execution journals.
- Уточнить границу rollback: core гарантирует rollback отдельного updater hop, а не общую транзакцию всех successful hops и PROJECT RECONCILE. Previous successful hops остаются в изолированной рабочей копии; RECONCILE failure не обещает полный rollback bytes. Неизменность main обеспечивается изоляцией и отдельным merge gate.
- Документировать private access/external owner boundaries без настройки release App/CI/Check/publish. STEP-003 владеет расширенным qualification consumer interface; STEP-002 не дублирует этот engine и не требует его для локального documentation completion.

**Files:**
- docs/canary-baseline.md

**Risks:**
- Никакие mutating команды из будущего promotion flow не выполняются внутри этого documentation STEP.

### 4. Обновить навигацию и собрать bounded completion evidence

- Добавить в docs/development.md ссылку на baseline contract, существующие read-only diagnostics и различие health/readiness. Navigation изменять только при необходимости в разрешённых project blocks; не переписывать architecture/REQ/Accepted ADR.
- Preserve исходный STEP-001 inventory/template/immutable reports и core/shared config; сравнить их bytes до/после текущего STEP. Пересобрать projections до canonical Verification.
- Выполнить validator/schema/traceability/command refs/Doctor и protected baseline diff guard; full suite не повторять для prose-only docs без выявленного regression. Manual observations подтверждают actual canonical STATUS/DOCTOR и все branch decisions.
- Required blast H1/Doctor и H2/protected baseline guard на PLAN planned/INCONCLUSIVE, а на REVIEW имеют fresh generated PASS/proven; semantic false-positive readiness и unreachable future branches проверяет независимый review documentation.

**Files:**
- docs/development.md
- docs/canary-baseline.md

**Tests:**
- git diff --exit-code 50260bbe6fd19f77ae25ac86b00f2404c1af3ff1 -- .harness .agents .codex .claude .github .gitignore .gitmessage docs/adr planning/init-reviews

## Evidence

<!-- VERIFICATION-EVIDENCE:START -->
- Verification run: 2026-10-07T08:40:07Z
- Status: PASS
- Git head: 50260bbe6fd19f77ae25ac86b00f2404c1af3ff1
- Worktree hash: sha256:114faf16b3782c9075396bd8ef61e6269d95704255c20cad83764564bf6fc803
- Verification contract basis: sha256:ad4de98d5cc02f4bdbddbe5ea18fa467861f4d442106765b5139840684bbb574
- Subject git head: 50260bbe6fd19f77ae25ac86b00f2404c1af3ff1
- Subject worktree hash: sha256:241607335727f3ce29e5973534c86c7301ed40a2359d5d24c078d4c5a0632993

### Automated verification
- Command: python3 .harness/tools/validate.py --mode manual
  - Status: PASS
  - Exit code: 0
  - Duration ms: 1065
  - stdout sha256: 5e3c42beae1058d52485d3529117ce013645860602a79359dc936f01b6c44207
  - stderr sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - stdout bytes: 66
  - stderr bytes: 0
- Command: python3 .harness/tools/migrate-project-schema.py --check --json
  - Status: PASS
  - Exit code: 0
  - Duration ms: 113
  - stdout sha256: 7e19d13781b0f820a5fdd57786a4778ea5cbaafe933923dea960779e3a199c07
  - stderr sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - stdout bytes: 52
  - stderr bytes: 0
- Command: python3 .harness/tools/traceability-coverage.py --json
  - Status: PASS
  - Exit code: 0
  - Duration ms: 113
  - stdout sha256: 12c858de159aa913e032f366353465dfda68ed0346d2e7c8abe3700a2f3abfa4
  - stderr sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - stdout bytes: 3019
  - stderr bytes: 0
- Command: python3 .harness/tools/check-command-references.py --json
  - Status: PASS
  - Exit code: 0
  - Duration ms: 114
  - stdout sha256: c9434e8073cf9e30263ab7425bc9ad84a91bbd7f2fd7986d3c03e75094c005a1
  - stderr sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - stdout bytes: 78
  - stderr bytes: 0
- Command: python3 .harness/tools/harness-ux.py doctor --json
  - Status: PASS
  - Exit code: 0
  - Duration ms: 1666
  - stdout sha256: 64538717b7eb5527b36f1acdb127291368b698495e61816e8db373f8c11b5d8c
  - stderr sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - stdout bytes: 1672
  - stderr bytes: 0
- Command: git diff --exit-code 50260bbe6fd19f77ae25ac86b00f2404c1af3ff1 -- .harness .agents .codex .claude .github .gitignore .gitmessage docs/adr planning/init-reviews
  - Status: PASS
  - Exit code: 0
  - Duration ms: 3
  - stdout sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - stderr sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - stdout bytes: 0
  - stderr bytes: 0

### Product verification
- none

### Manual verification
- Check: Прочитать фактические HARNESS STATUS/DOCTOR через canonical dispatcher и сохранить command/exit/result; отдельно отметить dirty/unpublished/source-ref-only readiness без candidate mutation и без promotion PASS.
  - Status: PASS
  - Observed: "Канонические HARNESS STATUS и HARNESS DOCTOR выполнены через dispatcher: exit 0, DONE, result PASS; STATUS git.dirty=true, initialized=true, release 0.11.2. Doctor все required checks PASS. Captured stdout/stderr .harness/local/step-002/canonical-status/doctor.stdout/.stderr; durable summaries docs/canary-baseline.md. Полный promotion readiness не объявлен: representative state не опубликован, lock без exact source SHA, target/acceptance отсутствуют; APPLY не запускался."
- Check: Семантически проверить decision table и failure/recovery: dirty/unpublished/missing SHA/unaccepted release/stale evidence/failed или skipped gate/reload/migration/unknown transition/preservation gap/rejected review не разрешают merge; contract examples отделены от actual runs.
  - Status: PASS
  - Observed: "Семантически проверены все 14 contract cases и поля stage/result/evidence/recovery. Dirty/unpublished/missing SHA/unaccepted/stale/failed/skipped/unknown/preservation/rejected-review cases запрещают merge; reload и pending migration требуют явного lifecycle до дальнейших gates. Таблица и future promotion явно являются contract examples, не actual failure experiments/e2e PASS. Rollback ограничен hop, main сохранён изоляцией."
- Check: Сравнить before/after результат STEP-001 (inventory/template/task/immutable reports), соответствие docs actual supported tooling, отсутствие UPDATE APPLY/GitHub/core mutation и unrelated changes.
  - Status: PASS
  - Observed: "Before/after SHA-256 всех protected existing artifacts совпадают, включая inventory/template/task и отчёты STEP-001, INIT history/Accepted ADR/core/config. HEAD и main ref прежние. Новые files ограничены docs/canary-baseline.md; существующие changes этого STEP только development/task2/generated projections. Подтверждены installed --to tag syntax и отсутствие UPDATE APPLY, candidate/GitHub/promotion/unrelated mutations."
<!-- VERIFICATION-EVIDENCE:END -->

INIT фиксирует только contract будущей работы. Команды, результаты и review evidence появятся при выполнении этого STEP; generated Verification evidence пишет deterministic runner.

## Blocker / Failure reason

—
