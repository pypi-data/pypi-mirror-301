import win32gui
import win32con
from .window_utils import MAKELPARAM
from .dpi_utils import XYMapper
from typing import Optional, Tuple

# Instantiate the XYMapper for DPI adjustments
trans_coord = XYMapper()

def click(hwnd: int, msg_down: int, msg_up: int, wparam: int, xy: Optional[Tuple[int, int]] = None) -> None:
    """Simulate a mouse click at a specific window handle.

    Args:
        hwnd (int): Handle to the window where the click occurs.
        msg_down (int): Message code for mouse button down.
        msg_up (int): Message code for mouse button up.
        wparam (int): Indicates which mouse button was pressed.
        xy (Optional[Tuple[int, int]], optional): Coordinates for the click. If None, uses the center of the window.
    """
    # Transform coordinates if provided, otherwise use window center
    if xy:
        xy = trans_coord(xy)
    else:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        xy = ((right - left) // 2, (bottom - top) // 2)

    lparam = MAKELPARAM(*xy)
    # Send the mouse down and up messages to the window
    win32gui.SendMessage(hwnd, msg_down, wparam, lparam)
    win32gui.SendMessage(hwnd, msg_up, wparam, lparam)

def lclick(hwnd: int, xy: Optional[Tuple[int, int]] = None) -> None:
    """Simulate a left mouse click at a specific window handle.

    Args:
        hwnd (int): Handle to the window where the click occurs.
        xy (Optional[Tuple[int, int]], optional): Coordinates for the click. If None, uses the center of the window.
    """
    click(
        hwnd,
        win32con.WM_LBUTTONDOWN,
        win32con.WM_LBUTTONUP,
        win32con.MK_LBUTTON,
        xy,
    )

if __name__ == '__main__':
    import time
    import win32api
    import threading

    title = "Message Box Title"
    message = "This message box will close automatically after 3 seconds!"
    
    def show_msg():
        # Show the message box
        win32api.MessageBox(0, message, title, win32con.MB_OK | win32con.MB_ICONINFORMATION)

    # Message box is modal so we run other thread
    thread = threading.Thread(target=show_msg)
    thread.start()

    # Wait for a moment to ensure the message box is shown
    time.sleep(3)

    # Find the message box window by title
    message_box_hwnd = win32gui.FindWindow(None, title)

    if message_box_hwnd:
        # Find OK button hwnd
        ok = win32gui.FindWindowEx(message_box_hwnd, None, 'Button', None)
        # Simulate the left click on the OK button
        lclick(ok)

    thread.join()
