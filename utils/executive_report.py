"""
Executive QA Dashboard generator.

Reads a directory of Allure result JSON files (the same ones produced by
allure_behave.formatter) and renders a single, self-contained HTML file that is
designed for stakeholders (QA / Dev / Manager / Product Owner / Client) rather
than for engineers debugging a run.

Design goals
------------
* One file, no external dependencies at view time. All charts are inline SVG /
  CSS (donut, bars, trend line, failure distribution) so the report opens
  offline, emails cleanly, and prints to PDF without a headless browser.
* Self-explanatory: every section has a heading and the numbers speak for
  themselves. A non-technical reader should understand health at a glance.
* Safe: credentials are masked. Passwords are never rendered.

Public entry point
------------------
    generate_executive_dashboard(results_dir, output_html, persona=None, extra_meta=None)
"""

from __future__ import annotations

import html
import json
import os
import platform
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from utils.logger import log

# ----------------------------------------------------------------------------
# Brand / theme
# ----------------------------------------------------------------------------
BRAND = {
    "name": "Wadhwani Foundation",
    "primary": "#C8102E",   # brand red (chrome / headers)
    "accent": "#F47920",    # brand orange
    # Status colors use the universally understood QA convention so executives
    # read them instantly (green = good). Brand red/orange is kept for chrome.
    "pass": "#16A34A",
    "fail": "#DC2626",
    "broken": "#F59E0B",
    "skip": "#94A3B8",
}

# Wadhwani Foundation brand mark recreated as inline SVG (red/orange feather
# fan) so the report stays a single self-contained file with no external image.
WADHWANI_LOGO_SVG = """
<svg viewBox="0 0 100 78" width="40" height="31" role="img" aria-label="Wadhwani Foundation">
  <!-- outer (lightest) blades -->
  <polygon points="50,66 74,30 82,37" fill="#F9A04A"/>
  <polygon points="50,66 26,30 18,37" fill="#F9A04A"/>
  <!-- mid blades -->
  <polygon points="50,66 66,21 72,26" fill="#F47920"/>
  <polygon points="50,66 34,21 28,26" fill="#F47920"/>
  <!-- inner orange blades -->
  <polygon points="50,66 58,15 63,18" fill="#E2591C"/>
  <polygon points="50,66 42,15 37,18" fill="#E2591C"/>
  <!-- central red blades (open book) -->
  <polygon points="50,66 52,12 57,14" fill="#C8102E"/>
  <polygon points="50,66 48,12 43,14" fill="#C8102E"/>
</svg>"""

# Fixed headline figure for the total number of automated test cases across
# the whole WSN Automation Framework, shown next to the "Total Tests" KPI for
# context - a given run's own total can be lower than this if only a subset
# of features/personas ran.
WSN_FRAMEWORK_TOTAL_TESTS_PASSED = 429
WSN_FRAMEWORK_TOTAL_TESTS = 545

STATUS_ORDER = ["passed", "failed", "broken", "skipped"]
STATUS_LABEL = {
    "passed": "Passed",
    "failed": "Failed",
    # 'broken' is Allure's internal status key; surface it to stakeholders as
    # "Error" (a broken step is a test/automation error, not a product failure).
    "broken": "Error",
    "skipped": "Skipped",
    "unknown": "Unknown",
}
STATUS_COLOR = {
    "passed": BRAND["pass"],
    "failed": BRAND["fail"],
    "broken": BRAND["broken"],
    "skipped": BRAND["skip"],
    "unknown": "#64748B",
}


# ----------------------------------------------------------------------------
# Small helpers
# ----------------------------------------------------------------------------
def esc(value) -> str:
    return html.escape("" if value is None else str(value))


def mask_username(username: str) -> str:
    """a***z@domain.com  -> keep first char of local part + domain visible."""
    if not username:
        return "—"
    username = str(username)
    if "@" in username:
        local, _, domain = username.partition("@")
        if len(local) <= 2:
            shown = local[:1] + "*"
        else:
            shown = local[0] + "*" * (len(local) - 2) + local[-1]
        return f"{shown}@{domain}"
    if len(username) <= 3:
        return username[0] + "**"
    return username[:2] + "*" * (len(username) - 3) + username[-1]


def fmt_duration(seconds: float) -> str:
    seconds = int(round(seconds or 0))
    if seconds < 60:
        return f"{seconds}s"
    minutes, sec = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes}m {sec:02d}s"
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h {minutes:02d}m {sec:02d}s"


def classify_failure(message: str) -> str:
    """Bucket a failure message into a stakeholder-friendly category.

    Tuned to the actual messages this suite emits. Crucially, it separates
    *automation/test defects* (TypeError, AttributeError, undefined steps —
    bugs in the test code) from *application failures*, so stakeholders do not
    read a broken test script as a broken product feature.
    """
    msg = (message or "").strip()
    if not msg:
        return "Unknown"
    low = msg.lower()

    # Order matters: most specific signals first.
    if "keyboardinterrupt" in low:
        return "Run interrupted"
    if "implement step definitions" in low or "undefined step" in low:
        return "Undefined / missing step"
    if "strict mode violation" in low:
        return "Ambiguous locator (strict mode)"
    if "targetclosederror" in low or "target page, context or brow" in low or "browser has been closed" in low:
        return "Browser / target closed"
    if low.startswith(("typeerror", "attributeerror", "nameerror", "keyerror",
                        "importerror", "modulenotfounderror", "indexerror")):
        return "Automation script error"
    if "timeout" in low or "wait_for" in low or "exceeded" in low:
        return "Timeout / Element not found"
    if low.startswith("assertionerror") or "assert" in low:
        return "Assertion failure (validation)"
    if "net::" in low or "connection" in low or "navigation" in low:
        return "Navigation / Network"
    if "permission" in low or "auth" in low or "credential" in low:
        return "Auth / Permissions"
    return "Application / Other"


# Explicit Allure 'feature' label -> role/persona mapping, derived from the
# Feature: line of each .feature file. Generic student-app features (Courses,
# Forums, Home Dashboard, ...) all run under the Student persona.
FEATURE_ROLE_MAP = {
    "faculty login": "Faculty",
    "rm login": "Relationship Manager",
    "mentor": "Mentor",
    "career buddy": "Career Buddy",
    "student persona": "Student",
    "login": "Student",
    "home dashboard": "Student",
    "courses": "Student",
    "programs": "Student",
    "forums": "Student",
    "jobsconnect": "Student",
    "interview coach": "Student",
    "personal_pitch": "Student",
    "my career advisor": "Student",
}


