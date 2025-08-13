import subprocess

from langchain_core.tools import tool


@tool
def bash_shell(command: str) -> str:
    """Run a single bash shell command on a Linux system connected to the target network.

    bash_shell cannot be used to run interactive commands.

    bash_shell should only be used when no other tools available can perform the required task.
    """
    proc = subprocess.run(command, shell=True, capture_output=True, timeout=30)
    return proc.stdout
