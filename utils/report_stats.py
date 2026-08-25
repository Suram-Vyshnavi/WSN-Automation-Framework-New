"""
Execution statistics extractor for the automated summary email.

This module deliberately owns NO parsing logic of its own: it reuses the exact
same helpers the executive dashboard uses (``collect_scenarios``,
``classify_failure``, ``fmt_duration``, ``env_pretty``, ``WSN_FRAMEWORK_*``), so
the numbers in the email can never drift away from the numbers in the attached
HTML report.

Public entry point
------------------
    collect_run_stats(results_dir, env=None, persona=None) -> dict
"""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path

from utils.executive_report import (
    WSN_FRAMEWORK_TOTAL_TESTS,
    classify_failure,
    collect_scenarios,
    env_pretty,
    first_line,
    fmt_duration,
)

# Short environment token used in the subject line ("WSN Prod Web Automation").
ENV_SHORT = {
    "dev": "Dev",
    "qa": "QA",
    "preprod": "Pre-Prod",
    "prod": "Prod",
}

# Maps a classify_failure() bucket to the human phrasing used in the email
# narrative. Keys mirror utils.executive_report.classify_failure exactly.
CATEGORY_PHRASE = {
    "Timeout / Element not found": "Playwright timeout issues",
    "Assertion failure (validation)": "validation/assertion failures",
    "Automation script error": "automation script errors",
    "Ambiguous locator (strict mode)": "ambiguous locator (strict mode) matches",
    "Browser / target closed": "the browser/page context closing mid-run",
    "Navigation / Network": "navigation or network issues",
    "Auth / Permissions": "authentication or permission issues",
    "Undefined / missing step": "undefined or missing step definitions",
    "Run interrupted": "the run being interrupted",
    "Application / Other": "application issues",
    "Unknown": "issues without a captured error message",
}


def _short_env(env_keys: list[str]) -> str:
    """'prod' -> 'Prod';  ['dev','prod'] -> 'Dev + Prod'."""
    if not env_keys:
        return ""
    return " + ".join(ENV_SHORT.get(e, e.upper()) for e in env_keys)


def _join(items: list[str]) -> str:
    """['a'] -> 'a'; ['a','b'] -> 'a and b'; ['a','b','c'] -> 'a, b and c'."""
    items = [i for i in items if i]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]


def collect_run_stats(results_dir, env=None, persona=None) -> dict:
    """Read an Allure results directory and return everything the email needs.

    ``env`` is only a fallback: results merged by the matrix runner already
    carry an ``environment`` label per scenario, which is preferred.
    """
    results_dir = Path(results_dir)
    scenarios = collect_scenarios(results_dir)

    fallback_env = (env or "").strip().lower()

    counts = Counter(s["status"] for s in scenarios)
    total = len(scenarios)
    passed = counts.get("passed", 0)
    failed = counts.get("failed", 0)
    broken = counts.get("broken", 0)
    skipped = counts.get("skipped", 0)
    executed = total - skipped
    pass_pct = round(passed / executed * 100, 1) if executed else 0.0

    steps_total_run = sum(s.get("steps_total", 0) for s in scenarios)
    steps_passed = sum(s.get("steps_passed", 0) for s in scenarios)
    steps_failed = sum(s.get("steps_failed", 0) for s in scenarios)

    duration_seconds = sum(s.get("duration", 0) for s in scenarios)

    # Environments actually present in the results.
    env_keys = sorted(
        {(s.get("env") or fallback_env) for s in scenarios if (s.get("env") or fallback_env)},
        key=lambda e: (e != "prod", e),
    )
    if not env_keys and fallback_env:
        env_keys = [fallback_env]

    # ---- Per-persona (role) roll-up -------------------------------------
    by_role = defaultdict(Counter)
    for s in scenarios:
        by_role[s["role"]][s["status"]] += 1

    role_rows = []
    for role, c in sorted(by_role.items(), key=lambda kv: -sum(kv[1].values())):
        role_total = sum(c.values())
        role_exec = role_total - c.get("skipped", 0)
        role_rows.append({
            "role": role,
            "total": role_total,
            "passed": c.get("passed", 0),
            "failed": c.get("failed", 0),
            "broken": c.get("broken", 0),
            "skipped": c.get("skipped", 0),
            "pass_pct": round(c.get("passed", 0) / role_exec * 100, 1) if role_exec else 0.0,
        })

    clean_roles = [r["role"] for r in role_rows
                   if r["passed"] > 0 and r["failed"] == 0 and r["broken"] == 0]
    problem_roles = [r["role"] for r in role_rows if r["failed"] or r["broken"]]
    skipped_roles = [r["role"] for r in role_rows if r["skipped"]]

    # ---- Failure / error detail -----------------------------------------
    # Only data that actually exists in the run is recorded here. When a result
    # carries no message, the category degrades to "Unknown" rather than being
    # guessed at.
    failures = []
    for s in scenarios:
        if s["status"] not in ("failed", "broken"):
            continue
        category = s.get("category") or classify_failure(s.get("message", "")) or "Unknown"
        failures.append({
            "scenario": s["name"],
            "role": s["role"],
            "feature": s["feature"],
            "env": s.get("env") or fallback_env,
            "status": s["status"],
            "category": category,
            "phrase": CATEGORY_PHRASE.get(category, category.lower()),
            "failing_step": s.get("failing_step", ""),
            "message": first_line(s.get("message", ""), limit=220),
        })

    # category -> the personas that hit it (drives "…in the Student, Mentor and
    # New User flows").
    category_roles: dict[str, list[str]] = defaultdict(list)
    for f in failures:
        if f["role"] not in category_roles[f["category"]]:
            category_roles[f["category"]].append(f["role"])
    category_counts = Counter(f["category"] for f in failures)

    # ---- Skipped detail --------------------------------------------------
    skipped_details = []
    for s in scenarios:
        if s["status"] != "skipped":
            continue
        skipped_details.append({
            "scenario": s["name"],
            "role": s["role"],
            "env": s.get("env") or fallback_env,
            "message": first_line(s.get("message", ""), limit=220),
        })

    return {
        # headline counts (the summary table)
        "total": total,
        "passed": passed,
        "failed": failed,
        "broken": broken,          # rendered to stakeholders as "Error"
        "skipped": skipped,
        "executed": executed,
        "pass_pct": pass_pct,
        # steps
        "steps_passed": steps_passed,
        "steps_failed": steps_failed,
        "steps_total_run": steps_total_run,
        "steps_framework_total": WSN_FRAMEWORK_TOTAL_TESTS,
        "steps_display": f"{steps_passed}/{WSN_FRAMEWORK_TOTAL_TESTS}",
        # time
        "duration_seconds": duration_seconds,
        "duration_human": fmt_duration(duration_seconds),
        # environment
        "env_keys": env_keys,
        "env_display": " + ".join(env_pretty(e) for e in env_keys) if env_keys else "—",
        "env_short": _short_env(env_keys),
        "persona": persona or "combined",
        # breakdowns
        "role_rows": role_rows,
        "clean_roles": clean_roles,
        "problem_roles": problem_roles,
        "skipped_roles": skipped_roles,
        "failures": failures,
        "category_counts": dict(category_counts),
        "category_roles": {k: list(v) for k, v in category_roles.items()},
        "skipped_details": skipped_details,
        "has_results": total > 0,
    }
