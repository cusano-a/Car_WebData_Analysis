import subprocess
import sys
import os
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


def get_scraper_path():
    return os.path.join(".", "autoscout_scraper.py")


def get_test_path():
    return os.path.join(".", "loadtest.py")


def get_python_command():
    return sys.executable


def run_scraper(python_command, scraper_path):
    print(f'Scraper running at {datetime.now()}')
    subprocess.run([python_command, scraper_path], check=True)


if __name__ == '__main__':

    python_command = get_python_command()  
    scraper_path = get_test_path()

    sched = BlockingScheduler()
    sched.add_job(run_scraper, 'interval', seconds=10, args=[python_command, scraper_path])

    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        sched.shutdown(wait=False)
