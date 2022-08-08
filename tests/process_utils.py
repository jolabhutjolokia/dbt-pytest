import logging
import subprocess
from typing import Dict


def execute_command(command: str, env_vars: Dict[str, str]):
    completed_process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, check=True, env=env_vars)
    if completed_process.returncode != 0:
        logging.error(completed_process.stdout)
        logging.error(completed_process.stderr)
        raise RuntimeError('Exit code was non zero')
