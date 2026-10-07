# Architecture Decision Records

ADR фиксирует **устойчивое архитектурное решение**, его контекст и последствия. ADR не создаётся для каждой задачи.

## Статусы

- `Proposed`
- `Accepted`
- `Rejected`
- `Superseded`
- `Deprecated`

## Правила

1. Accepted ADR считается immutable historical decision record.
2. Если контракт меняется, создай новый ADR и укажи `Supersedes`.
3. Не переписывай прошлую мотивацию задним числом.
4. Если решение ещё не принято, используй `Proposed` или `OPEN_QUESTIONS`, а не выдумывай Accepted ADR.
5. ID не переиспользуется: `ADR-001`, `ADR-002`, ...

## Index

- [ADR-001 — Стабильный baseline и изолированный candidate](ADR-001-stable-baseline-isolation.md).
- [ADR-002 — Ownership и сохранение downstream истории](ADR-002-ownership-preservation.md).
- [ADR-003 — Exact revisions и fail-closed evidence lifecycle](ADR-003-qualification-contract.md).