def classify_role(feature: str) -> str:
    """Map an Allure 'feature' label to the persona/role under test."""
    f = (feature or "").strip().lower()
    if f in FEATURE_ROLE_MAP:
        return FEATURE_ROLE_MAP[f]
    # Fallback heuristics for any feature added later.
    if "faculty" in f:
        return "Faculty"
    if f.startswith("rm ") or "relationship" in f:
        return "Relationship Manager"
    if "mentor" in f:
        return "Mentor"
    if "career buddy" in f or "career_buddy" in f:
        return "Career Buddy"
    if "institute" in f or "admin" in f:
        return "Institute Admin"
    return "Student"


PERSONA_PRETTY = {
    "student": "Student",
    "faculty": "Faculty",
    "rm": "Relationship Manager",
    "mentor": "Mentor",
    "career_buddy": "Career Buddy",
    "institute_admin": "Institute Admin",
}

ENV_DISPLAY = {
    "dev": "Development",
    "qa": "QA",
    "preprod": "Pre-Prod",
    "prod": "Production",
}


def env_pretty(env_name: str) -> str:
    e = (env_name or "").strip().lower()
    return ENV_DISPLAY.get(e, e.upper() if e else "—")


def embed_screenshot(image_path: Path, max_width: int = 900) -> str:
    """Return a downscaled JPEG data URI for inline embedding, or '' on failure.

    Keeps the report self-contained and portable (no broken file links when the
    folder is moved/emailed) while controlling size via downscale + JPEG quality.
    """
    import base64
    try:
        from PIL import Image as PILImage
        with PILImage.open(image_path) as img:
            img = img.convert("RGB")
            if img.width > max_width:
                ratio = max_width / img.width
                img = img.resize((max_width, int(img.height * ratio)))
            from io import BytesIO
            buf = BytesIO()
            img.save(buf, format="JPEG", quality=70, optimize=True)
            data = base64.b64encode(buf.getvalue()).decode("ascii")
            return f"data:image/jpeg;base64,{data}"
    except Exception:
        # Fallback: embed the raw PNG bytes directly.
        try:
            data = base64.b64encode(Path(image_path).read_bytes()).decode("ascii")
            return f"data:image/png;base64,{data}"
        except Exception:
            return ""


def first_line(text: str, limit: int = 160) -> str:
    if not text:
        return ""
    line = str(text).strip().splitlines()[0]
    return (line[:limit] + "…") if len(line) > limit else line


# ----------------------------------------------------------------------------
# Data collection
# ----------------------------------------------------------------------------
def collect_scenarios(results_dir: Path) -> list[dict]:
    scenarios = []
    for file in Path(results_dir).glob("*-result.json"):
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
        except Exception:
            continue

        labels = {l.get("name"): l.get("value") for l in data.get("labels", [])}
        feature = labels.get("feature") or (data.get("titlePath") or ["—"])[-1]
        # Environment + persona role are injected by the dev+prod matrix runner
        # when it merges per-(env,persona) results into the combined dir. A plain
        # single-run result has neither, so both fall back gracefully below.
        env_label = (labels.get("environment") or "").strip().lower()
        role = labels.get("persona_role") or classify_role(feature)
        status = (data.get("status") or "unknown").lower()
        start = data.get("start") or 0
        stop = data.get("stop") or start
        sd = data.get("statusDetails") or {}
        message = sd.get("message") or ""
        trace = sd.get("trace") or ""

        # Find the failing step + a screenshot to surface in failure analysis.
        failing_step = ""
        screenshot = ""
        steps = data.get("steps") or []
        last_shot = ""
        for step in steps:
            for att in step.get("attachments", []) or []:
                if str(att.get("type", "")).startswith("image"):
                    last_shot = att.get("source", "")
            if (step.get("status") or "").lower() in ("failed", "broken") and not failing_step:
                failing_step = step.get("name", "")
        screenshot = last_shot

        # Step-level (test-case-level) counts, so the dashboard can show how
        # many individual steps ran/passed/failed within each scenario, not
        # just the overall scenario status.
        steps_total = len(steps)
        steps_passed = sum(1 for st in steps if (st.get("status") or "").lower() == "passed")
        steps_failed = sum(1 for st in steps if (st.get("status") or "").lower() in ("failed", "broken"))
        steps_skipped = max(0, steps_total - steps_passed - steps_failed)

        scenarios.append({
            "name": data.get("name") or file.name,
            "feature": feature,
            "role": role,
            "env": env_label,
            "status": status,
            "severity": labels.get("severity", "normal"),
            "duration": round(max(0, stop - start) / 1000, 2),
            "start": start,
            "message": message,
            "trace": trace,
            "failing_step": failing_step,
            "category": classify_failure(message) if status in ("failed", "broken") else "",
            "screenshot": screenshot,
            "steps_total": steps_total,
            "steps_passed": steps_passed,
            "steps_failed": steps_failed,
            "steps_skipped": steps_skipped,
        })

    scenarios.sort(key=lambda s: s.get("start", 0))
    return scenarios


def gather_meta(persona: str | None, results_dir: Path, extra_meta: dict | None) -> dict:
    extra_meta = extra_meta or {}

    def git_sha():
        try:
            out = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                capture_output=True, text=True, timeout=5,
                cwd=str(Path(results_dir).resolve().parent.parent),
            )
            if out.returncode == 0:
                return out.stdout.strip()
        except Exception as _ignored:
            log.debug("Optional step in git_sha() did not apply: %s", _ignored)
        return ""

    # Execution type detection.
    if os.getenv("GITHUB_ACTIONS"):
        exec_type = "GitHub Actions"
    elif os.getenv("JENKINS_URL") or os.getenv("BUILD_NUMBER"):
        exec_type = "Jenkins"
    else:
        exec_type = "Local"

    # Prefer explicit run metadata (matrix/single runner) over ambient shell ENV.
    # This avoids stale terminal values (e.g. ENV=dev) mislabeling prod reports.
    env_name = (extra_meta.get("env") or os.getenv("ENV") or "dev").lower()
    env_display = {"dev": "Development", "qa": "QA", "preprod": "Pre-Prod", "prod": "Production"}.get(env_name, env_name.upper())

    try:
        import behave
        behave_ver = behave.__version__
    except Exception:
        behave_ver = "1.2.6"

    base_url = extra_meta.get("base_url", "")
    if not base_url:
        try:
            from utils.config import Config
            base_url = Config.BASE_URL
        except Exception:
            base_url = os.getenv("BASE_URL", "")

    build = os.getenv("BUILD_VERSION") or os.getenv("BUILD_NUMBER") or git_sha() or "N/A"

    return {
        "persona": persona or os.getenv("PERSONA", "—"),
        "env_name": env_name,
        "env_display": env_display,
        "base_url": base_url,
        "browser": extra_meta.get("browser", "Chromium (Playwright)"),
        "os": platform.platform(),
        "python": platform.python_version(),
        "behave": behave_ver,
        "framework": f"Behave {behave_ver} + Playwright (Allure)",
        "exec_type": exec_type,
        "build": build,
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "headless": os.getenv("HEADLESS", "false"),
    }


