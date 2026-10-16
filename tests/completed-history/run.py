#!/usr/bin/env python3
"""Проверить #355 на disposable копиях настоящей принятой истории canary.

Сценарии намеренно портят только отдельные копии. Прежние PASS не создаются
и не редактируются для положительных случаев; synthetic consumer — тестовый вход.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import stat
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, timeout=60)
    if result.returncode:
        raise RuntimeError("SCENARIO_GIT_FAILED")
    return result.stdout.strip()



def effective_snapshot(root: Path) -> dict:
    """Зафиксировать фактические bytes/modes, включая updater diff вне HEAD."""
    result = {}
    for directory, dirs, files in os.walk(root, followlinks=False):
        base = Path(directory)
        dirs[:] = [n for n in dirs if n not in {".git", "__pycache__"}
                   and not (base == root / ".harness" and n == "local")]
        for name in files + [n for n in dirs if (base / n).is_symlink()]:
            path = base / name
            if path.suffix == ".pyc" or path == root / ".harness/.execution-checkpoint-known":
                continue
            data = os.readlink(path).encode() if path.is_symlink() else path.read_bytes()
            result[path.relative_to(root).as_posix()] = (hashlib.sha256(data).hexdigest(), stat.S_IMODE(path.lstat().st_mode))
    return result


def copy_effective_baseline(baseline: Path, work: Path) -> None:
    """Clone задаёт историю, effective snapshot — установленный protocol.

    Updater оставляет новые файлы и удаления незакоммиченными. Один clone
    потерял бы их и проверял старые CTS/skills/config вместо установленного candidate.
    """
    git(baseline, "clone", "--quiet", "--no-local", str(baseline), str(work))
    for child in work.iterdir():
        if child.name == ".git":
            continue
        if child.is_dir() and not child.is_symlink():
            shutil.rmtree(child)
        else:
            child.unlink()

    def ignore(directory: str, names: list[str]) -> set[str]:
        skipped = {n for n in names if n in {".git", "__pycache__"} or n.endswith(".pyc")}
        if Path(directory) == baseline / ".harness":
            skipped.update({"local", ".execution-checkpoint-known"})
        return skipped

    shutil.copytree(baseline, work, dirs_exist_ok=True, symlinks=True, ignore=ignore)
    assert effective_snapshot(work) == effective_snapshot(baseline), "effective baseline snapshot mismatch"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--harness-root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    baseline = args.baseline.resolve()
    sys.path.insert(0, str(args.harness_root.resolve() / ".harness/tools"))
    from command_dispatch import start_dispatch
    from document_contract import render_document
    from execution_status import start_execution
    from harness_config import task_directory, review_directory, requirements_directory
    from planning_contract import (read_task, step_completion_proof, dependency_completion_failures,
                                   implementation_prerequisite_failures, planning_context_basis, validate_planning_contracts)
    from impact_analysis import plan_staleness
    from review_contract import latest_trusted_review
    from semantic_artifacts import write_plan_draft, write_planning_review
    from step_next import resolve_step_next
    from verification import verification_dependency_facts, run_step_verification

    fixtures = Path(__file__).resolve().parent
    cases = json.loads((fixtures / "scenarios.json").read_text(encoding="utf-8"))
    baseline_revision = git(baseline, "rev-parse", "HEAD")
    baseline_status = git(baseline, "status", "--porcelain=v1")
    before_snapshot = effective_snapshot(baseline)
    records = []
    with tempfile.TemporaryDirectory(prefix="completed-history-canary-") as tmp:
        for case in cases:
            name = case["name"]
            work = Path(tmp) / name
            copy_effective_baseline(baseline, work)
            tasks, reviews, reqs = task_directory(work), review_directory(work), requirements_directory(work)
            protected = {p.relative_to(work).as_posix(): p.read_bytes()
                         for folder in (tasks, reviews) for p in folder.rglob("*.md")}
            shutil.copyfile(fixtures / "STEP-991.md", tasks / "STEP-991.md")
            shutil.copyfile(fixtures / "REQ-991-scenario.md", reqs / "REQ-991-scenario.md")
            # Только новый synthetic consumer получает тестовый PLAN через
            # реальные writers. Исторические task/plan/review остаются прежними.
            write_plan_draft(work, "STEP-991", {
                "implementationPlan": [{"title": "Проверить новую работу", "actions": ["Исполнить тестовый consumer."]}],
                "verification": [{"kind": "command", "value": 'python3 -c "print(991)"'}],
            })
            start_execution(work, "STEP PLAN STEP-991")
            result = write_planning_review(work, "STEP-991", {
                "verdict": "pass", "findings": [], "rationale": "Synthetic planning fixture, не продуктовая приёмка.",
            })
            assert result["status"] == "PASS", result
            accepted = step_completion_proof(work, "STEP-003")
            assert accepted["complete"], accepted
            before_context = planning_context_basis(work, "STEP-991")
            changed_history = set()
            direct = tasks / "STEP-003.md"
            report = latest_trusted_review(work, "STEP-003")["path"]
            if name == "architecture-description":
                path = work / "docs/architecture.md"
                text = path.read_text(encoding="utf-8")
                # Меняем referenced секцию, а не добавляем unrelated хвост.
                lines = text.splitlines(keepends=True)
                index = next(i for i, line in enumerate(lines) if line.strip().lower() == "## ownership")
                lines.insert(index + 1, "\nУточнение после приёмки completed STEP.\n")
                path.write_text("".join(lines), encoding="utf-8")
                # Новая работа должна получить новый актуальный PLAN; это
                # не повторное планирование старого completed STEP.
                assert planning_context_basis(work, "STEP-991") != before_context
                write_plan_draft(work, "STEP-991", {
                    "implementationPlan": [{"title": "Проверить новую работу", "actions": ["Учесть текущее описание."]}],
                    "verification": [{"kind": "command", "value": 'python3 -c "print(991)"'}],
                })
                write_planning_review(work, "STEP-991", {"verdict": "pass", "findings": [], "rationale": "Актуальный synthetic PLAN."})
            elif name == "requirement-changed":
                path = sorted(reqs.glob("REQ-001-*.md"))[0]
                path.write_text(path.read_text(encoding="utf-8") + "\nНовое нормативное требование.\n", encoding="utf-8")
            elif name == "superseded-adr":
                path = sorted((work / "docs/adr").glob("ADR-001-*.md"))[0]
                path.write_text(path.read_text(encoding="utf-8").replace("status: accepted", "status: superseded", 1), encoding="utf-8")
            elif name == "future-open-question":
                oq = work / "docs/open-questions/OQ-991-scenario.md"
                oq.write_text("---\nschema: 1\nid: OQ-991\nstatus: open\naffects:\n  - REQ-003\ncreated_at: 2026-10-16T00:00:00Z\nresolved_at: null\n---\n\n# OQ-991 — Будущая работа\n\n## Context\n\nВопрос возник после принятия истории.\n\n## Decision needed\n\nУточнить следующий контракт.\n\n## Resolution\n\n", encoding="utf-8")
            elif name == "historical-anchor-renamed":
                path = work / "docs/architecture.md"
                text = path.read_text(encoding="utf-8")
                assert "## Baseline state" in text
                path.write_text(text.replace("## Baseline state", "## Accepted baseline", 1), encoding="utf-8")
            elif name == "old-review-metadata":
                assert "dependency_completion_basis" not in latest_trusted_review(work, "STEP-003")["document"]["frontmatter"]
            elif name == "completed-dependency-changed":
                doc = read_task(work, "STEP-003")
                doc["frontmatter"]["depends_on"] = ["STEP-999"]
                direct.write_text(render_document(doc["frontmatter"], doc["body"]), encoding="utf-8")
                changed_history.add(direct.relative_to(work).as_posix())
                # Изменился прямой task contract: PLAN нового consumer обновляется.
                write_plan_draft(work, "STEP-991", {
                    "implementationPlan": [{"title": "Проверить новую работу", "actions": ["Учесть текущий прямой контракт."]}],
                    "verification": [{"kind": "command", "value": 'python3 -c "print(991)"'}],
                })
                write_planning_review(work, "STEP-991", {"verdict": "pass", "findings": [], "rationale": "Актуальный synthetic PLAN."})
            elif name == "ancestor-review-missing":
                path = latest_trusted_review(work, "STEP-001")["path"]
                changed_history.add(path.relative_to(work).as_posix())
                path.unlink()
            elif name.startswith("direct-review-"):
                changed_history.add(report.relative_to(work).as_posix())
                if name.endswith("missing"):
                    report.unlink()
                else:
                    report.write_text("повреждённый REVIEW", encoding="utf-8")
            elif name in {"direct-evidence-missing", "direct-verification-failed", "direct-not-completed"}:
                doc = read_task(work, "STEP-003")
                if name == "direct-evidence-missing":
                    body = doc["body"]
                    start = body.index("## Evidence")
                    end = body.find("\n## ", start + 3)
                    doc["body"] = body[:start] + "## Evidence\n\n—\n" + (body[end:] if end >= 0 else "")
                elif name == "direct-verification-failed":
                    doc["body"] = doc["body"].replace("- Status: PASS", "- Status: FAIL")
                    assert doc["body"] != read_task(work, "STEP-003")["body"]
                else:
                    doc["frontmatter"]["status"] = "in_progress"
                direct.write_text(render_document(doc["frontmatter"], doc["body"]), encoding="utf-8")
                changed_history.add(direct.relative_to(work).as_posix())
            elif name in {"active-dependency-missing", "active-cycle"}:
                path = tasks / "STEP-991.md"
                text = path.read_text(encoding="utf-8")
                text = text.replace("  - STEP-003", "  - " + ("STEP-999" if name.endswith("missing") else "STEP-991"))
                path.write_text(text, encoding="utf-8")
            elif name == "consumer-plan-stale":
                path = reqs / "REQ-991-scenario.md"
                path.write_text(path.read_text(encoding="utf-8") + "\nНовый обязательный результат consumer.\n", encoding="utf-8")
            elif name != "unchanged":
                raise AssertionError(f"unknown scenario: {name}")

            planning_errors = validate_planning_contracts(work)
            if case["executable"] and name not in {"completed-dependency-changed", "ancestor-review-missing"}:
                assert not planning_errors, (name, planning_errors)
            for sid in ("STEP-001", "STEP-002", "STEP-003"):
                if read_task(work, sid)["frontmatter"].get("status") == "completed":
                    assert plan_staleness(work, sid) == {"status": "historical", "causes": [], "action": None}
            failures = dependency_completion_failures(work, "STEP-991")
            readiness = implementation_prerequisite_failures(work, "STEP-991")
            facts = verification_dependency_facts(work, "STEP-991")
            next_result = resolve_step_next(work)
            executable = not readiness
            assert executable is case["executable"], (name, readiness)
            # NEXT вправе выбрать RUN со stale PLAN: RUN сначала выполнит PLAN.
            if case["executable"]:
                assert not failures and all(f["complete"] for f in facts), (name, failures, facts)
                assert next_result["status"] == "PASS" and next_result["command"] == "STEP RUN STEP-991", (name, next_result)
                handoff = start_dispatch(work, "STEP IMPLEMENT STEP-991")
                assert handoff["status"] == "SEMANTIC", (name, handoff)
                verification = run_step_verification(work, "STEP-991")
                assert verification["status"] == "PASS", (name, verification)
                assert step_completion_proof(work, "STEP-003") == accepted, name
            else:
                handoff = start_dispatch(work, "STEP IMPLEMENT STEP-991")
                assert handoff["status"] == "BLOCKED", (name, handoff)
                assert readiness, name
                verification = run_step_verification(work, "STEP-991")
                if name != "consumer-plan-stale":
                    assert verification["status"] == "BLOCKED", (name, verification)
            for rel, data in protected.items():
                if rel not in changed_history:
                    assert (work / rel).read_bytes() == data, (name, rel)
            records.append({"scenario": name, "status": "PASS", "executable": executable,
                            "dependencyFailures": failures, "readinessFailures": readiness,
                            "dispatcherStatus": handoff["status"], "nextStatus": next_result["status"],
                            "verificationStatus": verification["status"],
                            "planningValidationErrors": planning_errors,
                            "protectedArtifacts": len(protected) - len(changed_history)})
    assert effective_snapshot(baseline) == before_snapshot, "source baseline mutated"
    assert git(baseline, "rev-parse", "HEAD") == baseline_revision
    assert git(baseline, "status", "--porcelain=v1") == baseline_status
    result = {"status": "PASS", "baselineRevision": baseline_revision, "scenarios": records}
    if args.output:
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
