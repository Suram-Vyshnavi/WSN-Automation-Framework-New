"""
Generate a comprehensive persona PDF report by reading the feature file directly,
and enrich statuses using available Allure result JSON files.
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def parse_feature(feature_path, exclude_tags=None):
    scenarios = []
    current = None
    pending_tags = []
    excluded = set(exclude_tags or [])

    for line in Path(feature_path).read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("@"):
            pending_tags.extend([tag.lstrip("@").strip() for tag in stripped.split() if tag.startswith("@")])
            continue
        if stripped.startswith("Scenario:"):
            if current:
                scenarios.append(current)
            scenario_tags = set(pending_tags)
            pending_tags = []
            if excluded.intersection(scenario_tags):
                current = None
                continue
            current = {
                "name": stripped[len("Scenario:"):].strip(),
                "steps": [],
                "tags": sorted(scenario_tags),
            }
        elif current and any(stripped.startswith(k) for k in ("Given ", "When ", "Then ", "And ", "But ")):
            current["steps"].append(stripped)

    if current:
        scenarios.append(current)

    return scenarios


def load_statuses(results_dir):
    status_map = {}
    for result_file in Path(results_dir).glob("*-result.json"):
        try:
            data = json.loads(result_file.read_text(encoding="utf-8"))
            scenario_name = data.get("name", "").strip()
            status = data.get("status", "unknown").strip().lower()
            if not scenario_name:
                continue

            current = status_map.get(scenario_name)
            if current != "passed":
                status_map[scenario_name] = status
        except Exception:
            continue

    return status_map


def generate_pdf(persona, feature_path, results_dir, output_pdf, exclude_tags=None, product_version="unknown"):
    scenarios = parse_feature(feature_path, exclude_tags=exclude_tags)
    status_map = load_statuses(results_dir)

    total = len(scenarios)
    passed = sum(1 for s in scenarios if status_map.get(s["name"]) == "passed")
    failed = sum(1 for s in scenarios if status_map.get(s["name"]) == "failed")
    broken = sum(1 for s in scenarios if status_map.get(s["name"]) == "broken")
    not_recorded = total - passed - failed - broken

    doc = SimpleDocTemplate(
        str(output_pdf),
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )

    styles = getSampleStyleSheet()
    small = ParagraphStyle("small", parent=styles["Normal"], fontSize=8, leading=11)
    step_style = ParagraphStyle(
        "step",
        parent=styles["Normal"],
        fontSize=8,
        leading=11,
        leftIndent=10,
        textColor=colors.HexColor("#374151"),
    )

    elements = []
    elements.append(Paragraph(f"{persona.title()} Persona - Test Execution Report", styles["Title"]))
    elements.append(
        Paragraph(
            (
                f"Feature: {Path(feature_path).name} | "
                f"Product Version: {product_version} | "
                f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            ),
            small,
        )
    )
    elements.append(Spacer(1, 8 * mm))

    summary = [
        ["Total", "Passed", "Failed", "Broken", "Not Recorded"],
        [str(total), str(passed), str(failed), str(broken), str(not_recorded)],
    ]
    summary_table = Table(summary, colWidths=[72, 72, 72, 72, 90])
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F3A5F")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#EFF6FF")),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
            ]
        )
    )
    elements.append(summary_table)
    elements.append(Spacer(1, 8 * mm))
    elements.append(Paragraph("Scenario Details", styles["Heading2"]))
    elements.append(Spacer(1, 3 * mm))

    status_color = {
        "passed": "#15803D",
        "failed": "#B91C1C",
        "broken": "#B45309",
    }

    for idx, scenario in enumerate(scenarios, start=1):
        raw_status = status_map.get(scenario["name"], "not recorded")
        color_code = status_color.get(raw_status, "#6B7280")

        header_row = [
            [
                Paragraph(
                    f"<b>{idx}. {scenario['name']}</b>",
                    ParagraphStyle("header", parent=styles["Normal"], fontSize=9, leading=13),
                ),
                Paragraph(
                    f'<b><font color="{color_code}">{raw_status.upper()}</font></b>',
                    ParagraphStyle("status", parent=styles["Normal"], fontSize=9, leading=13, alignment=2),
                ),
            ]
        ]

        scenario_header = Table(header_row, colWidths=[340, 88])
        scenario_header.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )
        elements.append(scenario_header)

        for step in scenario["steps"]:
            elements.append(Paragraph(f"  -> {step}", step_style))
        elements.append(Spacer(1, 4 * mm))

    doc.build(elements)


def main():
    parser = argparse.ArgumentParser(description="Generate persona-wise comprehensive PDF report")
    parser.add_argument("--persona", required=True, choices=["student", "faculty", "rm"])
    parser.add_argument("--feature", required=True, help="Feature file path")
    parser.add_argument("--results", required=True, help="Allure results directory")
    parser.add_argument("--output", required=True, help="Output PDF path")
    parser.add_argument("--exclude-tags", default="", help="Comma-separated tags to exclude from feature parsing")
    parser.add_argument("--product-version", default="unknown", help="Product version to print in report")
    args = parser.parse_args()

    exclude_tags = [tag.strip().lstrip("@") for tag in args.exclude_tags.split(",") if tag.strip()]
    generate_pdf(
        args.persona,
        args.feature,
        args.results,
        args.output,
        exclude_tags=exclude_tags,
        product_version=args.product_version,
    )
    print(f"PDF generated: {args.output}")


if __name__ == "__main__":
    main()
