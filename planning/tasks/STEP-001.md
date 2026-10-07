---
schema: 1
id: STEP-001
status: completed
type: implementation
priority: high
phase: canary-bootstrap
depends_on: []
requirements:
  - REQ-001
  - REQ-002
  - REQ-003
  - REQ-007
  - REQ-012
adrs:
  - ADR-001
  - ADR-002
architecture_refs:
  - docs/architecture.md#ownership
  - docs/architecture.md#baseline-state
  - docs/architecture.md#preservation-and-migration
  - docs/architecture.md#compatibility-and-operations
risk_flags:
  - release-critical
plan:
  status: ready
  revision: 1
  context_basis: sha256:c0ab8dfe602455ce52e54aeed16a84f683522a839fd263f93e1b28d242c3223a
  content_hash: sha256:a76f96a5d809bafa7d23a813a8d2c056a52243b33eb939806f6c862cff034906
  reviewed_report: planning/plan-reviews/STEP-001/PLAN-REVIEW-20261007T081021Z.md
  planned_at: 2026-10-07T08:10:21+00:00
  execution_groups:
  context_components:
    - "ADR@ADR-001=sha256:7051cb5cc51b1ef418ed9dc52b207dc567a5b0aa18928111f36d1310e88f65cc"
    - "ADR@ADR-002=sha256:8d7e3c2ac25da6d759bf551d577fc327690e0f77ca8dd80823315efe627b44cc"
    - "ARCH@docs/architecture.md#baseline-state=sha256:d0a365cccbc8c996dd8a591bcb5735c7d9878cf1182fb59fc8284e948954409f"
    - "ARCH@docs/architecture.md#compatibility-and-operations=sha256:1082dc1397e504a684f2fc196ee6d2e2e8ba4c4ef217025090b894b87b3f9cf9"
    - "ARCH@docs/architecture.md#ownership=sha256:bbfc4b08f6f79828df2eace5c73541f57249896e2e4472787358de213902b41d"
    - "ARCH@docs/architecture.md#preservation-and-migration=sha256:feb228cf301013681755368b9bc33da4880b637dc09fd3b10d8a7674e0a5a821"
    - "REQ@REQ-001=sha256:c01bcd92194d3c08b56debc16b338ce879dbca59eb25632e04a1d7d0cb99b829"
    - "REQ@REQ-002=sha256:ab5df3c50c2f05a51c5df77ab1529bc40bb822ea02c4f59765bbb01f20ca668c"
    - "REQ@REQ-003=sha256:bfa54ce5b092120005f24b0ed1474a1e39b54d4d811674c7ac682bef98b51ac6"
    - "REQ@REQ-007=sha256:fcb11bc49239c0ce51251c2d21ae8d7186e0983731b7a06ab3c98e86c9437365"
    - "REQ@REQ-012=sha256:6337e108cbb3c5cd305eade249c773c7d3e9c35b59f409606dad40f2cb7dc1b6"
    - "STEP@STEP-001=sha256:dd15f5e751157e712950b343211541cec1b0ab9da3a66f88071f072960985298"
---

# STEP-001 — Сформировать representative project-owned состояние

## Goal

Получить небольшой валидный downstream state с естественной историей workflows и допустимой project-owned customization.

## Context