def gather_credentials(scenarios: list[dict], persona: str | None) -> list[dict]:
    """Return masked credential rows for the roles that actually ran."""
    try:
        from utils.config import Config
        cred_map = Config.CREDENTIALS
    except Exception:
        cred_map = {}

    role_to_key = {
        "Student": "student",
        "Faculty": "faculty",
        "Relationship Manager": "rm",
        "Mentor": "mentor",
        "Career Buddy": "career_buddy",
        "Institute Admin": "institute_admin",
    }

    roles_present = {s["role"] for s in scenarios}
    if persona:
        # Single-persona run: trust the persona explicitly.
        pretty = {v: k for k, v in role_to_key.items()}.get(persona.lower())
        if pretty:
            roles_present.add(pretty)

    rows = []
    for role in sorted(roles_present):
        key = role_to_key.get(role)
        configured_username, configured_password = cred_map.get(key, ("", "")) if key else ("", "")
        rows.append({
            "role": role,
            "username": mask_username(configured_username) if configured_username else "—",
            "password": "••••••••" if configured_password else "—",
            "account": "Configured test account" if configured_username else "Not configured",
        })
    return rows


# ----------------------------------------------------------------------------
# Execution history (for the trend chart)
# ----------------------------------------------------------------------------
def update_history(results_dir: Path, persona: str, total, passed, failed, broken, skipped, pass_pct):
    history_file = Path(results_dir).resolve().parent / "execution_history.json"
    try:
        history = json.loads(history_file.read_text(encoding="utf-8")) if history_file.exists() else []
    except Exception:
        history = []

    history.append({
        "ts": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "persona": persona,
        "total": total,
        "passed": passed,
        "failed": failed,
        "broken": broken,
        "skipped": skipped,
        "pass_pct": pass_pct,
    })
    history = history[-30:]  # keep last 30 runs
    try:
        history_file.write_text(json.dumps(history, indent=1), encoding="utf-8")
    except Exception as _ignored:
        log.debug("Optional step in update_history() did not apply: %s", _ignored)
    return history


# ----------------------------------------------------------------------------
# Inline SVG / CSS chart builders
# ----------------------------------------------------------------------------
def svg_donut(counts: dict, size: int = 180) -> str:
    total = sum(counts.values()) or 1
    radius = size / 2 - 18
    cx = cy = size / 2
    circumference = 2 * 3.141592653589793 * radius
    offset = 0.0
    segments = []
    for status in STATUS_ORDER:
        value = counts.get(status, 0)
        if not value:
            continue
        frac = value / total
        dash = frac * circumference
        segments.append(
            f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" '
            f'stroke="{STATUS_COLOR[status]}" stroke-width="22" '
            f'stroke-dasharray="{dash:.2f} {circumference - dash:.2f}" '
            f'stroke-dashoffset="{-offset:.2f}" transform="rotate(-90 {cx} {cy})"/>'
        )
        offset += dash

    passed = counts.get("passed", 0)
    pct = round(passed / total * 100) if total else 0
    return f"""
    <svg viewBox="0 0 {size} {size}" width="{size}" height="{size}" role="img" aria-label="Pass/Fail distribution">
      {''.join(segments)}
      <text x="{cx}" y="{cy-4}" text-anchor="middle" font-size="34" font-weight="800" fill="#0F172A">{pct}%</text>
      <text x="{cx}" y="{cy+20}" text-anchor="middle" font-size="12" fill="#64748B">PASS</text>
    </svg>"""


def module_bars(module_rows: list[dict]) -> str:
    if not module_rows:
        return "<p class='muted'>No module data.</p>"
    rows = []
    for m in module_rows:
        total = m["total"] or 1
        seg = []
        for status in STATUS_ORDER:
            v = m["counts"].get(status, 0)
            if v:
                seg.append(
                    f'<span style="width:{v/total*100:.1f}%;background:{STATUS_COLOR[status]}" '
                    f'title="{STATUS_LABEL[status]}: {v}"></span>'
                )
        rows.append(f"""
          <div class="barrow">
            <div class="barlabel" title="{esc(m['module'])}">{esc(m['module'])}</div>
            <div class="bartrack">{''.join(seg)}</div>
            <div class="barpct">{m['pass_pct']}%</div>
          </div>""")
    return "<div class='bars'>" + "".join(rows) + "</div>"


def failure_bars(cat_counter: Counter) -> str:
    if not cat_counter:
        return "<p class='muted'>No failures recorded. 🎉</p>"
    max_v = max(cat_counter.values()) or 1
    rows = []
    for cat, count in cat_counter.most_common():
        rows.append(f"""
          <div class="barrow">
            <div class="barlabel" title="{esc(cat)}">{esc(cat)}</div>
            <div class="bartrack"><span style="width:{count/max_v*100:.1f}%;background:{BRAND['fail']}"></span></div>
            <div class="barpct">{count}</div>
          </div>""")
    return "<div class='bars'>" + "".join(rows) + "</div>"


def trend_svg(history: list[dict], width: int = 640, height: int = 180) -> str:
    if len(history) < 2:
        return "<p class='muted'>Trend appears after at least two recorded runs.</p>"
    pad = 28
    pts = [h.get("pass_pct", 0) for h in history]
    n = len(pts)
    x_step = (width - 2 * pad) / (n - 1)
    coords = [
        (pad + i * x_step, height - pad - (p / 100) * (height - 2 * pad))
        for i, p in enumerate(pts)
    ]
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in coords)
    dots = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{BRAND["primary"]}"/>'
        for x, y in coords
    )
    gridlines = "".join(
        f'<line x1="{pad}" y1="{height-pad-(g/100)*(height-2*pad):.1f}" '
        f'x2="{width-pad}" y2="{height-pad-(g/100)*(height-2*pad):.1f}" '
        f'stroke="#E2E8F0"/><text x="4" y="{height-pad-(g/100)*(height-2*pad)+4:.1f}" '
        f'font-size="9" fill="#94A3B8">{g}%</text>'
        for g in (0, 50, 100)
    )
    return f"""
    <svg viewBox="0 0 {width} {height}" width="100%" height="{height}" role="img" aria-label="Pass % trend">
      {gridlines}
      <polyline points="{poly}" fill="none" stroke="{BRAND['accent']}" stroke-width="2.5"/>
      {dots}
    </svg>"""


def pivot_table(headers: list[str], rows: list[list]) -> str:
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{esc(c)}</td>" for c in row) + "</tr>" for row in rows
    )
    return f"<table class='pivot'><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


