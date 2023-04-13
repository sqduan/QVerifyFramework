import os
import datetime

from robot import run_cli

if __name__ == '__main__':

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

    log_dir = os.path.join(os.getcwd(), 'results/USB', timestamp)
    os.makedirs(log_dir)

    args = ['-d', log_dir, '-P', 'libraries', 'tests/USB']
    run_cli(args)