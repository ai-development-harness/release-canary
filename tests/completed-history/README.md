# Завершённые STEP и новая работа

Набор проверяет модель [Harness #355](https://github.com/ai-development-harness/ai-development-harness-template/issues/355): completed STEP остаётся принятым историческим фактом. Текущие требования, план и проверки относятся к новой работе.

`STEP-991.md` и `REQ-991-scenario.md` — входные данные синтетического consumer. Они хранятся вне canonical directories и не изображают выполненную продуктовую работу. Runner создаёт отдельную disposable Git-копию принятой базы для каждого сценария. Исторические REVIEW STEP-001/002/003 используются настоящие, через обычный schema/trust validator. Для нового consumer тестовый PLAN создают штатные deterministic writers.

| Сценарии | Ожидаемый результат |
| --- | --- |
| Принятая база, старые REVIEW без dependency metadata | Новая работа разрешена |
| Изменённое architecture description, REQ, superseded ADR, будущий OQ или переименованный старый anchor | Прежний completion proof сохранён; новый consumer использует актуальный план |
| Изменившийся depends_on completed STEP, отсутствующий REVIEW его старого предка | Принятый прямой prerequisite не переоткрывается |
| Missing/corrupt REVIEW, отсутствие Evidence, Verification FAIL или незавершённый прямой prerequisite | Новая работа BLOCKED |
| Отсутствующая активная зависимость или активный цикл | Новая работа BLOCKED |
| Устаревший собственный PLAN нового consumer | IMPLEMENT BLOCKED; NEXT может предложить RUN, который сначала выполнит PLAN |

Runner сравнивает результаты общего proof, dependency gate, Verification facts, NEXT и настоящего dispatcher IMPLEMENT. В положительных случаях исполняется реальная Verification нового consumer; в отрицательных проверяется отказ до реализации. Общий planning validator также проверяется на положительных непротиворечивых сценариях; completed планы получают `historical` без команды re-plan. Прежние task/plan/review сравниваются побайтно; намеренное повреждение разрешено только внутри конкретного отрицательного fixture. Исходный checkout не меняется.

Из корня canary после установки исправленного Harness:

```bash
python3 tests/completed-history/run.py --baseline . --harness-root . --output /tmp/completed-history.json
```

До выпуска можно проверить candidate engine без изменения установленного Harness:

```bash
python3 tests/completed-history/run.py --baseline . --harness-root ../ai-development-harness-template --output /tmp/completed-history-candidate.json
```

Initialized upgrade qualification автоматически запускает этот project-owned набор после обновления disposable canary. Проверка на старом engine v0.14.1 должна завершаться ошибкой; проверка на исправленном candidate — PASS.
