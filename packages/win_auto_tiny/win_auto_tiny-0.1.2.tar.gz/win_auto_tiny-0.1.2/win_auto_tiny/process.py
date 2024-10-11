import subprocess
import platform
import os
from typing import List, Optional

def execute(exe_path: str, *args: str) -> Optional[subprocess.Popen]:
    """Run an executable with given arguments.

    Args:
        exe_path (str): The path to the executable.
        *args (str): Additional arguments to pass to the executable.

    Returns:
        Optional[subprocess.Popen]: A Popen object representing the running process, or None if the process could not be started.
    """
    try:
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP if platform.system() == 'Windows' else 0
        return subprocess.Popen(
            [exe_path] + list(args),
            creationflags=creationflags|subprocess.CREATE_NO_WINDOW
        )
    except Exception as e:
        print(f"Error starting process: {e}")
        return None

def kill(exe_name: str):
    """Kill a process by its executable name in a platform-agnostic way.

    Args:
        exe_name (str): The name of the executable to kill.

    Returns:
        None
    """
    try:
        if platform.system() == 'Windows':
            command = ['taskkill', '/F', '/IM', exe_name, '/T']
        else:
            pids = subprocess.check_output(['pgrep', exe_name]).decode().splitlines()
            command = ['kill', '-9']  # Use '-9' for SIGKILL
            command.extend(pids)

        null_device = os.devnull

        if platform.system() == 'Windows':   
            null_device = 'NUL'
        else:
            null_device = '/dev/null'

        with open(null_device, 'w') as devnull:
            process = subprocess.Popen(
                command,
                stdout=devnull,
                stderr=devnull,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            process.wait()
    except Exception as e:
        print(f"Error killing process: {e}")

if __name__ == '__main__':
    import time
    app = 'notepad.exe'
    execute(app)
    time.sleep(1)
    kill(app)
