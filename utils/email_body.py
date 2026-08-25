"""
Builds the HTML execution-summary email that mirrors the manually shared
"WSN Prod Web Automation – Summary/Report" mail.

Structure produced (in order):
    1. Greeting                     "Hi Team,"
    2. Execution introduction       "Please find the WSN Production Environment …"
    3. HTML summary table           bordered metric/value table
    4. "Summary:" heading
    5. Detailed execution summary   counts written out as prose
    6. Error/failure explanation    derived from real classify_failure() buckets
    7. Overall execution observation + report-generation status sentence
    8. Closing / signature

Every number and every persona name comes from utils.report_stats — nothing in
this module is hardcoded, and no failure reason is invented: when the execution
data carries no error message the wording degrades to an accurate generic
statement instead of guessing.
"""

from __future__ import annotations

import html

from utils.report_stats import CATEGORY_PHRASE, _join

# How many individual failing scenarios are itemised under the narrative before
# the list is truncated (the full detail lives in the attached report).
MAX_ITEMISED_FAILURES = 8


def esc(value) -> str:
    return html.escape("" if value is None else str(value))


# ---------------------------------------------------------------------------
# Subject
# ---------------------------------------------------------------------------
def build_subject(stats: dict, cfg: dict) -> str:
    template = cfg.get("subject_template") or "{product} {env_short} {application} – Summary/Report"
    subject = template.format(
        product=cfg.get("product", "WSN"),
        application=cfg.get("application", "Web Automation"),
        env_short=stats.get("env_short") or "",
        env_display=stats.get("env_display") or "",
    )
    # Collapse the double space left behind when env_short is empty.
    return " ".join(subject.split())


# ---------------------------------------------------------------------------
# Narrative pieces
# ---------------------------------------------------------------------------
def _intro_sentence(stats: dict, cfg: dict) -> str:
    """'Please find the WSN Production Environment execution summary below.'"""
    product = cfg.get("product", "WSN")
    env_display = stats.get("env_display") or ""
    if not env_display or env_display == "—":
        return f"Please find the {product} execution summary below."
    if len(stats.get("env_keys", [])) > 1:
        return f"Please find the {product} {env_display} execution summary below."
    return f"Please find the {product} {env_display} Environment execution summary below."


def _headline_paragraph(stats: dict, cfg: dict) -> str:
    """Counts written out as prose — only non-zero buckets are mentioned."""
    product = cfg.get("product", "WSN")
    env_short = stats.get("env_short") or ""
    application = cfg.get("application", "Web Automation")
    run_name = " ".join(x for x in (product, env_short, application) if x)

    total = stats["total"]
    if not total:
        return (f"The {run_name} execution did not produce any scenario results. "
                "Please check the execution logs for details.")

    clauses = []
    if stats["passed"]:
        clauses.append(f"{stats['passed']} scenario{'s' if stats['passed'] != 1 else ''} passed")
    if stats["failed"]:
        clauses.append(f"{stats['failed']} failed")
    if stats["broken"]:
        clauses.append(f"{stats['broken']} had error{'s' if stats['broken'] != 1 else ''}")
    if stats["skipped"]:
        clauses.append(f"{stats['skipped']} {'were' if stats['skipped'] != 1 else 'was'} skipped")

    body = _join(clauses) if clauses else "no scenarios were executed"
    return (f"The {run_name} execution was completed with {total} scenario"
            f"{'s' if total != 1 else ''}. {body[0].upper() + body[1:]}, "
            f"with an overall pass percentage of {stats['pass_pct']}%.")


def _failure_paragraph(stats: dict) -> str:
    """Explain the failures/errors using the categories the run actually emitted."""
    failures = stats.get("failures") or []
    if not failures:
        return ""

    category_counts = stats.get("category_counts", {})
    category_roles = stats.get("category_roles", {})

    # Categories ordered by how many scenarios they account for.
    ordered = sorted(category_counts.items(), key=lambda kv: -kv[1])

    sentences = []
    known = [(c, n) for c, n in ordered if c != "Unknown"]
    if known:
        primary_cat, primary_n = known[0]
        phrase = CATEGORY_PHRASE.get(primary_cat, primary_cat.lower())
        roles = category_roles.get(primary_cat, [])
        role_text = f" in the {_join(roles)} flow{'s' if len(roles) != 1 else ''}" if roles else ""
        lead = "The errors were mainly due to" if len(ordered) > 1 or primary_n > 1 else "The issue was caused by"
        sentences.append(f"{lead} {phrase}{role_text}.")

        for cat, n in known[1:]:
            phrase = CATEGORY_PHRASE.get(cat, cat.lower())
            roles = category_roles.get(cat, [])
            role_text = f" in the {_join(roles)} flow{'s' if len(roles) != 1 else ''}" if roles else ""
            sentences.append(
                f"A further {n} scenario{'s' if n != 1 else ''} reported {phrase}{role_text}.")

    unknown_n = category_counts.get("Unknown", 0)
    if unknown_n:
        roles = category_roles.get("Unknown", [])
        role_text = f" in the {_join(roles)} flow{'s' if len(roles) != 1 else ''}" if roles else ""
        sentences.append(
            f"{unknown_n} scenario{'s' if unknown_n != 1 else ''}{role_text} did not carry a captured "
            "error message; please refer to the attached report for the execution detail.")

    return " ".join(sentences)


