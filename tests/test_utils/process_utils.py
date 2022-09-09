import logging
from subprocess import run, CalledProcessError, STDOUT, PIPE
from typing import Dict


def execute_command(command: str, env_vars: Dict[str, str], cwd: str = None):
    try:
        completed_process = run(command, stdout=PIPE, stderr=STDOUT, cwd=cwd, shell=True, check=True, text=True, env=env_vars)
        if completed_process.returncode != 0:
            logging.error(completed_process.stdout)
            logging.error(completed_process.stderr)
            raise RuntimeError('Exit code was non zero')
    except CalledProcessError as error:
        print(error.stderr)
        print(error.stdout)
        print(error.output)
        raise error
