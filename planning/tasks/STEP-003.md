---
schema: 1
id: STEP-003
status: completed
type: documentation
priority: high
phase: canary-bootstrap
depends_on:
  - STEP-001
  - STEP-002
requirements:
  - REQ-003
  - REQ-004
  - REQ-005
  - REQ-006
  - REQ-007
  - REQ-008
  - REQ-009
  - REQ-011
  - REQ-012
adrs:
  - ADR-001
  - ADR-002
  - ADR-003
architecture_refs:
  - docs/architecture.md#ownership
  - docs/architecture.md#preservation-and-migration
  - docs/architecture.md#qualification-lifecycle
  - docs/architecture.md#security-boundaries
  - docs/architecture.md#compatibility-and-operations
risk_flags:
  - release-critical
  - external-integration
plan:
  status: ready
  revision: 1
  context_basis: sha256:778a0bd3fa082585bae7ee576f7f8402fb4c0407f2c30862b8bf98206517b03e
  content_hash: sha256:44fb9103305a7c07d29147f8214cb1bbdf15edf539c31c61b165507ec21ad26e
  reviewed_report: planning/plan-reviews/STEP-003/PLAN-REVIEW-20261007T093249Z.md
  planned_at: 2026-10-07T09:32:49+00:00
  execution_groups:
  context_components:
    - "ADR@ADR-001=sha256:7051cb5cc51b1ef418ed9dc52b207dc567a5b0aa18928111f36d1310e88f65cc"
    - "ADR@ADR-002=sha256:8d7e3c2ac25da6d759bf551d577fc327690e0f77ca8dd80823315efe627b44cc"
    - "ADR@ADR-003=sha256:739050183e5225e76c067ff076dcde089e17d7df32f04365bb633a75ada228d9"
    - "ARCH@docs/architecture.md#compatibility-and-operations=sha256:1082dc1397e504a684f2fc196ee6d2e2e8ba4c4ef217025090b894b87b3f9cf9"
    - "ARCH@docs/architecture.md#ownership=sha256:bbfc4b08f6f79828df2eace5c73541f57249896e2e4472787358de213902b41d"
    - "ARCH@docs/architecture.md#preservation-and-migration=sha256:feb228cf301013681755368b9bc33da4880b637dc09fd3b10d8a7674e0a5a821"
    - "ARCH@docs/architecture.md#qualification-lifecycle=sha256:6ce2f2708d84370c7d3fa6b4166136baa49440601ae7077ec528e1e59b0e0b49"
    - "ARCH@docs/architecture.md#security-boundaries=sha256:318bde5701fe0414477469e36844050dd4cfd5be6e3dc0c44e421ff102264c7a"
    - "REQ@REQ-003=sha256:bfa54ce5b092120005f24b0ed1474a1e39b54d4d811674c7ac682bef98b51ac6"
    - "REQ@REQ-004=sha256:c6575afc45c34211f69f2067639e036320198c5f59370d0ae03a20a55c7acc1c"
    - "REQ@REQ-005=sha256:60c1ef9d2498de7c2196db5a77c1c6e26e3bf302f72ae4ae486733c82a572c7e"
    - "REQ@REQ-006=sha256:c3a21412cbcb8ed91d643cf17a02306cb2bc6fa5ee29eb80115d573d97bcc778"
    - "REQ@REQ-007=sha256:fcb11bc49239c0ce51251c2d21ae8d7186e0983731b7a06ab3c98e86c9437365"
    - "REQ@REQ-008=sha256:1eb337ca2050d452bbf2e44a2aa108cc17f0bff2d0bcc796edbdfbb6c3ed4b9c"
    - "REQ@REQ-009=sha256:9e2f0a7ae6bf6aba1782464e270eda02f23fa734f9d95228b3ec7788d422ac2b"
    - "REQ@REQ-011=sha256:907e727eda98e468a0ce37c71ed363999bb76417188691a559d65d63d88f58c2"
    - "REQ@REQ-012=sha256:6337e108cbb3c5cd305eade249c773c7d3e9c35b59f409606dad40f2cb7dc1b6"
    - "STEP@STEP-001=sha256:7ed21ae346ee9f4a92b39d7907478e59f2e322cdbe864959d13f9381ebd9e09b"
    - "STEP@STEP-002=sha256:fcf0526e2fbc03158c0989a4132541046c9b33c1ff2e2c432af07246463e19b4"
    - "STEP@STEP-003=sha256:7a995f4bfedd21120a16995c0c3ec0b060f9c5d21bdf758ceb38636e590b6810"