def _skipped_paragraph(stats: dict) -> str:
    n = stats.get("skipped", 0)
    if not n:
        return ""
    roles = stats.get("skipped_roles") or []
    role_text = f" in the {_join(roles)} flow{'s' if len(roles) != 1 else ''}" if roles else ""
    # Use the reason recorded by the run when there is one; never invent one.
    reasons = [d["message"] for d in stats.get("skipped_details", []) if d.get("message")]
    if reasons:
        unique = []
        for r in reasons:
            if r not in unique:
                unique.append(r)
        reason_text = f" Reported reason: {unique[0]}" + (" (and similar)." if len(unique) > 1 else ".")
    else:
        reason_text = " These scenarios did not execute in this run."
    return (f"{n} scenario{'s' if n != 1 else ''}{role_text} "
            f"{'were' if n != 1 else 'was'} skipped.{reason_text}")


def _clean_flows_paragraph(stats: dict) -> str:
    clean = stats.get("clean_roles") or []
    if not clean:
        return ""
    return (f"The {_join(clean)} flow{'s' if len(clean) != 1 else ''} "
            f"{'were' if len(clean) != 1 else 'was'} completed successfully.")


def _outcome_sentence(stats: dict, report_generated: bool) -> str:
    """Meaningful outcome text — never a bare PASSED/FAILED.

    Report-generation status is evaluated independently of test status.
    """
    if not report_generated:
        return ("The automation execution was completed, but the automation report could not be "
                "generated successfully. Please check the execution logs.")
    if not stats.get("has_results"):
        return ("The automation execution did not produce any scenario results, although the report "
                "generation step completed. Please check the execution logs.")
    if stats.get("failed"):
        return ("The automation execution was completed with test failures, and the report was "
                "generated successfully. Please refer to the detailed report for the failed scenarios.")
    if stats.get("broken"):
        return ("The automation execution was completed with some errors, and the report was "
                "generated successfully. The errors are detailed above for reference.")
    return ("The automation execution was completed successfully, and the report was generated "
            "successfully.")


# ---------------------------------------------------------------------------
# HTML assembly
# ---------------------------------------------------------------------------
_TABLE_ROW_KEYS = [
    ("Total Scenarios", "total"),
    ("Passed", "passed"),
    ("Failed", "failed"),
    ("Error", "broken"),
    ("Skipped", "skipped"),
]

TD = "border:1px solid #000;padding:4px 8px;font-family:Calibri,Arial,sans-serif;font-size:11pt;"


def _summary_table(stats: dict, cfg: dict) -> str:
    rows = [(label, stats.get(key, 0)) for label, key in _TABLE_ROW_KEYS]
    rows.append(("Pass percentage", f"{stats.get('pass_pct', 0)}%"))
    rows.append(("Total steps", stats.get("steps_display", "—")))
    rows.append(("Execution time", stats.get("duration_human", "—")))
    # Context rows that make the mail self-describing without changing the
    # familiar shape of the original table.
    rows.append(("Environment", stats.get("env_display", "—")))
    rows.append(("Application", f"{cfg.get('product', 'WSN')} {cfg.get('application', 'Web Automation')}"))

    body = "".join(
        f'<tr><td style="{TD}">{esc(label)}</td>'
        f'<td style="{TD}">{esc(value)}</td></tr>'
        for label, value in rows
    )
    return (
        '<table cellspacing="0" cellpadding="0" '
        'style="border-collapse:collapse;border:1px solid #000;">'
        f"<tbody>{body}</tbody></table>"
    )