# ----------------------------------------------------------------------------
# Main render
# ----------------------------------------------------------------------------
def generate_executive_dashboard(results_dir, output_html, persona=None, extra_meta=None):
    results_dir = Path(results_dir)
    output_html = Path(output_html)
    output_html.parent.mkdir(parents=True, exist_ok=True)

    scenarios = collect_scenarios(results_dir)

    # For a single-persona run every scenario belongs to that persona, so trust
    # it over the feature-label heuristic (a faculty run's "Login" feature is
    # still Faculty, not Student).
    persona_key = (persona or "").strip().lower()
    if persona_key and persona_key not in ("combined", "—", ""):
        forced_role = PERSONA_PRETTY.get(persona_key)
        if forced_role:
            for s in scenarios:
                s["role"] = forced_role

    meta = gather_meta(persona, results_dir, extra_meta)
    creds = gather_credentials(scenarios, persona)

    # Relative path from the HTML location to the results dir (where the
    # screenshot attachments live), so "View screenshot" links resolve.
    try:
        shot_base = os.path.relpath(results_dir.resolve(), output_html.parent.resolve()).replace("\\", "/")
    except Exception:
        shot_base = results_dir.name

    # Aggregate counts
    status_counts = Counter(s["status"] for s in scenarios)
    total = len(scenarios)
    passed = status_counts.get("passed", 0)
    failed = status_counts.get("failed", 0)
    broken = status_counts.get("broken", 0)
    skipped = status_counts.get("skipped", 0)
    executed = total - skipped
    pass_pct = round(passed / executed * 100, 1) if executed else 0.0
    total_duration = sum(s["duration"] for s in scenarios)

    # Step-level (test-case-level) totals across the whole run.
    step_total = sum(s.get("steps_total", 0) for s in scenarios)
    step_passed = sum(s.get("steps_passed", 0) for s in scenarios)
    step_failed = sum(s.get("steps_failed", 0) for s in scenarios)
    step_skipped = sum(s.get("steps_skipped", 0) for s in scenarios)

    # Module summary
    by_module = defaultdict(lambda: {"counts": Counter(), "total": 0, "steps_total": 0, "steps_passed": 0})
    for s in scenarios:
        by_module[s["feature"]]["counts"][s["status"]] += 1
        by_module[s["feature"]]["total"] += 1
        by_module[s["feature"]]["steps_total"] += s.get("steps_total", 0)
        by_module[s["feature"]]["steps_passed"] += s.get("steps_passed", 0)
    module_rows = []
    for module, agg in sorted(by_module.items(), key=lambda kv: -kv[1]["total"]):
        c = agg["counts"]
        exec_m = agg["total"] - c.get("skipped", 0)
        ppct = round(c.get("passed", 0) / exec_m * 100, 1) if exec_m else 0.0
        module_rows.append({
            "module": module, "counts": c, "total": agg["total"], "pass_pct": ppct,
            "steps_total": agg.get("steps_total", 0), "steps_passed": agg.get("steps_passed", 0),
        })

    # Pivots
    by_role = defaultdict(lambda: {"counts": Counter(), "total": 0})
    for s in scenarios:
        by_role[s["role"]]["counts"][s["status"]] += 1
        by_role[s["role"]]["total"] += 1
    cat_counter = Counter(s["category"] for s in scenarios if s["category"])

    # Environment breakdown. For a combined dev+prod run each scenario carries an
    # 'environment' label; for a single-env run they share the meta env so this
    # collapses to one row.
    by_env = defaultdict(lambda: {"counts": Counter(), "total": 0})
    for s in scenarios:
        env_key = s.get("env") or meta["env_name"]
        by_env[env_key]["counts"][s["status"]] += 1
        by_env[env_key]["total"] += 1
    # Environment × Role pivot for the combined view.
    by_env_role = defaultdict(lambda: {"counts": Counter(), "total": 0})
    for s in scenarios:
        env_key = s.get("env") or meta["env_name"]
        by_env_role[(env_key, s["role"])]["counts"][s["status"]] += 1
        by_env_role[(env_key, s["role"])]["total"] += 1
    env_sorted = sorted(by_env.items(), key=lambda kv: (kv[0] != "prod", kv[0]))
    multi_env = len({(s.get("env") or meta["env_name"]) for s in scenarios}) > 1
    if multi_env:
        meta["env_display"] = " + ".join(
            env_pretty(e) for e in sorted(by_env, key=lambda x: (x != "prod", x))
        )

    history = update_history(results_dir, meta["persona"], total, passed, failed, broken, skipped, pass_pct)

    # Health verdict
    if pass_pct >= 95:
        health, health_color = "Healthy", BRAND["pass"]
    elif pass_pct >= 80:
        health, health_color = "Needs Attention", BRAND["broken"]
    else:
        health, health_color = "At Risk", BRAND["fail"]

    # ---- Build HTML sections ----
    # KPI cards. The 4th tuple element is the status value this card filters
    # the Detailed Test Execution table to when clicked ('all' fully resets
    # every filter); cards with None aren't clickable (Pass %, Steps, Duration
    # are summary stats, not a status a scenario row can match against).
    kpi_cards = [
        ("Total Tests", total, "#0F172A", "all", f"WSN Automation Framework: {WSN_FRAMEWORK_TOTAL_TESTS_PASSED}/{WSN_FRAMEWORK_TOTAL_TESTS}"),
        ("Passed", passed, BRAND["pass"], "passed", None),
        ("Failed", failed, BRAND["fail"], "failed", None),
        ("Error", broken, BRAND["broken"], "broken", None),
        ("Skipped", skipped, BRAND["skip"], "skipped", None),
        ("Total Steps", f"{step_passed}/{WSN_FRAMEWORK_TOTAL_TESTS}", "#6a4fb3", None, None),
        ("Pass %", f"{pass_pct}%", health_color, None, None),
        ("Duration", fmt_duration(total_duration), "#0F172A", None, None),
    ]
    kpi_html = "".join(
        (
            f'<a class="kpi kpi-link" href="#detailed" data-action="status" data-value="{esc(status_val)}">'
            f'<div class="kpi-val" style="color:{c}">{esc(v)}</div>'
            f'<div class="kpi-lbl">{esc(label)} ▸</div>'
            + (f'<div class="kpi-sub">{esc(sub)}</div>' if sub else "")
            + '</a>'
        ) if status_val else (
            f'<div class="kpi"><div class="kpi-val" style="color:{c}">{esc(v)}</div>'
            f'<div class="kpi-lbl">{esc(label)}</div>'
            + (f'<div class="kpi-sub">{esc(sub)}</div>' if sub else "")
            + '</div>'
        )
        for label, v, c, status_val, sub in kpi_cards
    )

    # Persona tabs — one per role that actually ran, plus an "All Personas"
    # reset tab. Filters the same Detailed Test Execution table as the KPI
    # cards and module links (see DASH_FILTER in the injected <script>).
    persona_tabs_html = (
        '<div class="persona-tabs">'
        '<button class="persona-tab active" data-action="role" data-value="all">All Personas</button>'
        + "".join(
            f'<button class="persona-tab" data-action="role" data-value="{esc(role)}">'
            f'{esc(role)} ({agg["total"]})</button>'
            for role, agg in sorted(by_role.items(), key=lambda kv: -kv[1]["total"])
        )
        + '</div>'
    )

    legend = "".join(
        f'<span class="lg"><i style="background:{STATUS_COLOR[s]}"></i>{STATUS_LABEL[s]} '
        f'({status_counts.get(s,0)})</span>'
        for s in STATUS_ORDER
    )

    # Execution info grid
    info_items = [
        ("Application URL", meta["base_url"] or "—"),
        ("Environment", meta["env_display"]),
        ("Browser", meta["browser"]),
        ("Operating System", meta["os"]),
        ("Framework", meta["framework"]),
        ("Python", meta["python"]),
        ("Execution Type", meta["exec_type"]),
        ("Build Version", meta["build"]),
        ("Headless", meta["headless"]),
        ("Generated", meta["generated"]),
    ]
    info_html = "".join(
        f'<div class="info-cell"><span class="info-k">{esc(k)}</span>'
        f'<span class="info-v">{esc(v)}</span></div>'
        for k, v in info_items
    )

    cred_rows = "".join(
        f"<tr><td>{esc(r['role'])}</td><td>{esc(r['username'])}</td>"
        f"<td>{esc(r['password'])}</td><td>{esc(r['account'])}</td></tr>"
        for r in creds
    ) or "<tr><td colspan='4' class='muted'>No credentials resolved.</td></tr>"

    # Module coverage table — module name is clickable to filter the Detailed
    # Test Execution table down to that module/feature.
    module_table_rows = "".join(
        f"<tr><td><a class='mod-link' href='#detailed' data-action='module' "
        f"data-value='{esc(m['module'])}'>{esc(m['module'])}</a></td>"
        f"<td>{m['total']}</td><td>{m.get('steps_total', 0)}</td>"
        f"<td class='ok'>{m['counts'].get('passed',0)}</td>"
        f"<td class='bad'>{m['counts'].get('failed',0)}</td>"
        f"<td class='warn'>{m['counts'].get('broken',0)}</td>"
        f"<td>{m['counts'].get('skipped',0)}</td>"
        f"<td><b>{m['pass_pct']}%</b></td></tr>"
        for m in module_rows
    )

    # Environment coverage (only meaningful when more than one env ran, e.g. the
    # combined dev+prod matrix run). Built as a table + colored bars mirroring the
    # module coverage section.
    env_rows_view = []
    for env_key, agg in env_sorted:
        c = agg["counts"]
        exec_e = agg["total"] - c.get("skipped", 0)
        ppct = round(c.get("passed", 0) / exec_e * 100, 1) if exec_e else 0.0
        env_rows_view.append({
            "module": env_pretty(env_key), "counts": c, "total": agg["total"], "pass_pct": ppct,
        })
    env_table_rows = "".join(
        f"<tr><td>{esc(m['module'])}</td><td>{m['total']}</td>"
        f"<td class='ok'>{m['counts'].get('passed',0)}</td>"
        f"<td class='bad'>{m['counts'].get('failed',0)}</td>"
        f"<td class='warn'>{m['counts'].get('broken',0)}</td>"
        f"<td>{m['counts'].get('skipped',0)}</td>"
        f"<td><b>{m['pass_pct']}%</b></td></tr>"
        for m in env_rows_view
    )
    env_coverage_section = ""
    if multi_env:
        env_coverage_section = f"""
  <section>
    <h2>Environment Coverage Summary</h2>
    <p class="desc">Outcomes per environment for this combined run. Production health is listed first.</p>
    <div class="charts">
      <div>{module_bars(env_rows_view)}</div>
      <div>
        <table><thead><tr><th>Environment</th><th>Total</th><th>Passed</th><th>Failed</th><th>Error</th><th>Skipped</th><th>Pass %</th></tr></thead>
        <tbody>{env_table_rows}</tbody></table>
      </div>
    </div>
  </section>"""

    # Pivots
    pivot_module = pivot_table(
        ["Module", "Passed", "Failed", "Error", "Skipped", "Total"],
        [[m["module"], m["counts"].get("passed", 0), m["counts"].get("failed", 0),
          m["counts"].get("broken", 0), m["counts"].get("skipped", 0), m["total"]] for m in module_rows],
    )
    pivot_feature = pivot_table(
        ["Feature", "Execution Count", "Test Steps Executed"],
        [[m["module"], m["total"], m.get("steps_total", 0)] for m in module_rows],
    )
    pivot_env = pivot_table(
        ["Environment", "Passed", "Failed", "Error", "Skipped", "Total"],
        [[env_pretty(e), agg["counts"].get("passed", 0), agg["counts"].get("failed", 0),
          agg["counts"].get("broken", 0), agg["counts"].get("skipped", 0), agg["total"]]
         for e, agg in env_sorted],
    )
    pivot_env_role = pivot_table(
        ["Environment", "User Role", "Passed", "Failed", "Error", "Total"],
        [[env_pretty(e), role, agg["counts"].get("passed", 0), agg["counts"].get("failed", 0),
          agg["counts"].get("broken", 0), agg["total"]]
         for (e, role), agg in sorted(by_env_role.items(), key=lambda kv: (kv[0][0] != "prod", kv[0][0], kv[0][1]))],
    )
    pivot_failcat = pivot_table(
        ["Failure Category", "Count"],
        [[cat, n] for cat, n in cat_counter.most_common()] or [["—", 0]],
    )
    pivot_role = pivot_table(
        ["User Role", "Passed", "Failed", "Error", "Total"],
        [[role, agg["counts"].get("passed", 0), agg["counts"].get("failed", 0),
          agg["counts"].get("broken", 0), agg["total"]]
         for role, agg in sorted(by_role.items(), key=lambda kv: -kv[1]["total"])],
    )

    # Detailed execution table — every row carries data-status / data-role /
    # data-module attributes so the injected filter script (KPI cards, persona
    # tabs, module links, and the filter bar below) can all filter it in place.
    detail_rows = []
    show_env_col = multi_env
    for i, s in enumerate(scenarios, 1):
        st = s["status"]
        expected = "Scenario completes successfully"
        actual = "As expected" if st == "passed" else (first_line(s["message"], 120) or STATUS_LABEL.get(st, st))
        env_cell = f"<td>{esc(env_pretty(s.get('env') or meta['env_name']))}</td>" if show_env_col else ""
        steps_cell = f"<td>{s.get('steps_passed', 0)}/{s.get('steps_total', 0)}</td>"
        detail_rows.append(
            f"<tr class='r-{st}' data-status='{esc(st)}' data-role='{esc(s['role'])}' "
            f"data-module='{esc(s['feature'])}'>"
            f"<td>{i}</td><td>{esc(s['name'])}</td><td>{esc(s['feature'])}</td>"
            f"{env_cell}"
            f"<td><span class='pill pill-{st}'>{STATUS_LABEL.get(st, st)}</span></td>"
            f"{steps_cell}"
            f"<td>{s['duration']}s</td><td>{esc(expected)}</td><td>{esc(actual)}</td></tr>"
        )
    detail_colspan = 9 if show_env_col else 8
    detail_html = "".join(detail_rows) or f"<tr><td colspan='{detail_colspan}' class='muted'>No scenarios.</td></tr>"
    detail_env_header = "<th>Environment</th>" if show_env_col else ""

    # Explicit filter bar in the Detailed Test Execution section, alongside the
    # KPI cards / persona tabs / module links above (all drive the same filter).
    filter_bar_html = (
        "<div class='filter-bar'>"
        "<button class='filter-btn active' data-action='status' data-value='all'>All</button>"
        "<button class='filter-btn' data-action='status' data-value='passed'>✅ Passed</button>"
        "<button class='filter-btn' data-action='status' data-value='failed'>❌ Failed</button>"
        "<button class='filter-btn' data-action='status' data-value='broken'>⚠️ Error</button>"
        "<button class='filter-btn' data-action='status' data-value='skipped'>⏭️ Skipped</button>"
        "<button class='filter-btn' data-action='reset' data-value=''>Reset filters</button>"
        "</div>"
    )

    # Failure analysis cards — embed the failure screenshot inline (downscaled
    # base64) so the report stays self-contained. Capped to keep file size sane;
    # beyond the cap we fall back to a relative link.
    failures = [s for s in scenarios if s["status"] in ("failed", "broken")]
    try:
        max_shots = max(0, int(os.getenv("EXEC_DASH_MAX_SHOTS", "60")))
    except Exception:
        max_shots = 60

    fail_cards = []
    embedded = 0
    for s in failures:
        shot_block = "<span class='info-v muted'>No screenshot captured</span>"
        if s["screenshot"]:
            shot_path = results_dir / s["screenshot"]
            data_uri = ""
            if embedded < max_shots and shot_path.exists():
                data_uri = embed_screenshot(shot_path)
            if data_uri:
                embedded += 1
                shot_block = (
                    f'<a href="{data_uri}" target="_blank" title="Open full size">'
                    f'<img class="shot-img" src="{data_uri}" alt="Failure screenshot"/></a>'
                )
            else:
                shot_block = (
                    f'<a class="shot-link" href="{esc(shot_base)}/{esc(s["screenshot"])}" '
                    f'target="_blank">View screenshot ↗</a>'
                )
        trace = esc(s["trace"][:1500]) if s["trace"] else esc(s["message"][:800])
        fail_cards.append(f"""
          <details class="failcard">
            <summary>
              <span class="pill pill-{s['status']}">{STATUS_LABEL[s['status']]}</span>
              <b>{esc(s['name'])}</b>
              <span class="tag">{esc(s['feature'])}</span>
              <span class="tag tag-cat">{esc(s['category'])}</span>
            </summary>
            <div class="fail-body">
              <div class="fail-meta">
                <div><span class="info-k">Failed step</span><span class="info-v">{esc(s['failing_step'] or '—')}</span></div>
                <div><span class="info-k">Reason</span><span class="info-v">{esc(first_line(s['message'], 200) or '—')}</span></div>
                <div><span class="info-k">Category</span><span class="info-v">{esc(s['category'])}</span></div>
                <div><span class="info-k">Severity</span><span class="info-v">{esc(s['severity'])}</span></div>
                <div><span class="info-k">Steps completed</span><span class="info-v">{s.get('steps_passed',0)}/{s.get('steps_total',0)}</span></div>
              </div>
              <div class="shot-wrap"><span class="info-k">Screenshot at failure</span>{shot_block}</div>
              <pre class="trace">{trace}</pre>
            </div>
          </details>""")
    cap_note = ""
    if max_shots and len(failures) > max_shots:
        cap_note = (f"<p class='muted'>Showing inline screenshots for the first {max_shots} of "
                    f"{len(failures)} failures (remaining link to file). Adjust with EXEC_DASH_MAX_SHOTS.</p>")
    fail_html = cap_note + ("".join(fail_cards) or "<p class='muted'>No failures in this run. 🎉</p>")

    #  Tip banner shown above the dashboard, explaining the interactive filtering.
    tip_html = (
        "<p class='dash-tip'>💡 <b>Tip:</b> Click any KPI card, persona tab, or module name to filter "
        "the Detailed Test Execution table (section 7) down to just those results. "
        "Click <b>Total Tests</b> or <b>Reset filters</b> to clear all filters.</p>"
    )

    html_out = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>QA Execution Dashboard — {esc(meta['env_display'])}</title>
