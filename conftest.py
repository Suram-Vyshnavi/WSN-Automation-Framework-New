
"""
Minimal Behave configuration for single HTML report generation.
"""

import subprocess
from pathlib import Path
import shutil


class BehaveReportGenerator:
    """Minimal report generator for single HTML output."""
    
    def __init__(self):
        self.reports_dir = Path("reports")
        self.allure_results_dir = self.reports_dir / "allure-results"
        self.allure_temp_dir = self.reports_dir / "allure-temp"
        self.complete_report = self.reports_dir / "complete-report.html"
        
    def setup_directories(self):
        """Create necessary directories."""
        self.reports_dir.mkdir(exist_ok=True)
        self.allure_results_dir.mkdir(exist_ok=True)
        
    def generate_report(self):
        """Generate single HTML report."""
        try:
            # Check if results exist
            if not list(self.allure_results_dir.glob("*.json")):
                print("⚠️  No test results found")
                return
                
            # Generate allure report
            subprocess.run([
                "allure", "generate",
                str(self.allure_results_dir),
                "-o", str(self.allure_temp_dir),
                "--clean"
            ], capture_output=True)
            
            # Combine into single HTML
            subprocess.run([
                "allure-combine",
                str(self.allure_temp_dir),
                "--auto-create-folders"
            ], capture_output=True)
            
            # Move to final location
            complete_html = self.allure_temp_dir / "complete.html"
            if complete_html.exists():
                shutil.move(str(complete_html), str(self.complete_report))
                shutil.rmtree(self.allure_temp_dir)
                print(f"✅ Report: {self.complete_report}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")


# Global instance
report_generator = BehaveReportGenerator()


def before_all(context):
    """Setup before tests."""
    report_generator.setup_directories()


def after_all(context):
    """Generate report after tests."""
    report_generator.generate_report()
