---
schema: 1
id: REQ-012
priority: high
source: brief
steps:
  - STEP-001
  - STEP-002
  - STEP-003
adrs:
  - ADR-002
---

# REQ-012 — Минимальный стек и поддерживаемая совместимость

## Requirement

Canary использует Git, Python Harness tooling и Markdown/YAML/TOML/JSON без отдельного приложения, БД или framework. Baseline соответствует документированной нижней границе core, сейчас Python 3.11+. Synthetic, stress и Windows coverage остаются в core/release qualification.

## Rationale

Fixture должен оставаться небольшим и проверять update contract, а не собственный runtime.

## Acceptance

- Документация setup и проверки ссылается на существующие Harness commands, без выдуманных build/deploy scripts.
- Baseline/preflight contract включает validation и configured suite на поддерживаемом Python, включая текущую нижнюю границу 3.11.
- Canary не дублирует Windows matrix и stress suite; их external ownership указан явно, а полный release PASS не выводится из одного canary gate.
