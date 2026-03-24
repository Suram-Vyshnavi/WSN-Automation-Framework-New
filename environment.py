from playwright.sync_api import sync_playwright
import os
import sys
from pathlib import Path

# Add project root to path to import conftest
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from conftest import report_generator
except ImportError:
    report_generator = None


def _is_enabled(name, default="false"):
    return os.getenv(name, default).lower() in ("1", "true", "yes")


def before_all(context):
    """Initialize report generation environment."""
    if report_generator:
        report_generator.setup_directories()
        print("🔧 Test environment initialized")


def before_scenario(context, scenario):
    """Set up Playwright browser before each scenario."""
    headless = _is_enabled("HEADLESS")
    slow_mo_ms = int(os.getenv("SLOW_MO_MS", "0" if headless else "1500"))

    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(
        headless=headless,
        slow_mo=slow_mo_ms
    )
    context.context = context.browser.new_context()
    
    # Start tracing if TRACE_ON env var is set
    try:
        trace_on = _is_enabled("TRACE_ON")
        if trace_on:
            context.context.tracing.start(screenshots=True, snapshots=True, sources=True)
            context._trace_enabled = True
        else:
            context._trace_enabled = False
    except Exception:
        context._trace_enabled = False
    
    context.page = context.context.new_page()


def after_scenario(context, scenario):
    """Clean up Playwright browser after each scenario."""
    # Stop tracing and save trace file per scenario
    try:
        if getattr(context, "_trace_enabled", False):
            traces_dir = os.path.join(os.getcwd(), "reports", "traces")
            os.makedirs(traces_dir, exist_ok=True)
            # Sanitize scenario name for filename
            name = "".join(c if c.isalnum() or c in (" ", "-", "_") else "_" for c in scenario.name).strip().replace(" ", "_")
            trace_file = os.path.join(traces_dir, f"{name}.zip")
            context.context.tracing.stop(path=trace_file)
    except Exception:
        pass
    
    # Close browser resources
    context.context.close()
    context.browser.close()
    context.playwright.stop()


def after_all(context):
    """Generate consolidated reports after all tests complete."""
    if report_generator:
        report_generator.generate_report()
