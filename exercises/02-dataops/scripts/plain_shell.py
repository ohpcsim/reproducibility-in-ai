"""Make ! commands in this notebook print plain text.

With a terminal, DVC draws progress bars, and those make a mess of a notebook's output.
"""
import os
import subprocess

from IPython import get_ipython

environment = {name: value for name, value in os.environ.items() if name != "FORCE_COLOR"}


def system(command):
    done = subprocess.run(["bash", "-c", command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=environment)
    get_ipython().user_ns["_exit_code"] = done.returncode
    print(done.stdout, end="")


get_ipython().system = system
