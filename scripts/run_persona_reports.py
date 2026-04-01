"""
Run persona-specific Behave scenarios, generate Allure HTML, and generate a
comprehensive PDF report for that persona.
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


FEATURE_BY_PERSONA = {
    "student": "features/Student_All.feature",
    "faculty": "features/Faculty_All.feature",
    "rm": "features/Faculty_All.feature",
}

EXCLUDE_TAGS_BY_PERSONA = {
    "rm": ["faculty_only"],
}


def find_allure_executable():
    possible_paths = [
        Path.home() / "scoop" / "shims" / "allure.bat",
        Path.home() / "scoop" / "shims" / "allure.cmd",
        Path.home() / "allure-2.36.0" / "bin" / "allure.bat",
        Path("C:/ProgramData/chocolatey/bin/allure.bat"),
        Path("C:/ProgramData/chocolatey/bin/allure.cmd"),
    ]
    for path in possible_paths:
        if path.exists():
            return str(path)
    return "allure"


def run_persona(persona, extra_exclude_tags=None):
    project_root = Path(__file__).resolve().parent.parent
    feature_path = FEATURE_BY_PERSONA[persona]
    results_dir = project_root / "reports" / f"allure-results-{persona}"
    report_dir = project_root / "reports" / f"allure-report-{persona}"
    output_pdf = report_dir / f"allure-report-{persona}-full.pdf"

    if results_dir.exists():
        shutil.rmtree(results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env["PERSONA"] = persona

    behave_cmd = [
        sys.executable,
        "-m",
        "behave",
        feature_path,
        "-f",
        "pretty",
        "-o",
        "-",
        "-f",
        "allure_behave.formatter:AllureFormatter",
        "-o",
        str(results_dir),
    ]

    excluded_tags = list(EXCLUDE_TAGS_BY_PERSONA.get(persona, []))
    if extra_exclude_tags:
        excluded_tags.extend(t for t in extra_exclude_tags if t not in excluded_tags)
    for tag in excluded_tags:
        behave_cmd.extend(["--tags", f"~@{tag}"])

    print(f"Running {persona} scenarios from {feature_path}")
    behave_result = subprocess.run(behave_cmd, env=env)
    print(f"Behave exit code: {behave_result.returncode}")

    allure_exe = find_allure_executable()
    allure_cmd = [
        allure_exe,
        "generate",
        str(results_dir),
        "-o",
        str(report_dir),
        "--clean",
        "--single-file",
    ]

    subprocess.run(allure_cmd, check=True, shell=True, env=env)

    pdf_cmd = [
        sys.executable,
        str(project_root / "scripts" / "generate_persona_pdf.py"),
        "--persona",
        persona,
        "--feature",
        feature_path,
        "--results",
        str(results_dir),
        "--output",
        str(output_pdf),
    ]
    if excluded_tags:
        pdf_cmd.extend(["--exclude-tags", ",".join(excluded_tags)])
    subprocess.run(pdf_cmd, check=True, env=env)

    print(f"HTML report: {report_dir / 'index.html'}")
    print(f"PDF report: {output_pdf}")

    return behave_result.returncode


def main():
    parser = argparse.ArgumentParser(description="Run persona-wise tests and generate reports")
    parser.add_argument("--persona", required=True, choices=["student", "faculty", "rm"])
    parser.add_argument(
        "--exclude-tags",
        nargs="+",
        default=[],
        metavar="TAG",
        help="Additional Behave tags to exclude (e.g. --exclude-tags faculty_only)",
    )
    args = parser.parse_args()

    exit_code = run_persona(args.persona, extra_exclude_tags=args.exclude_tags)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
