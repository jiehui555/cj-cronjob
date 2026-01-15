from src.cron.screenshot_job import run_screenshot_job


def run() -> int:
    """Run the screenshot job (legacy entry point for main.py)"""
    return run_screenshot_job()