def _failure_table(stats: dict) -> str:
    """Itemised failing scenarios — only rendered when there are any."""
    failures = stats.get("failures") or []
    if not failures:
        return ""
    shown = failures[:MAX_ITEMISED_FAILURES]
    head = (
        f'<tr>'
        f'<th style="{TD}background:#f2f2f2;text-align:left;">Flow</th>'
        f'<th style="{TD}background:#f2f2f2;text-align:left;">Scenario</th>'
        f'<th style="{TD}background:#f2f2f2;text-align:left;">Status</th>'
        f'<th style="{TD}background:#f2f2f2;text-align:left;">Observed issue</th>'
        f'</tr>'
    )
    body = "".join(
        f'<tr><td style="{TD}">{esc(f["role"])}</td>'
        f'<td style="{TD}">{esc(f["scenario"])}</td>'
        f'<td style="{TD}">{esc("Error" if f["status"] == "broken" else "Failed")}</td>'
        f'<td style="{TD}">{esc(f["category"])}'
        + (f'<br><span style="color:#555;font-size:10pt;">{esc(f["message"])}</span>' if f["message"] else "")
        + "</td></tr>"
        for f in shown
    )
    more = ""
    if len(failures) > len(shown):
        more = (f'<p style="font-family:Calibri,Arial,sans-serif;font-size:10pt;color:#555;">'
                f'…and {len(failures) - len(shown)} more — see the attached report for the full list.</p>')
    return (
        '<p style="font-family:Calibri,Arial,sans-serif;font-size:11pt;"><b>Failure / Error details:</b></p>'
        '<table cellspacing="0" cellpadding="0" style="border-collapse:collapse;border:1px solid #000;">'
        f"<tbody>{head}{body}</tbody></table>{more}"
    )


def _persona_table(stats: dict) -> str:
    """Per-flow roll-up, so readers see which persona contributed what."""
    rows = stats.get("role_rows") or []
    if len(rows) < 2:
        return ""
    head = (
        f'<tr>'
        f'<th style="{TD}background:#f2f2f2;text-align:left;">Flow / Persona</th>'
        f'<th style="{TD}background:#f2f2f2;">Total</th>'
        f'<th style="{TD}background:#f2f2f2;">Passed</th>'
        f'<th style="{TD}background:#f2f2f2;">Failed</th>'
        f'<th style="{TD}background:#f2f2f2;">Error</th>'
        f'<th style="{TD}background:#f2f2f2;">Skipped</th>'
        f'<th style="{TD}background:#f2f2f2;">Pass %</th>'
        f'</tr>'
    )
    body = "".join(
        f'<tr><td style="{TD}">{esc(r["role"])}</td>'
        f'<td style="{TD}text-align:center;">{r["total"]}</td>'
        f'<td style="{TD}text-align:center;">{r["passed"]}</td>'
        f'<td style="{TD}text-align:center;">{r["failed"]}</td>'
        f'<td style="{TD}text-align:center;">{r["broken"]}</td>'
        f'<td style="{TD}text-align:center;">{r["skipped"]}</td>'
        f'<td style="{TD}text-align:center;"><b>{r["pass_pct"]}%</b></td></tr>'
        for r in rows
    )
    return (
        '<p style="font-family:Calibri,Arial,sans-serif;font-size:11pt;"><b>Flow-wise breakdown:</b></p>'
        '<table cellspacing="0" cellpadding="0" style="border-collapse:collapse;border:1px solid #000;">'
        f"<tbody>{head}{body}</tbody></table>"
    )


P = 'style="font-family:Calibri,Arial,sans-serif;font-size:11pt;margin:10px 0;"'


def build_email_html(stats: dict, cfg: dict, report_generated: bool = True,
                     attachment_name: str | None = None) -> str:
    """Assemble the complete HTML email body."""
    paragraphs = [
        _headline_paragraph(stats, cfg),
        _failure_paragraph(stats),
        _skipped_paragraph(stats),
        _clean_flows_paragraph(stats),
        _outcome_sentence(stats, report_generated),
    ]
    narrative = "".join(f"<p {P}>{esc(p)}</p>" for p in paragraphs if p)

    if report_generated and attachment_name:
        attach_note = (f'<p {P}>The detailed HTML execution report '
                       f'(<b>{esc(attachment_name)}</b>) is attached to this email.</p>')
    elif not report_generated:
        attach_note = (f'<p {P}><b>Note:</b> the detailed HTML report could not be generated for this '
                       f'run, so no report is attached.</p>')
    else:
        attach_note = ""

    signature = cfg.get("signature", "")

    return f"""<html><body style="font-family:Calibri,Arial,sans-serif;font-size:11pt;color:#000;">
<p {P}>Hi Team,</p>
<p {P}>{esc(_intro_sentence(stats, cfg))}</p>
{_summary_table(stats, cfg)}
<p {P}><b>Summary:</b></p>
{narrative}
{_persona_table(stats)}
{_failure_table(stats)}
{attach_note}
<p {P}>Thanks,<br>{esc(signature)}</p>
</body></html>"""
