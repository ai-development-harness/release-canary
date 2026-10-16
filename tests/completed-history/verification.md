# Проверка набора #355

Локально проверена принятая база `7813d33dee55f02c6b221fc0dbffc686acd48a8b` с candidate engine исправления #355. Это summary наблюдений, не реконструированный terminal output и не продуктовый REVIEW.

- `run.py --baseline <canary> --harness-root <candidate>`: exit 0, PASS всех 17 сценариев.
- Собственные исторические task/plan/review сохраняются побайтно, кроме явно повреждаемых входов отдельных disposable fixtures.
- Положительные непротиворечивые fixtures проходят общий planning validator; исторические планы имеют `status: historical`, без команды re-plan.
- Настоящие NEXT/IMPLEMENT/Verification используют общий completion proof. Старые зависимости completed STEP не переоткрываются; повреждённый прямой prerequisite блокирует новую работу.
- Собственный устаревший PLAN consumer блокирует IMPLEMENT. NEXT вправе предложить RUN с предварительным PLAN; отдельная Verification не заменяет readiness gate.
- На установленном engine v0.14.1 runner завершается ненулевым exit: воспроизведён `completion-dependency-proof-missing` для настоящих REVIEW STEP-002/003.
- В disposable candidate умышленный обход trusted completion guard обнаружен сценарием `direct-review-missing`.
- В другой disposable candidate отключение проверки актуальности собственного PLAN обнаружено сценарием `consumer-plan-stale`.
- Независимый reviewer воспроизвёл ошибку проверки старого CTS при обычном clone после незакоммиченного upgrade. После исправления переноса effective snapshot изменённый валидный CTS обнаруживается: ожидаемый SEMANTIC отличается от фактического DONE/step-show.

Основной Harness проверен 77 discoverable self-tests, `validate.py --mode manual/ci`, STEP NEXT / impact-analysis / initialized upgrade regression и bounded stress на пяти итерациях: PASS. Независимое code-review завершилось PASS после устранения двух findings. Удалённые CI, qualification и принятие релиза подтверждаются отдельно артефактами release workflow.