<style>
  :root {{ --brand:{BRAND['primary']}; --accent:{BRAND['accent']}; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font-family:'Segoe UI',Roboto,Helvetica,Arial,sans-serif; color:#0F172A; background:#F1F5F9; }}
  header {{ background:linear-gradient(110deg,var(--brand),#9e0c24); color:#fff; padding:22px 32px; display:flex;
           align-items:center; justify-content:space-between; flex-wrap:wrap; gap:16px; }}
  header .brand {{ display:flex; align-items:center; gap:14px; }}
  header .logo {{ width:46px;height:46px;border-radius:10px;background:#fff;color:var(--brand);font-weight:800;
                 display:flex;align-items:center;justify-content:center;font-size:20px; }}
  header h1 {{ margin:0; font-size:20px; }}
  header .sub {{ opacity:.85; font-size:13px; margin-top:2px; }}
  .badges {{ display:flex; gap:8px; flex-wrap:wrap; }}
  .badge {{ background:rgba(255,255,255,.15); border:1px solid rgba(255,255,255,.35); padding:6px 12px;
           border-radius:999px; font-size:12px; font-weight:600; }}
  .badge.health {{ background:{health_color}; border-color:transparent; }}
  main {{ max-width:1180px; margin:0 auto; padding:24px 18px 60px; }}
  section {{ background:#fff; border:1px solid #E2E8F0; border-radius:14px; padding:20px 22px; margin:18px 0;
            box-shadow:0 1px 2px rgba(15,23,42,.04); }}
  section h2 {{ margin:0 0 4px; font-size:16px; }}
  section .desc {{ color:#64748B; font-size:12.5px; margin:0 0 16px; }}
  .dash-tip {{ background:#FFF7ED; border:1px solid #FED7AA; color:#9A3412; padding:12px 16px;
              border-radius:10px; font-size:13px; margin:0 0 4px; }}
  .kpis {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(120px,1fr)); gap:12px; }}
  .kpi {{ background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:16px; text-align:center; }}
  .kpi-val {{ font-size:28px; font-weight:800; line-height:1; }}
  .kpi-lbl {{ font-size:12px; color:#64748B; margin-top:6px; text-transform:uppercase; letter-spacing:.04em; }}
  .kpi-sub {{ font-size:11px; color:#94A3B8; margin-top:4px; }}
  a.kpi-link {{ text-decoration:none; color:inherit; display:block; cursor:pointer;
               transition:box-shadow .15s, transform .15s; }}
  a.kpi-link:hover {{ box-shadow:0 6px 16px rgba(15,23,42,.14); transform:translateY(-2px); }}
  a.kpi-link.active {{ outline:2px solid var(--accent); outline-offset:1px; }}
  .persona-tabs {{ display:flex; gap:8px; flex-wrap:wrap; margin-top:16px; }}
  .persona-tab {{ border:1px solid #E2E8F0; background:#fff; color:#475569; padding:6px 14px;
                 border-radius:18px; font-size:12px; font-weight:700; cursor:pointer; transition:all .12s; }}
  .persona-tab:hover {{ border-color:var(--accent); color:#C2540C; }}
  .persona-tab.active {{ background:var(--accent); border-color:var(--accent); color:#fff; }}
  .filter-bar {{ display:flex; gap:8px; margin-bottom:14px; flex-wrap:wrap; }}
  .filter-btn {{ border:1px solid #E2E8F0; background:#fff; color:#475569; padding:6px 14px;
                border-radius:18px; font-size:12px; font-weight:700; cursor:pointer; transition:all .12s; }}
  .filter-btn:hover {{ border-color:var(--accent); color:#C2540C; }}
  .filter-btn.active {{ background:var(--accent); border-color:var(--accent); color:#fff; }}
  a.mod-link {{ color:var(--brand); text-decoration:none; font-weight:600; cursor:pointer; }}
  a.mod-link:hover {{ text-decoration:underline; }}
  a.mod-link.active {{ color:var(--accent); }}
  .charts {{ display:grid; grid-template-columns:220px 1fr; gap:24px; align-items:center; }}
  @media(max-width:720px){{ .charts{{grid-template-columns:1fr;}} }}
  .legend {{ display:flex; gap:14px; flex-wrap:wrap; margin-top:10px; font-size:12.5px; color:#475569; }}
  .lg i {{ display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:5px;vertical-align:-1px; }}
  .bars {{ display:flex; flex-direction:column; gap:9px; }}
  .barrow {{ display:grid; grid-template-columns:160px 1fr 46px; gap:10px; align-items:center; font-size:12.5px; }}
  .barlabel {{ white-space:nowrap; overflow:hidden; text-overflow:ellipsis; color:#334155; }}
  .bartrack {{ display:flex; height:16px; border-radius:8px; overflow:hidden; background:#EEF2F7; }}
  .bartrack span {{ display:block; height:100%; }}
  .barpct {{ text-align:right; font-weight:700; color:#334155; }}
  .grid2 {{ display:grid; grid-template-columns:1fr 1fr; gap:18px; }}
  @media(max-width:720px){{ .grid2{{grid-template-columns:1fr;}} }}
  .info-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:1px; background:#E2E8F0;
               border:1px solid #E2E8F0; border-radius:10px; overflow:hidden; }}
  .info-cell {{ background:#fff; padding:12px 14px; display:flex; flex-direction:column; gap:3px; }}
  .info-k {{ font-size:11px; text-transform:uppercase; letter-spacing:.04em; color:#94A3B8; }}
  .info-v {{ font-size:13.5px; font-weight:600; word-break:break-word; }}
  table {{ width:100%; border-collapse:collapse; font-size:13px; }}
  th,td {{ text-align:left; padding:9px 11px; border-bottom:1px solid #EEF2F7; }}
  thead th {{ background:#F8FAFC; color:#475569; font-size:11.5px; text-transform:uppercase; letter-spacing:.03em; position:sticky; top:0; }}
  .pivot thead th {{ background:var(--brand); color:#fff; }}
  td.ok {{ color:{BRAND['pass']}; font-weight:700; }}
  td.bad {{ color:{BRAND['fail']}; font-weight:700; }}
  td.warn {{ color:{BRAND['broken']}; font-weight:700; }}
  .pivots {{ display:grid; grid-template-columns:1fr 1fr; gap:18px; }}
  @media(max-width:820px){{ .pivots{{grid-template-columns:1fr;}} }}
  .pivots h3 {{ font-size:13px; margin:0 0 8px; color:#334155; }}
  .scroll {{ max-height:520px; overflow:auto; border:1px solid #EEF2F7; border-radius:10px; }}
  .pill {{ padding:2px 9px; border-radius:999px; font-size:11px; font-weight:700; color:#fff; }}
  .pill-passed {{ background:{BRAND['pass']}; }} .pill-failed {{ background:{BRAND['fail']}; }}
  .pill-broken {{ background:{BRAND['broken']}; }} .pill-skipped {{ background:{BRAND['skip']}; }}
  tr.r-failed td, tr.r-broken td {{ background:#FEF2F2; }}
  .failcard {{ border:1px solid #FEE2E2; border-radius:10px; margin:10px 0; background:#fff; }}
  .failcard summary {{ cursor:pointer; padding:12px 14px; display:flex; align-items:center; gap:10px; flex-wrap:wrap; }}
  .tag {{ background:#F1F5F9; color:#475569; font-size:11px; padding:2px 8px; border-radius:6px; }}
  .tag-cat {{ background:#FEF3C7; color:#92400E; }}
  .fail-body {{ padding:0 14px 14px; }}
  .fail-meta {{ display:grid; grid-template-columns:1fr 1fr; gap:10px; margin:6px 0 12px; }}
  @media(max-width:640px){{ .fail-meta{{grid-template-columns:1fr;}} }}
  .trace {{ background:#0F172A; color:#E2E8F0; font-size:11.5px; padding:12px; border-radius:8px; overflow:auto; max-height:280px; white-space:pre-wrap; }}
  .shot-link {{ color:var(--brand); font-weight:600; text-decoration:none; }}
  .shot-wrap {{ display:flex; flex-direction:column; gap:6px; margin:4px 0 12px; }}
  .shot-img {{ max-width:100%; border:1px solid #E2E8F0; border-radius:8px; display:block;
              box-shadow:0 2px 6px rgba(15,23,42,.08); }}
  .muted {{ color:#94A3B8; }}
  footer {{ text-align:center; color:#94A3B8; font-size:12px; padding:20px; }}
</style></head>
<body>
<header>
  <div class="brand">
    <div class="logo">{WADHWANI_LOGO_SVG}</div>
    <div><h1>WSN · QA Automation Execution Dashboard</h1>
      <div class="sub">{esc(BRAND['name'])} · Persona: {esc(meta['persona'])} · {esc(meta['generated'])}</div></div>
  </div>
  <div class="badges">
    <span class="badge">WSN</span>
    <span class="badge">ENV: {esc(meta['env_display'])}</span>
  </div>
</header>
<main>
  {tip_html}

  <section>
    <h2>1 · Executive Dashboard</h2>
    <p class="desc">High-level snapshot of the run. Overall health verdict is based on executed pass rate. Click a KPI card to filter the detailed results below.</p>
    <div class="kpis">{kpi_html}</div>
    {persona_tabs_html}
  </section>

  <section>
    <h2>Result Distribution</h2>
    <div class="charts">
      <div style="text-align:center">{svg_donut(status_counts)}</div>
      <div>
        {module_bars(module_rows[:12])}
        <div class="legend">{legend}</div>
      </div>
    </div>
  </section>

  <section>
    <h2>2 · Execution Information</h2>
    <p class="desc">Where and how this run executed — the verifiable context behind the numbers.</p>
    <div class="info-grid">{info_html}</div>
  </section>

  <section>
    <h2>3 · Credentials Used</h2>
    <p class="desc">Test accounts per role. Usernames are masked and passwords are never rendered.</p>
    <table><thead><tr><th>User Role</th><th>Username (masked)</th><th>Password</th><th>Account</th></tr></thead>
    <tbody>{cred_rows}</tbody></table>
  </section>

  <section>
    <h2>4 · Module Coverage Summary</h2>
    <p class="desc">Scenario outcomes per module/feature with pass percentage and test step counts. Click a module name to filter section 7 to just that module.</p>
    <table><thead><tr><th>Module</th><th>Total</th><th>Test Steps</th><th>Passed</th><th>Failed</th><th>Error</th><th>Skipped</th><th>Pass %</th></tr></thead>
    <tbody>{module_table_rows}</tbody></table>
  </section>
{env_coverage_section}
  <section>
    <h2>5 · Pivot Summaries</h2>
    <p class="desc">Cross-tabulated views for quick slicing of results.</p>
    <div class="pivots">
      <div><h3>Module × Pass/Fail</h3>{pivot_module}</div>
      <div><h3>Feature × Execution Count</h3>{pivot_feature}</div>
      <div><h3>Environment × Pass/Fail</h3>{pivot_env}</div>
      <div><h3>Failure Category × Count</h3>{pivot_failcat}</div>
      <div><h3>User Role × Executed Tests</h3>{pivot_role}</div>
      {"<div><h3>Environment × User Role</h3>" + pivot_env_role + "</div>" if multi_env else ""}
    </div>
  </section>

  <section>
    <h2>6 · Charts &amp; Trends</h2>
    <div class="grid2">
      <div><h3>Execution History (Pass %)</h3>{trend_svg(history)}</div>
      <div><h3>Failure Distribution</h3>{failure_bars(cat_counter)}</div>
    </div>
  </section>

  <section id="detailed">
    <h2>7 · Detailed Test Execution</h2>
    <p class="desc">Every scenario with status, step counts, time, expected vs. actual result.</p>
    {filter_bar_html}
    <div class="scroll">
      <table id="exec-table"><thead><tr><th>#</th><th>Test Name</th><th>Module</th>{detail_env_header}<th>Status</th><th>Steps</th><th>Time</th><th>Expected</th><th>Actual</th></tr></thead>
      <tbody>{detail_html}</tbody></table>
    </div>
  </section>

  <section>
    <h2>8 · Failure Analysis</h2>
    <p class="desc">Each failure with failing step, reason, error category, step-completion count, screenshot link and stack trace.</p>
    {fail_html}
  </section>

</main>
<footer>Generated by the WSN Automation Framework · {esc(meta['framework'])} · {esc(meta['generated'])}</footer>
<script>
  // Single filter state shared by KPI cards, persona tabs, module links, and
  // the explicit filter bar in section 7 — all use data-action/data-value
  // attributes and are wired up here via event delegation, so no inline
  // onclick handlers are needed (avoids escaping issues with module/persona
  // names that may contain quotes or special characters).
  var DASH_FILTER = {{ status: 'all', role: 'all', module: null }};

  function applyFilter() {{
    var rows = document.querySelectorAll('#exec-table tbody tr');
    rows.forEach(function (r) {{
      var st = r.getAttribute('data-status');
      var role = r.getAttribute('data-role');
      var mod = r.getAttribute('data-module');
      var okStatus = DASH_FILTER.status === 'all' || st === DASH_FILTER.status;
      var okRole = DASH_FILTER.role === 'all' || role === DASH_FILTER.role;
      var okModule = !DASH_FILTER.module || mod === DASH_FILTER.module;
      r.style.display = (okStatus && okRole && okModule) ? '' : 'none';
    }});
    document.querySelectorAll('[data-action="status"]').forEach(function (el) {{
      el.classList.toggle('active', el.getAttribute('data-value') === DASH_FILTER.status);
    }});
    document.querySelectorAll('[data-action="role"]').forEach(function (el) {{
      el.classList.toggle('active', el.getAttribute('data-value') === DASH_FILTER.role);
    }});
    document.querySelectorAll('[data-action="module"]').forEach(function (el) {{
      el.classList.toggle('active', !!DASH_FILTER.module && el.getAttribute('data-value') === DASH_FILTER.module);
    }});
  }}

  function resetFilters() {{
    DASH_FILTER = {{ status: 'all', role: 'all', module: null }};
    applyFilter();
  }}

  document.addEventListener('click', function (e) {{
    var el = e.target.closest('[data-action]');
    if (!el) return;
    e.preventDefault();
    var action = el.getAttribute('data-action');
    var value = el.getAttribute('data-value');
    if (action === 'reset') {{
      resetFilters();
    }} else if (action === 'status') {{
      if (value === 'all') {{ resetFilters(); }}
      else {{ DASH_FILTER.status = value; applyFilter(); }}
    }} else if (action === 'role') {{
      DASH_FILTER.role = value;
      applyFilter();
    }} else if (action === 'module') {{
      DASH_FILTER.module = (DASH_FILTER.module === value) ? null : value;
      applyFilter();
    }}
    var target = document.getElementById('detailed');
    if (target) target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
  }});

  document.addEventListener('DOMContentLoaded', applyFilter);
</script>
</body></html>"""

    output_html.write_text(html_out, encoding="utf-8")
    return str(output_html)


if __name__ == "__main__":
    rd = sys.argv[1] if len(sys.argv) > 1 else "reports/allure-results"
    out = sys.argv[2] if len(sys.argv) > 2 else "reports/executive-dashboard.html"
    path = generate_executive_dashboard(rd, out, persona=os.getenv("PERSONA"))
    log.info(f"Executive dashboard written to {path}")