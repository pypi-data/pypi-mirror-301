import win32gui
import win32api
import win32process
import win32con
from typing import Callable, List, Optional

def MAKELPARAM(l, h):
    # Ensure x and y are within the 16-bit range
    l &= 0xFFFF
    h &= 0xFFFF
    # Combine x and y into a single 32-bit integer
    lparam = (h << 16) | l
    return lparam

def minimize(hwnd: int):
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

def get_executable_path(pid: int) -> Optional[str]:
    """Get the executable path of a process by its PID.

    Args:
        pid (int): Process ID.

    Returns:
        Optional[str]: Path to the executable or None if an error occurred.
    """
    hproc = 0
    try:
        hproc = win32api.OpenProcess(
            win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ,
            False,
            pid
        )
        return win32process.GetModuleFileNameEx(hproc, 0)
    except Exception as e:
        #print(f'Error retrieving executable path: {e}')
        return None
    finally:
        if hproc:
            win32api.CloseHandle(hproc)

def find_windows(match: Callable[[int, Optional[str]], bool]) -> List[int]:
    """Find window handles based on a matching condition.

    Args:
        match (Callable): A function that takes a window handle and executable name and returns a boolean.

    Returns:
        List[int]: A list of matching window handles.
    """
    def callback(hwnd, hwnds):
        hwnds.append(hwnd)

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    matching_windows = []

    for hwnd in hwnds:
        tid, pid = win32process.GetWindowThreadProcessId(hwnd)
        exe_name = get_executable_path(pid)
        if match(hwnd, exe_name):
            matching_windows.append(hwnd)

    return matching_windows

if __name__ == '__main__':
    import time
    from .process import execute, kill
    app = 'notepad.exe'
    execute(app)
    time.sleep(1)
    def match(hwnd, exe_path):
        return exe_path and exe_path.lower().endswith(app)
    hwnds = find_windows(match)
    print(hwnds)
    kill(app)
