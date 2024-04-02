import os
import sys
import time
import subprocess
from subprocess import TimeoutExpired

def subprocess_start(command: str, timespan: int):
    """Create a subprocess

    Args:
        command  (_type_): Command needs to execute in subprocess
        timespan (_type_): Timespan for the subprocess

    Returns:
        _type_: _description_
    """
    outs = 0
    errs = 0
    process = None

    try:
        # Create subprocess non-blockingly
        process = subprocess.Popen(command, \
                           stdout=subprocess.PIPE,stderr=subprocess.PIPE, \
                           start_new_session = True)

    # There is a two exception that we may encounter, the trace32 has already
    # been occupied, currently don't know how to cover this
    except Exception as e:
        if not process is None:
            process.kill()
            outs, errs = process.communicate()
            process = None
            print("==============TimeoutExpired outs===============")
            print(outs.decode('utf-8','ignore'))
            print("==============TimeoutExpired errs===============")
            print(errs)

    return [process, outs, errs]