---

# STEP-003 — Подготовить интерфейс внешней qualification

## Goal

Получить непротиворечивый canary consumer contract для external Release Qualification, с isolation/evidence и explicit integration prerequisites.

## Context

State STEP-001 и contract STEP-002 являются входами. Core #261 owns executable primitives, maintainer-tools #7/#8 — external workflow/Check/publish gate; их реализация не является mutation scope canary.

## Scope

- Описать semantic inputs/outputs baseline commit, source identities и exact candidate SHA, private access и ordered update flow.
- Определить evidence field meanings, aggregate failure/incomplete/stale semantics, tracked diff и preservation proof; concrete executable schema/entrypoint брать из core, когда доступны.
- Зафиксировать external owner/issues для private scoped checkout, core entrypoint, exact-SHA Check/publish, stress/Windows и cleanup.
- Подготовить непретендующие на реальные runs примеры success/failure/reload/migration/no-op; bounded proof сопоставляет docs с доступным installed protocol, без отдельного release engine.

## Mutation policy

### Allowed

- docs/canary-qualification.md и navigation links в project docs/README.
- Собственный STEP Evidence и штатные review artifacts; projections через tools.

### Conditional

- Уточнение examples после появления опубликованного shared core schema; не создавать competing machine schema.
- Ссылки на фактические external issues/contracts и evidence предоставленного caller run, если доступен, без изменения внешних repositories.

### Forbidden

- Изменение core/maintainer-tools или собственный reusable release workflow/engine в canary.
- Qualification в canonical checkout, candidate push/merge или изменение stable baseline.
- Credentials, выдуманная evidence/history, изменение Harness-owned tools и immutable reports.

## Out of scope

- Проверка App credentials, внешняя реализация Publish gate/Check, выпуск релиза, полная e2e qualification при отсутствии runner.

## Acceptance criteria

- Consumer contract связывает exact baseline/candidate identities, private read preflight, isolation и все ordered lifecycle gates.
- Evidence requirements включают stage/command/exit/stdout/stderr, reload/migration, preservation diff и repeated APPLY/NO_UPDATE; incomplete/stale evidence не даёт PASS.
- Success/failure/reload/migration examples явно помечены как contract examples, не реальные runs; неизвестный transition fail-closed.
- Реализация каждого external prerequisite имеет owner/issue; отсутствие core runner/App access отмечено честно, локальные docs не объявляются working release integration.
- Independent review подтверждает consistency с REQ/ADR, STEP-001 inventory и STEP-002 preflight; нет duplicating engine или main mutation.

## Verification

- command: `python3 .harness/tools/validate.py --mode manual`
- command: `python3 .harness/tools/traceability-coverage.py --json`
- command: `python3 .harness/tools/check-command-references.py --json`
- command: `git diff --exit-code 6de39722312a3ff554be81f562f5073a2ab2d0ac -- .harness .agents .codex .claude docs/adr planning/init-reviews planning/plan-reviews/STEP-001 planning/plan-reviews/STEP-002 planning/reviews/STEP-001 planning/reviews/STEP-002 docs/canary-state.md docs/canary-baseline.md planning/tasks/STEP-001.md planning/tasks/STEP-002.md`
- manual: Сопоставить consumer contract с REQ/ADR, STEP-001 inventory, STEP-002 preflight, installed UPDATES/EXECUTION_PROTOCOL и текущими external issues; подтвердить отсутствие опубликованного candidate-SHA интерфейса в проверенном installed contract и не выдавать документацию за e2e run.
- manual: Проверить contract examples success/failure/reload/migration/no-op и decision table missing-access, stale-SHA, skipped-gate, reload-required, migration-required, failure-before-cleanup; удостовериться в exact identities, fail-closed результате, сохранении canonical refs/state, preservation и cleanup после writers/evidence без credentials.

## Deliverables

