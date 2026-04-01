"""
Generate a comprehensive student persona PDF report by reading the feature file
directly, so all scenarios and steps are included regardless of allure result gaps.
"""
import json
from pathlib import Path
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import mm


def parse_feature(feature_path):
    scenarios = []
    current = None
    for line in Path(feature_path).read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("Scenario:"):
            if current:
                scenarios.append(current)
            current = {"name": stripped[len("Scenario:"):].strip(), "steps": []}
        elif current and any(
            stripped.startswith(kw)
            for kw in ("Then ", "Given ", "When ", "And ", "But ")
        ):
            current["steps"].append(stripped)
    if current:
        scenarios.append(current)
    return scenarios


def load_statuses(results_dir):
    status_map = {}
    for f in Path(results_dir).glob("*-result.json"):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
            name = d.get("name", "")
            status = d.get("status", "unknown")
            # Keep best status if duplicates
            existing = status_map.get(name)
            if existing != "passed":
                status_map[name] = status
        except Exception:
            continue
    return status_map


def generate(feature_path, results_dir, out_pdf):
    scenarios = parse_feature(feature_path)
    status_map = load_statuses(results_dir)

    total = len(scenarios)
    passed = sum(1 for s in scenarios if status_map.get(s["name"]) == "passed")
    failed = sum(1 for s in scenarios if status_map.get(s["name"]) == "failed")
    broken = sum(1 for s in scenarios if status_map.get(s["name"]) == "broken")
    not_recorded = total - passed - failed - broken

    doc = SimpleDocTemplate(
        out_pdf, pagesize=A4,
        leftMargin=15 * mm, rightMargin=15 * mm,
        topMargin=15 * mm, bottomMargin=15 * mm,
    )
    styles = getSampleStyleSheet()
    small = ParagraphStyle("small", parent=styles["Normal"], fontSize=8, leading=11)
    step_style = ParagraphStyle(
        "step", parent=styles["Normal"], fontSize=8, leading=11,
        leftIndent=10, textColor=colors.HexColor("#374151"),
    )

    elements = []
    elements.append(Paragraph("Student Persona — Test Execution Report", styles["Title"]))
    elements.append(Paragraph(
        f"Feature: {Path(feature_path).name}  |  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        small,
    ))
    elements.append(Spacer(1, 8 * mm))

    # Summary table
    summary = [
        ["Total", "Passed", "Failed", "Broken", "Not Recorded"],
        [str(total), str(passed), str(failed), str(broken), str(not_recorded)],
    ]
    st = Table(summary, colWidths=[72, 72, 72, 72, 90])
    st.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F3A5F")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#EFF6FF")),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
    ]))
    elements.append(st)
    elements.append(Spacer(1, 8 * mm))
    elements.append(Paragraph("Scenario Details", styles["Heading2"]))
    elements.append(Spacer(1, 3 * mm))

    STATUS_COLOR = {
        "passed": "#15803D",
        "failed": "#B91C1C",
        "broken": "#B45309",
    }
    DEFAULT_COLOR = "#6B7280"

    for idx, scenario in enumerate(scenarios, 1):
        raw_status = status_map.get(scenario["name"], "not recorded")
        sc = STATUS_COLOR.get(raw_status, DEFAULT_COLOR)
        display_status = raw_status.upper()

        header_row = [[
            Paragraph(
                f"<b>{idx}. {scenario['name']}</b>",
                ParagraphStyle("h", parent=styles["Normal"], fontSize=9, leading=13),
            ),
            Paragraph(
                f'<b><font color="{sc}">{display_status}</font></b>',
                ParagraphStyle("s", parent=styles["Normal"], fontSize=9, leading=13, alignment=2),
            ),
        ]]
        ht = Table(header_row, colWidths=[340, 88])
        ht.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        elements.append(ht)

        for step in scenario["steps"]:
            elements.append(Paragraph(f"  \u2192 {step}", step_style))
        elements.append(Spacer(1, 4 * mm))

    doc.build(elements)
    print(f"PDF generated: {out_pdf}")


if __name__ == "__main__":
    generate(
        feature_path="features/Student_All.feature",
        results_dir="reports/allure-results-student",
        out_pdf="reports/allure-report-student/allure-report-student-full.pdf",
    )
