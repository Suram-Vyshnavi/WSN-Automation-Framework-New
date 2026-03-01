import subprocess
import sys
import os
from pathlib import Path
import shutil
import pdfkit
import json
import matplotlib.pyplot as plt
import webbrowser

def find_allure_executable():
    possible_paths = [
        Path.home() / "scoop" / "shims" / "allure.bat",
        Path.home() / "scoop" / "shims" / "allure.cmd",
        Path.home() / "allure-2.36.0" / "bin" / "allure.bat",
    ]
    for path in possible_paths:
        if path.exists():
            return str(path)
    return "allure"

def parse_results(results_dir):
    passed = failed = broken = 0
    for file in Path(results_dir).glob("*.json"):
        try:
            with open(file) as f:
                data = json.load(f)
                status = data.get("status")
                if status == "passed":
                    passed += 1
                elif status == "failed":
                    failed += 1
                elif status == "broken":
                    broken += 1
        except Exception:
            continue
    total = passed + failed + broken
    return total, passed, failed, broken

def create_chart(passed, failed, broken):
    labels = ['Passed', 'Failed', 'Broken']
    values = [passed, failed, broken]
    colors = ['green', 'red', 'orange']
    plt.figure(figsize=(5,5))
    plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%')
    plt.title("Test Results Distribution")
    chart_path = "reports/results_chart.png"
    plt.savefig(chart_path)
    plt.close()
    return chart_path

def build_summary_html(total, passed, failed, broken, chart_path):
    chart_abs = Path(chart_path).resolve().as_uri()
    html = f"""
    <h1>Automation Test Summary</h1>
    <p><b>Total Tests:</b> {total}</p>
    <p><b>Passed:</b> {passed}</p>
    <p><b>Failed:</b> {failed}</p>
    <p><b>Broken:</b> {broken}</p>
    <img src="{chart_abs}" alt="Results Chart">
    """
    return html

def generate_summary_pdf(html_content):
    output_pdf = "reports/summary-report.pdf"
    try:
        pdfkit.from_string(html_content, output_pdf)
        print(f"✅ Management summary PDF generated at {output_pdf}")
        webbrowser.open(output_pdf)
    except Exception as e:
        print(f"❌ Failed to generate summary PDF: {e}")

def run_tests(feature_path=None, tags=None, trace_on=False, headless=False):
    if trace_on:
        os.environ["TRACE_ON"] = "true"
    if headless:
        os.environ["HEADLESS"] = "true"

    project_root = Path(__file__).resolve().parent
    python_exe = sys.executable
    results_dir = project_root / "reports" / "allure-results"
    report_dir = project_root / "reports" / "allure-report"

    if results_dir.exists():
        shutil.rmtree(results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)

    cmd = [python_exe, "-m", "behave"]
    cmd.append(feature_path if feature_path else "features/")
    if tags:
        cmd.extend(["--tags", tags])
    cmd.extend([
        "-f", "allure_behave.formatter:AllureFormatter",
        "-o", str(results_dir),
        "-f", "pretty"
    ])

    result = subprocess.run(cmd)
    print("✅ Behave test run complete")

    allure_exe = find_allure_executable()
    try:
        subprocess.run([
            allure_exe, "generate",
            str(results_dir),
            "-o", str(report_dir),
            "--clean",
            "--single-file"
        ], check=True, shell=True)
        print(f"✅ Allure report generated at {report_dir}/index.html")

        input_html = str(report_dir / "index.html")
        output_pdf = str(report_dir / "allure-report.pdf")
        try:
            pdfkit.from_file(input_html, output_pdf)
            print(f"✅ Detailed Allure PDF generated at {output_pdf}")
        except Exception as e:
            print(f"❌ Failed to generate Allure PDF: {e}")

        total, passed, failed, broken = parse_results(results_dir)
        chart_path = create_chart(passed, failed, broken)
        summary_html = build_summary_html(total, passed, failed, broken, chart_path)
        generate_summary_pdf(summary_html)

    except FileNotFoundError:
        print("❌ Allure CLI not found. Please install Allure Commandline and add it to PATH.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to generate Allure report: {e}")

    return result.returncode

def main():
    exit_code = run_tests()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