- docs/canary-qualification.md: semantic inputs/outputs, lifecycle, evidence и ownership/prerequisite table.
- Independent contract review и bounded proof без external mutation.

## Implementation plan

### 1. Проверить актуальные inputs и external prerequisites

- Использовать baseline HEAD 6de39722312a3ff554be81f562f5073a2ab2d0ac с завершёнными STEP-001/002; исторический inventory bootstrap 50260bb не выдавать за snapshot нового baseline.
- Проверить installed Harness 0.11.2 lock/source ref v0.11.2 и tag-only updater contract; missing source SHA должен разрешаться доверенным core runner перед mutation.
- Прочитать actual GitHub issues core #260/#261/#262/#263/#264 и maintainer-tools #7/#8; назначить owners executable schema/entrypoint, arbitrary exact candidate update, scoped App checkout, Check/publish, stress/Python/Windows и cleanup. OPEN issue не доказывает отсутствия любого remote code, App-доступ не подтверждён пользовательским gh.

**Files:**
- docs/canary-qualification.md

**Risks:**
- Локальный installed tag-only APPLY не заменяет ещё не предоставленный shared core candidate-SHA interface.

### 2. Описать consumer lifecycle и достоверную evidence

- Создать semantic Markdown contract inputs/outputs без competing JSON schema/CLI и release engine.
- Упорядочить read/access preflight, isolated baseline checkout, exact candidate APPLY, настоящий runtime reload/repeat, migration/reconcile, STATUS/DOCTOR, validator/configured suite, preservation, повтор migration/no-op если применимо, repeat APPLY/NO_UPDATE, canonical isolation check, durable evidence и cleanup.
- Определить baseline/source/candidate identities, stage/command/exit/stdout/stderr, skipped/not-run, aggregate failed/incomplete/stale/unknown semantics, diff paths/modes/content/new/deleted files, допустимую migration и immutable history. Не обещать общей atomic rollback всех hops/reconcile.
- Развести read token и external Check/publish authority, credentials не включать в artifacts; завершение writers и сохранение diagnostics предшествуют cleanup.

**Files:**
- docs/canary-qualification.md

### 3. Добавить явно условные examples и навигацию

- Подготовить таблицу success/failure/reload/migration/no-op без вымышленных SHA, command exits и реальных run claims; failure-before-cleanup и unknown transition fail-closed.
- Добавить link в project-owned README block и docs/PROJECT.md; accepted architecture/ADR и dependency docs не менять.
- Записать реальные bounded observations protocol/help/issues как command/exit/observed facts, а не reconstructed terminal quotes; указать prerequisites будущей e2e integration.

**Files:**
- docs/canary-qualification.md
- README.md
- docs/PROJECT.md

### 4. Проверить contract и завершить independent review

- Сначала sync-projections, затем verify-step с четырьмя автоматическими checks и двумя semantic manual checks.
- Critical H1 protocol/dependency/immutable preservation доказать exact Git guard, H2 отсутствие устаревших команд подтвердить check-command-references; PLAN proof planned/INCONCLUSIVE, REVIEW требует fresh generated PASS на exact revision.
- Выполнить independent contract review и required specialized gates; writer закрывает STEP только при schema-valid PASS/type-specific proof. Не применять candidate, не делать commit/push/merge и external mutations.

**Files:**
- planning/tasks/STEP-003.md

**Tests:**
- validate/traceability/command-reference checks
- git diff --exit-code 6de39722312a3ff554be81f562f5073a2ab2d0ac -- .harness .agents .codex .claude docs/adr planning/init-reviews planning/plan-reviews/STEP-001 planning/plan-reviews/STEP-002 planning/reviews/STEP-001 planning/reviews/STEP-002 docs/canary-state.md docs/canary-baseline.md planning/tasks/STEP-001.md planning/tasks/STEP-002.md
- Manual contract consistency и decision table review

## Evidence

