# Requirements Status

> Tracked deterministic projection lifecycle state. Статус выводится из canonical REQ + STEP completion proofs.

| REQ | Название | Статус | Реализующие STEP | Evidence |
|---|---|---|---|---|
| [REQ-001](REQ-001-stable-baseline.md) | Воспроизводимый стабильный baseline | completed | STEP-001, STEP-002 | sha256:c05450a400d79e7d6edee6f1a35823f02a2f3b30359caebdc408a392989cd3c6, sha256:c9cd6494332433eec5619316b0f3f13bee0374723123d8efb5abddd626918c93 |
| [REQ-002](REQ-002-representative-state.md) | Реалистичное накопленное состояние | completed | STEP-001 | sha256:c05450a400d79e7d6edee6f1a35823f02a2f3b30359caebdc408a392989cd3c6 |
| [REQ-003](REQ-003-ownership.md) | Разделение ответственности репозиториев | completed | STEP-001, STEP-002, STEP-003 | sha256:c05450a400d79e7d6edee6f1a35823f02a2f3b30359caebdc408a392989cd3c6, sha256:c9cd6494332433eec5619316b0f3f13bee0374723123d8efb5abddd626918c93, sha256:98be73661704df13897fa63f67dee92978d9230a3b073dd5f46ffd46882a4a77 |
| [REQ-004](REQ-004-candidate-isolation.md) | Изоляция проверки candidate | completed | STEP-003 | sha256:98be73661704df13897fa63f67dee92978d9230a3b073dd5f46ffd46882a4a77 |
| [REQ-005](REQ-005-revision-identity.md) | Точная идентичность входов qualification | completed | STEP-002, STEP-003 | sha256:c9cd6494332433eec5619316b0f3f13bee0374723123d8efb5abddd626918c93, sha256:98be73661704df13897fa63f67dee92978d9230a3b073dd5f46ffd46882a4a77 |
| [REQ-006](REQ-006-update-lifecycle.md) | Штатный lifecycle обновления и восстановления | completed | STEP-002, STEP-003 | sha256:c9cd6494332433eec5619316b0f3f13bee0374723123d8efb5abddd626918c93, sha256:98be73661704df13897fa63f67dee92978d9230a3b073dd5f46ffd46882a4a77 |
| [REQ-007](REQ-007-state-preservation.md) | Сохранность project-owned артефактов | completed | STEP-001, STEP-002, STEP-003 | sha256:c05450a400d79e7d6edee6f1a35823f02a2f3b30359caebdc408a392989cd3c6, sha256:c9cd6494332433eec5619316b0f3f13bee0374723123d8efb5abddd626918c93, sha256:98be73661704df13897fa63f67dee92978d9230a3b073dd5f46ffd46882a4a77 |
| [REQ-008](REQ-008-qualification-evidence.md) | Диагностика и достоверный результат | completed | STEP-002, STEP-003 | sha256:c9cd6494332433eec5619316b0f3f13bee0374723123d8efb5abddd626918c93, sha256:98be73661704df13897fa63f67dee92978d9230a3b073dd5f46ffd46882a4a77 |
| [REQ-009](REQ-009-idempotence.md) | Идемпотентное повторное применение | completed | STEP-002, STEP-003 | sha256:c9cd6494332433eec5619316b0f3f13bee0374723123d8efb5abddd626918c93, sha256:98be73661704df13897fa63f67dee92978d9230a3b073dd5f46ffd46882a4a77 |
| [REQ-010](REQ-010-baseline-advancement.md) | Контролируемое продвижение baseline | completed | STEP-002 | sha256:c9cd6494332433eec5619316b0f3f13bee0374723123d8efb5abddd626918c93 |
| [REQ-011](REQ-011-private-access-security.md) | Приватный доступ и безопасные границы | completed | STEP-003 | sha256:98be73661704df13897fa63f67dee92978d9230a3b073dd5f46ffd46882a4a77 |
| [REQ-012](REQ-012-minimal-compatibility.md) | Минимальный стек и поддерживаемая совместимость | completed | STEP-001, STEP-002, STEP-003 | sha256:c05450a400d79e7d6edee6f1a35823f02a2f3b30359caebdc408a392989cd3c6, sha256:c9cd6494332433eec5619316b0f3f13bee0374723123d8efb5abddd626918c93, sha256:98be73661704df13897fa63f67dee92978d9230a3b073dd5f46ffd46882a4a77 |