INIT создал canonical REQ/ADR и реальные INIT reviews на Harness 0.11.2. У initialized template ещё нет representative post-INIT state, который должен переживать последующие releases (core #263).

## Scope

- Составить ownership inventory baseline: protocol-owned, project-owned, immutable reports и local operational state.
- Через normal Harness workflows выполнить допустимую customization project-owned template/config с пояснением реального назначения; выбранные fields/sections согласовать с установленным schema contract.
- Зафиксировать реальные planning/implementation/review lifecycle evidence этого STEP; сохранять исходные INIT reports.
- OQ/PRN добавлять только при реальном основании, без искусственной незавершённости ради fixture.

## Mutation policy

### Allowed

- Project-owned docs/ и planning/ внутри scope STEP, кроме immutable historical reports; шаблоны — только совместимая customization после INIT.
- Разрешённые generated project blocks README.md/AGENTS.md; projections только sync-projections.

### Conditional

- Project configuration в manifest — только обоснованная supported настройка; не менять project.initialized/name или Harness version.
- Новые OQ/PRN/REQ — только по подтверждённой необходимости и штатным workflows с обратными refs.

### Forbidden

- Harness-owned tools/protocol/runtime adapters, version lock и updater policy.
- Перезапись Accepted ADR/immutable reports, fake history, ручная порча fixture, копирование другого продукта.
- Candidate update, GitHub mutation и release orchestration.

## Out of scope

- Baseline advancement и release qualification integration; product runtime, БД и CI extensions.

## Acceptance criteria

- Inventory объясняет ownership и содержит конкретные paths/hash baseline artifacts.
- Есть schema-compatible project-owned template/config customization, отличающаяся от чистого template, и объяснение её назначения; нет выдуманных reports/OQ/PRN.
- Завершение этого STEP даёт естественный completion proof и independent review; исходная INIT history сохранена.
- Validator и configured self-tests проходят на initialized customized состоянии; результат не объявляется candidate qualification.

## Verification

- command: `python3 .harness/tools/validate.py --mode manual`
- command: `python3 .harness/tools/migrate-project-schema.py --check --json`
- command: `python3 .harness/tools/traceability-coverage.py --json`
- command: `python3 .harness/tools/check-command-references.py --json`
- command: `python3 .harness/tools/run-self-tests.py`
- command: `git diff --exit-code 50260bbe6fd19f77ae25ac86b00f2404c1af3ff1 -- .harness .agents .codex .claude docs/adr planning/init-reviews .github .gitignore .gitmessage AGENTS.local.example.md PROJECT_BRIEF.example.md README.md AGENTS.md`
- manual: Сверить inventory ownership/counts/path hashes и customization before/after с exact Git baseline; подтвердить сохранность INIT reports/Accepted ADR, реальность lifecycle refs и отсутствие unrelated mutations.

## Deliverables

- docs/canary-state.md: inventory, происхождение state и customization rationale.
- Допустимая project-owned customization и реальные PLAN/REVIEW/Evidence этого STEP.

## Implementation plan

### 1. Зафиксировать происхождение и ownership baseline

- Использовать exact accepted bootstrap commit 50260bbe6fd19f77ae25ac86b00f2404c1af3ff1 и установленный Harness 0.11.2/source ref v0.11.2. Не подменять tag точным source SHA, которого lock не содержит.
- По Git tree baseline и действующей ownership policy вычислить counts всех 381 tracked paths, SHA-256 group digest и конкретных representative artifacts; выделить updater-owned lock, shared paths, marker blocks, project-owned templates и immutable INIT reports.
- Документировать reproducible Git-based восстановление baseline без local brief/chat и exclusion ignored local operational state. Источник snapshot — Git objects, не transcript.

**Files:**
- docs/canary-state.md

**Risks:**
- Inventory фиксирует before-state, а не выдуманный future qualification run.

### 2. Добавить совместимую project-owned customization review template

- В planning/reviews/TEMPLATE.md дополнить только prose Scope checked и Verification observations краткими canary prompts: exact baseline/source identities, ownership inventory, preservation historical reports и границы выполненных gates.
- Сохранить frontmatter/kind/schema, обязательные headings и machine finding contract; existing Findings example не переписывать. Не менять core/protocol/manifest/lock.
- В docs/canary-state.md объяснить назначение customization и записать before/after SHA-256 template; не создавать fake OQ/PRN/reports или arbitrary configuration.

**Files:**
- planning/reviews/TEMPLATE.md
- docs/canary-state.md

**Tests:**
- Validator и full configured self-tests на initialized customized состоянии.

### 3. Сохранить реальную STEP history и проверить границы изменения

- Записать ссылки на immutable INIT reports и настоящий Ready planning-review, generated Verification evidence STEP-001 и штатный review directory; не утверждать PASS/Completed до writer completion.
- Проверить baseline SHA-256 immutable reports/Accepted ADR; exact Git diff guard подтверждает unchanged protocol/shared control plane и историю. Inventory/table сравнить с baseline Git tree; current diff должен включать только docs/canary-state.md, review TEMPLATE, текущий STEP/projections и штатные новые reports.
- Не применять release candidate, не делать GitHub mutation/Git commit и не реализовывать promotion/integration будущих STEP.

**Files:**
- docs/canary-state.md
- planning/tasks/STEP-001.md

**Tests:**
- git diff --exit-code 50260bbe6fd19f77ae25ac86b00f2404c1af3ff1 -- .harness .agents .codex .claude docs/adr planning/init-reviews .github .gitignore .gitmessage AGENTS.local.example.md PROJECT_BRIEF.example.md README.md AGENTS.md

### 4. Выполнить Verification и независимый review для completion

- Пересобрать projections до verification. Выполнить validator, schema check, traceability, command-reference check, все configured self-tests и exact baseline preservation guard через verify-step.
- Для critical H1 использовать fresh generated PASS run-self-tests.py, для critical H2 — fresh generated PASS exact Git diff command. На PLAN proofs planned/INCONCLUSIVE; на REVIEW необходимо proven/PASS по exact subject revision.
- Передать фактический diff и evidence независимому reviewer и всем required specialized reviewers; после PASS completion выполняет deterministic writer/dispatcher, без ручного completed status.

**Tests:**
- Независимый semantic inventory check и реальные generated Verification results.

## Evidence

<!-- VERIFICATION-EVIDENCE:START -->
- Verification run: 2026-10-07T08:13:05Z
- Status: PASS
- Git head: 50260bbe6fd19f77ae25ac86b00f2404c1af3ff1
- Worktree hash: sha256:bbfc8804fc16e1d6ab34666f7bbb0112064f3caab563a354eb363adc3fd4d4b6
- Verification contract basis: sha256:73a450d39d382b7ce176a35b679fefd18116d43f4cb4cd0e7e49d04ada1dff5b
- Subject git head: 50260bbe6fd19f77ae25ac86b00f2404c1af3ff1
- Subject worktree hash: sha256:0eece9bb8b141a4a8ae8661b9ffb3ca5441d2e773077ab777c16fbb0c67b9aba

### Automated verification
- Command: python3 .harness/tools/validate.py --mode manual
  - Status: PASS
  - Exit code: 0
  - Duration ms: 1015
  - stdout sha256: 5e3c42beae1058d52485d3529117ce013645860602a79359dc936f01b6c44207
  - stderr sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - stdout bytes: 66
  - stderr bytes: 0
- Command: python3 .harness/tools/migrate-project-schema.py --check --json
  - Status: PASS
  - Exit code: 0
  - Duration ms: 114
  - stdout sha256: 7e19d13781b0f820a5fdd57786a4778ea5cbaafe933923dea960779e3a199c07
  - stderr sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - stdout bytes: 52
  - stderr bytes: 0
- Command: python3 .harness/tools/traceability-coverage.py --json
  - Status: PASS
  - Exit code: 0
  - Duration ms: 113
  - stdout sha256: 925717df4e9e88184a8c4b5501570cc353af41860e2e0370c193302649380051
  - stderr sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - stdout bytes: 2968
  - stderr bytes: 0
- Command: python3 .harness/tools/check-command-references.py --json
  - Status: PASS
  - Exit code: 0
  - Duration ms: 113
  - stdout sha256: c9434e8073cf9e30263ab7425bc9ad84a91bbd7f2fd7986d3c03e75094c005a1
  - stderr sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - stdout bytes: 78
  - stderr bytes: 0
- Command: python3 .harness/tools/run-self-tests.py
  - Status: PASS
  - Exit code: 0
  - Duration ms: 61760
  - stdout sha256: fcb3e2d7b10f41daa97c8eb0441e9bd75f6630b094ff35d564a50f1d49f4e663
  - stderr sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - stdout bytes: 5046
  - stderr bytes: 0
- Command: git diff --exit-code 50260bbe6fd19f77ae25ac86b00f2404c1af3ff1 -- .harness .agents .codex .claude docs/adr planning/init-reviews .github .gitignore .gitmessage AGENTS.local.example.md PROJECT_BRIEF.example.md README.md AGENTS.md
  - Status: PASS
  - Exit code: 0
  - Duration ms: 7
  - stdout sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - stderr sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - stdout bytes: 0
  - stderr bytes: 0

### Product verification
- none

### Manual verification
- Check: Сверить inventory ownership/counts/path hashes и customization before/after с exact Git baseline; подтвердить сохранность INIT reports/Accepted ADR, реальность lifecycle refs и отсутствие unrelated mutations.
  - Status: PASS
  - Observed: "27 representative path hashes проверены по exact Git commit 50260bb; group counts относятся к его 381 tracked paths. Все 3 INIT reports и 3 Accepted ADR byte-identical. Template frontmatter/headings/Findings/machine contract совпадают, изменены только 2 prose sections; after hash соответствует текущим bytes. Actual diff включает только review template, current STEP/projections, canary-state doc и новый настоящий planning-review; unrelated files отсутствуют. Lifecycle docs ссылаются на существующий Ready report и не утверждают преждевременный implementation PASS."
<!-- VERIFICATION-EVIDENCE:END -->

INIT фиксирует только contract будущей работы. Команды, результаты и review evidence появятся при выполнении этого STEP; generated Verification evidence пишет deterministic runner.

## Blocker / Failure reason

—