<!-- VERIFICATION-EVIDENCE:START -->
- Verification run: 2026-10-07T09:33:57Z
- Status: PASS
- Git head: 6de39722312a3ff554be81f562f5073a2ab2d0ac
- Worktree hash: sha256:68e0910e0f6c47203583ab88a9f3f331450d2563264ed1a6f7ae323916a23925
- Verification contract basis: sha256:dce657314b41f2fe7c16e90faf3c59a05ab3a6c3e251c30fc59821ef4e6d6755
- Subject git head: 6de39722312a3ff554be81f562f5073a2ab2d0ac
- Subject worktree hash: sha256:bbf88f32d6d929b654f787f939e5292642290316994eaad4323849d4ed6f4614

### Automated verification
- Command: python3 .harness/tools/validate.py --mode manual
  - Status: PASS
  - Exit code: 0
  - Duration ms: 1115
  - stdout sha256: 52c9b3e7b5e4a3303c9a2dee764b746ad102fe98e641dd9356b4036f3f7b512c
  - stderr sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - stdout bytes: 66
  - stderr bytes: 0
- Command: python3 .harness/tools/traceability-coverage.py --json
  - Status: PASS
  - Exit code: 0
  - Duration ms: 114
  - stdout sha256: 4e0cdadc8865b9e2804af9be95bd25980c24381a61dfa338428e91121e1d74aa
  - stderr sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - stdout bytes: 3115
  - stderr bytes: 0
- Command: python3 .harness/tools/check-command-references.py --json
  - Status: PASS
  - Exit code: 0
  - Duration ms: 114
  - stdout sha256: c9434e8073cf9e30263ab7425bc9ad84a91bbd7f2fd7986d3c03e75094c005a1
  - stderr sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - stdout bytes: 78
  - stderr bytes: 0
- Command: git diff --exit-code 6de39722312a3ff554be81f562f5073a2ab2d0ac -- .harness .agents .codex .claude docs/adr planning/init-reviews planning/plan-reviews/STEP-001 planning/plan-reviews/STEP-002 planning/reviews/STEP-001 planning/reviews/STEP-002 docs/canary-state.md docs/canary-baseline.md planning/tasks/STEP-001.md planning/tasks/STEP-002.md
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
- Check: Сопоставить consumer contract с REQ/ADR, STEP-001 inventory, STEP-002 preflight, installed UPDATES/EXECUTION_PROTOCOL и текущими external issues; подтвердить отсутствие опубликованного candidate-SHA интерфейса в проверенном installed contract и не выдавать документацию за e2e run.
  - Status: PASS
  - Observed: "Сопоставлены все 9 linked REQ, ADR-001/002/003 и 5 architecture refs, dependency inventory/bootstrap 50260bb и accepted baseline 6de3972. Contract различает source ref и missing exact SHA, installed tag-only updater и непредоставленный candidate primitive. UPDATES/EXECUTION_PROTOCOL и apply --help проверены без APPLY; actual gh issue view core 260/261/262/263/264 и maintainer-tools 7/8 завершились exit 0, issues OPEN. Owner/prerequisite table покрывает schema/runner, App read, Check/publish, stress/Python/Windows и cleanup. Ни App access, ни remote implementation readiness, ни e2e run не объявлены доказанными."
- Check: Проверить contract examples success/failure/reload/migration/no-op и decision table missing-access, stale-SHA, skipped-gate, reload-required, migration-required, failure-before-cleanup; удостовериться в exact identities, fail-closed результате, сохранении canonical refs/state, preservation и cleanup после writers/evidence без credentials.
  - Status: PASS
  - Observed: "Каждая строка таблицы явно contract example с symbolic inputs, без вымышленных SHA/exit/timestamp. Success требует real transition и repeat NO_UPDATE; missing-access/stale/skipped/unknown/failure запрещают aggregate PASS. Reload требует real runtime transition и repeat exact request; migration — reconcile/schema/preservation/repeat no-op. Canonical state/refs проверяются success и failure; partial hops не обещают общий rollback. Evidence хранится вне копии до cleanup, writers должны завершиться, cleanup error сохраняет неуспех. Credentials не включаются в repository/captured output. Фактический diff ограничен qualification doc, 2 navigation links, STEP003/projections и настоящим planning-review; candidate/source/core не мутированы."
<!-- VERIFICATION-EVIDENCE:END -->

INIT фиксирует только contract будущей работы. Команды, результаты и review evidence появятся при выполнении этого STEP; generated Verification evidence пишет deterministic runner.

## Blocker / Failure reason

—
