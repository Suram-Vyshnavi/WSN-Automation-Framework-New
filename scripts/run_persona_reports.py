"""
Run persona-specific Behave scenarios, generate Allure HTML, and generate a
comprehensive PDF report for that persona.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    from dotenv import load_dotenv
    _dotenv_path = Path(__file__).resolve().parent.parent / ".env"
    if _dotenv_path.exists():
        load_dotenv(dotenv_path=_dotenv_path, override=False)
except ImportError:
    pass


FEATURE_BY_PERSONA = {
    "student": "features/Student_All.feature",
    "faculty": "features/Faculty_All.feature",
    "rm": "features/RM_All.feature",
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


def sanitize_version(version):
    cleaned = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in version)
    return cleaned.strip("_") or "unknown"


def write_allure_environment_file(results_dir, persona, env_name, product_version):
    env_file = Path(results_dir) / "environment.properties"
    lines = [
        f"Persona={persona}",
        f"Environment={env_name}",
        f"ProductVersion={product_version}",
        f"GeneratedAt={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    ]
    env_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def push_to_reports_repo(persona, env_name, product_version, report_dir, output_pdf):
    """
    Clone (or pull) a dedicated reports repo, copy the generated PDF + HTML into a
    dated folder, then commit and push.  Skips silently if REPORTS_REPO_URL is not set.

    Folder layout inside the reports repo:
        <persona>/<env>/<YYYY-MM-DD>_v<version>/
            index.html
            allure-report-<persona>-full.pdf
            metadata.json
    """
    reports_repo_url = os.getenv("REPORTS_REPO_URL", "").strip()
    if not reports_repo_url:
        print("INFO: REPORTS_REPO_URL not set — skipping push to reports repo.")
        return None

    project_root = Path(__file__).resolve().parent.parent
    local_repo_str = os.getenv("REPORTS_REPO_LOCAL_PATH", "").strip()
    local_repo = Path(local_repo_str) if local_repo_str else project_root.parent / "WSN-Test-Reports"

    if not (local_repo / ".git").exists():
        print(f"Cloning reports repo to {local_repo} ...")
        subprocess.run(["git", "clone", reports_repo_url, str(local_repo)], check=True)
    else:
        print(f"Pulling latest from reports repo at {local_repo} ...")
        subprocess.run(["git", "-C", str(local_repo), "pull", "--rebase"], check=True)

    date_stamp = datetime.now().strftime("%Y-%m-%d")
    dest_dir = local_repo / persona / env_name / f"{date_stamp}_v{sanitize_version(product_version)}"
    dest_dir.mkdir(parents=True, exist_ok=True)

    report_index = Path(report_dir) / "index.html"
    if report_index.exists():
        shutil.copy2(report_index, dest_dir / "index.html")

    output_pdf_path = Path(output_pdf)
    if output_pdf_path.exists():
        shutil.copy2(output_pdf_path, dest_dir / output_pdf_path.name)

    metadata = {
        "persona": persona,
        "environment": env_name,
        "product_version": product_version,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }
    (dest_dir / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    subprocess.run(["git", "-C", str(local_repo), "add", "."], check=True)
    commit_msg = f"report({persona}): {date_stamp} v{product_version} [{env_name}]"
    commit_result = subprocess.run(
        ["git", "-C", str(local_repo), "commit", "-m", commit_msg],
        capture_output=True,
        text=True,
    )
    if commit_result.returncode == 0:
        subprocess.run(["git", "-C", str(local_repo), "push"], check=True)
        print(f"Reports pushed → {reports_repo_url}  folder: {dest_dir.relative_to(local_repo)}")
    else:
        print("INFO: Nothing new to commit to reports repo.")

    return dest_dir


def run_persona(persona, extra_exclude_tags=None, product_version="unknown"):
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
    env_name = env.get("ENV", "qa")
    resolved_product_version = product_version or env.get("PRODUCT_VERSION") or "unknown"
    env["PRODUCT_VERSION"] = resolved_product_version

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

    write_allure_environment_file(results_dir, persona, env_name, resolved_product_version)

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
        "--product-version",
        resolved_product_version,
    ]
    if excluded_tags:
        pdf_cmd.extend(["--exclude-tags", ",".join(excluded_tags)])
    subprocess.run(pdf_cmd, check=True, env=env)

    dest = push_to_reports_repo(
        persona=persona,
        env_name=env_name,
        product_version=resolved_product_version,
        report_dir=report_dir,
        output_pdf=output_pdf,
    )

    print(f"HTML report: {report_dir / 'index.html'}")
    print(f"PDF report:  {output_pdf}")
    if dest:
        print(f"Reports repo folder: {dest}")

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
    parser.add_argument(
        "--product-version",
        default=os.getenv("PRODUCT_VERSION", "unknown"),
        help="Product version for metadata and archive folder naming",
    )
    args = parser.parse_args()

    exit_code = run_persona(
        args.persona,
        extra_exclude_tags=args.exclude_tags,
        product_version=args.product_version,
    )
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
