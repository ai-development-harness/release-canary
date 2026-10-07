---
schema: 1
---
# Architecture

## System context

Release Canary — обычный private initialized downstream Git repository. Maintainer-tools читает accepted baseline, core supplies qualification primitives; candidate проверяется в disposable copy. Никакого product runtime, API server, queue или внешней БД нет.

## Ownership

| Область | Owner | Граница |
| --- | --- | --- |
| Canonical project state и consumer docs | release-canary | Normal Harness workflows; без release engine |
| Protocol layer, updater, migration, общие qualification primitives | Harness core | Общий contract без специальных canary исключений |
| Checkout credentials, release orchestration, Check/publish hard gate | maintainer-tools | Отдельные #7/#8; qualification не меняет baseline |
| Принятие stable baseline | Maintainer | Отдельный reviewed promotion после publication |

## Baseline state

main хранит accepted stable baseline (ADR-001). Initial protocol: manifest/lock release 0.11.2, source v0.11.2; точный source SHA разрешает qualification runner. Начальный baseline commit фиксируется отдельным Git workflow после INIT. REQ/ADR/STEP являются canonical; PLAN/STATUS/SPEC/OQ index — projections. INIT review reports — реальная первая история. STEP-001 затем добавляет representative state/customization через поддерживаемые workflows, не создавая fake reports/OQ/PRN.

## Preservation and migration

Ownership inventory и сравнение bytes/paths доказывают сохранность project-owned state (ADR-002). Updater меняет protocol layer; schema pending требует PROJECT RECONCILE. Migration сохраняет Accepted ADR и immutable reports по core contract. Повторная migration и APPLY — canonical no-op. Local journals не равны canonical state. Canary не исправляет core fixtures ручной заменой своих templates.

## Qualification lifecycle

Семантический интерфейс (ADR-003): exact baseline commit + baseline release/ref/source SHA + candidate repository/release/SHA → access/preflight → disposable checkout → APPLY → runtime reload/repeat при UPDATER_RELOAD_REQUIRED → RECONCILE при migration pending → STATUS/DOCTOR → validate → configured self-tests → repeated APPLY/NO_UPDATE. Evidence сохраняет ordered stages, command/exit/stdout/stderr, exact identities, reload/migration и tracked diff до cleanup. Незапущенный, failed, unknown или stale mandatory gate не даёт aggregate PASS. Shared executable schema/entrypoint принадлежит core #261, внешняя orchestration — maintainer-tools #7. STEP-003 создаёт contract и bounded proof на доступном core, без обещания уже работающего внешнего workflow.

## Baseline advancement and recovery

STEP-002 определяет preflight и отдельный promotion: published release + maintainer acceptance → APPLY/reload/reconcile в рабочей ветке → gates → independent review diff → explicit Git workflow/merge. Failure сохраняет прежний main и evidence; повторный запуск начинает с сохранённого baseline. Destructive rollback/reset и автоматический merge отсутствуют.

## Security boundaries

Private read-доступ release App проверяет external caller до mutation. Отсутствие доступа — fail-fast. Production secrets и персональные данные отсутствуют; credentials принадлежат внешней automation, не сохраняются в project artifacts или captured output. Qualification не имеет write-authority на canary. Candidate executable tooling запускается в disposable external environment, не в canonical checkout. Cleanup следует завершению writers и сохранению failure evidence.

## Compatibility and operations

Git и core Python tooling, текущий минимум Python 3.11+. Separate stress/Windows/compatibility и publish hard gate — внешние gates; PASS canary не означает full release qualification. Unknown update transition не маскируется blind retry/sleep. Нет async product processing, сетевого API, deployment, DB migrations или отдельного scale/SLO; применимы Git/update consistency, diagnostics и сохранение истории.

## Accepted ADR

- [ADR-001: baseline и изоляция](adr/ADR-001-stable-baseline-isolation.md).
- [ADR-002: ownership и история](adr/ADR-002-ownership-preservation.md).
- [ADR-003: qualification interface](adr/ADR-003-qualification-contract.md).

## Известный architecture debt / drift

External core #261 и maintainer-tools #7/#8 — prerequisites реальной automated qualification, а не неопределённость локального architecture baseline. Их код/CI этим INIT не создаётся и не объявляется проверенным. Доступ release App не подтверждён пользовательским CLI. Representative customization и post-INIT completion state остаются STEP-001; current installed version не изменяется.
