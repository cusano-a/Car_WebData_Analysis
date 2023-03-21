import subprocess
import sys
import os
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


def get_scraper_path():
    return os.path.join(".", "usedcars_scraper.py")


def get_python_command():
    return sys.executable


def run_scraper(python_command, scraper_path):
    print(f"Scraper running at {datetime.now()}")
    subprocess.run([python_command, scraper_path], check=True)


if __name__ == "__main__":
    print("Scraper scheduler started")
    python_command = get_python_command()
    scraper_path = get_scraper_path()

    sched = BlockingScheduler()
    sched.add_job(
        run_scraper,
        "interval",
        hours=1,
        next_run_time=datetime.now(),
        args=[python_command, scraper_path],
    )

    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        sched.shutdown(wait=False)
