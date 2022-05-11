import sys
import os
import shutil
import subprocess

def wsl_available() -> bool:
    """
    heuristic to detect if Windows Subsystem for Linux is available.

    Uses presence of /etc/os-release in the WSL image to say Linux is there.
    This is a de facto file standard across Linux distros.
    """
    if os.name == "nt":
        wsl = shutil.which("wsl")
        if not wsl:
            return False
        # can't read this file or test with
        # pathlib.Path('//wsl$/Ubuntu/etc/os-release').
        # A Python limitation?
        ret = subprocess.run(["wsl", "test", "-f", "/etc/os-release"])
        return ret.returncode == 0

    return False

wsl_available()