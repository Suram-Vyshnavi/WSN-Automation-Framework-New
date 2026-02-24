"""
Behave test runner with automatic report generation.
Run all tests and generate consolidated HTML report at the end.
"""

import subprocess
import sys
import os
import argparse
from pathlib import Path


def setup_environment():
    """Set up environment variables for test execution."""
    # Set default environment variables if not already set
    if "HEADLESS" not in os.environ:
        os.environ["HEADLESS"] = "false"


def run_tests(feature_path=None, tags=None, trace_on=False, headless=False, generate_report=False):
    """
    Run Behave tests with specified options.
    
    Args:
        feature_path: Path to specific feature file or directory (default: features/)
        tags: Behave tags to filter tests (e.g., '@smoke', '@regression')
        trace_on: Enable Playwright tracing
        headless: Run browser in headless mode
        generate_report: Generate Allure HTML report after tests
    """
    setup_environment()
    
    # Set environment variables
    if trace_on:
        os.environ["TRACE_ON"] = "true"
    if headless:
        os.environ["HEADLESS"] = "true"
    
    # Find Python executable (prefer virtual environment)
    project_root = Path(__file__).resolve().parent
    venv_python = project_root / ".venv" / "Scripts" / "python.exe"
    if not venv_python.exists():
        venv_python = project_root / "env" / "Scripts" / "python.exe"
    python_exe = str(venv_python) if venv_python.exists() else sys.executable
    
    # Clean old allure results before running tests
    if generate_report:
        import shutil
        allure_results_path = project_root / "reports" / "allure-results"
        if allure_results_path.exists():
            shutil.rmtree(allure_results_path)
            print(f"🗑️  Cleaned old test results from {allure_results_path}")
        allure_results_path.mkdir(parents=True, exist_ok=True)
    
    # Build behave command
    cmd = [python_exe, "-m", "behave"]
    
    # Add feature path
    if feature_path:
        cmd.append(feature_path)
    else:
        cmd.append("features/")
    
    # Add tags if specified
    if tags:
        cmd.extend(["--tags", tags])
    
    # Add Allure formatter first (with output directory)
    cmd.extend([
        "-f", "allure_behave.formatter:AllureFormatter",
        "-o", "reports/allure-results",
        "-f", "pretty"
    ])
    
    try:
        print("=" * 60)
        print("🚀 Starting Test Execution")
        print("=" * 60)
        print(f"Command: {' '.join(cmd)}")
        print(f"Trace: {'Enabled' if trace_on else 'Disabled'}")
        print(f"Headless: {'Enabled' if headless else 'Disabled'}")
        print("=" * 60 + "\n")
        
        # Run behave tests
        result = subprocess.run(cmd, capture_output=False, text=True)
        
        print("\n" + "=" * 60)
        if result.returncode == 0:
            print("✅ All tests completed successfully")
        else:
            print("❌ Some tests failed")
        print("=" * 60)
        
        # Generate Allure HTML report if requested
        if generate_report:
            print("\n" + "=" * 60)
            print("📊 Generating Allure HTML Report...")
            print("=" * 60)
            
            try:
                # Find allure executable
                allure_paths = [
                    Path.home() / "scoop" / "shims" / "allure.bat",
                    Path.home() / "scoop" / "shims" / "allure.cmd",
                    Path.home() / "allure-2.36.0" / "bin" / "allure.bat",
                ]
                
                allure_exe = "allure"  # Default to PATH
                for path in allure_paths:
                    if path.exists():
                        allure_exe = str(path)
                        break
                
                allure_cmd = [
                    allure_exe, "generate",
                    "reports/allure-results",
                    "-o", "reports/allure-report",
                    "--clean",
                    "--single-file"
                ]
                subprocess.run(allure_cmd, check=True, shell=True)
                
                print("✅ Allure single-file HTML report generated successfully!")
                print(f"📁 Report location: reports/allure-report/index.html")
                print(f"💡 You can open this file directly in your browser!")
                print("=" * 60)
            except FileNotFoundError:
                print("⚠ Allure CLI not found. Install with: scoop install allure")
            except subprocess.CalledProcessError as e:
                print(f"⚠ Failed to generate Allure report: {e}")
        
        return result.returncode
        
    except Exception as e:
        print(f"❌ Error running behave: {e}")
        return 1


def main():
    """Main entry point for test execution."""
    parser = argparse.ArgumentParser(
        description="Run Behave + Playwright tests with report generation"
    )
    
    parser.add_argument(
        "feature",
        nargs="?",
        default=None,
        help="Path to feature file or directory (default: features/)"
    )
    
    parser.add_argument(
        "--tags",
        "-t",
        help="Behave tags to filter tests (e.g., '@smoke', '@regression')"
    )
    
    parser.add_argument(
        "--trace",
        action="store_true",
        help="Enable Playwright tracing"
    )
    
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode"
    )
    
    parser.add_argument(
        "--show-report",
        action="store_true",
        help="Open report in browser after test execution"
    )
    
    parser.add_argument(
        "--allure",
        action="store_true",
        help="Generate Allure HTML report after test execution"
    )
    
    args = parser.parse_args()
    
    # Run tests
    exit_code = run_tests(
        feature_path=args.feature,
        tags=args.tags,
        trace_on=args.trace,
        headless=args.headless,
        generate_report=args.allure
    )
    
    # Open report if requested
    if args.show_report and exit_code == 0:
        report_path = Path("reports/test-report.html")
        if report_path.exists():
            import webbrowser
            webbrowser.open(f"file://{report_path.absolute()}")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
