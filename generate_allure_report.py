"""
Generate Allure HTML Report
"""
import subprocess
import sys
from pathlib import Path
import shutil


def find_allure_executable():
    """Find the Allure executable in common installation locations"""
    # First, try to find in PATH using where.exe
    try:
        result = subprocess.run(
            ["where.exe", "allure"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            # Prefer .bat or .cmd files for Windows
            paths = result.stdout.strip().split('\n')
            for path in paths:
                path = path.strip()
                if path.endswith('.bat') or path.endswith('.cmd'):
                    return path
            # If no .bat/.cmd found, return the first one
            return paths[0]
    except:
        pass
    
    # Common Allure installation paths
    possible_paths = [
        Path.home() / "scoop" / "shims" / "allure.bat",
        Path.home() / "scoop" / "shims" / "allure.cmd",
        Path.home() / "allure-2.36.0" / "bin" / "allure.bat",
        Path("C:/ProgramData/chocolatey/bin/allure.bat"),
        Path("C:/ProgramData/chocolatey/bin/allure.cmd"),
    ]
    
    # Check common installation paths
    for path in possible_paths:
        if path.exists():
            return str(path)
    
    return None


def generate_allure_html():
    """Generate Allure HTML report from existing results"""
    project_root = Path(__file__).resolve().parent
    
    allure_results = project_root / "reports" / "allure-results"
    allure_report = project_root / "reports" / "allure-report"
    
    if not allure_results.exists() or not any(allure_results.iterdir()):
        print("⚠ No test results found!")
        print(f"Please run tests first to generate results in: {allure_results}")
        print("\nExample: python -m behave features/login.feature -f allure_behave.formatter:AllureFormatter -o reports/allure-results")
        return 1
    
    print("="*70)
    print("Generating Allure HTML Report...")
    print("="*70)
    
    # Find Allure executable
    allure_exe = find_allure_executable()
    
    if not allure_exe:
        print("\n⚠ Allure command not found!")
        print("Please install Allure CLI:")
        print("  • scoop install allure")
        print("  • choco install allure")
        print("  • Download from: https://github.com/allure-framework/allure2/releases")
        return 1
    
    try:
        # Generate HTML report
        cmd = [
            allure_exe, "generate",
            str(allure_results),
            "-o", str(allure_report),
            "--clean",
            "--single-file"
        ]
        
        subprocess.run(cmd, check=True, shell=True)
        
        print("\n" + "="*70)
        print("✓ Allure HTML Report Generated Successfully!")
        print("="*70)
        print(f"\nReport Location: {allure_report}")
        print(f"Index File: {allure_report / 'index.html'}")
        print("\nTo view the report, open index.html in your browser")
        print(f"Or run: allure open {allure_report}")
        print("="*70)
        
        return 0
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error generating report: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(generate_allure_html())
