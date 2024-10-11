import win32gui
import win32con
import win32ui
from typing import Optional

def RGB(r: int, g: int, b: int) -> int:
    """Convert RGB values to a DWORD value."""
    return (b << 16) | (g << 8) | r

def draw_point_on_window(hwnd: int, x: int, y: int, radius: Optional[int] = 4, color: Optional[int] = RGB(255, 0, 0)) -> None:
    """Draw a point on the specified window at (x, y) with the given radius and color.

    Args:
        hwnd (int): Handle to the window where the point will be drawn.
        x (int): The x-coordinate of the point.
        y (int): The y-coordinate of the point.
        radius (Optional[int]): The radius of the point. Defaults to 4.
        color (Optional[int]): The color of the point in RGB format. Defaults to red.
    """
    # Get the device context of the window
    hdc = win32gui.GetDC(hwnd)
    if not hdc:
        print("Failed to get device context")
        return
    
    # Create a brush for the specified color
    brush = win32ui.CreateBrush(win32con.BS_SOLID, color, 0)
    
    # Select the brush into the device context
    old_brush = win32gui.SelectObject(hdc, brush.GetSafeHandle())

    # Draw a circle centered at (x, y) with the given radius
    win32gui.Ellipse(hdc, x - radius, y - radius, x + radius, y + radius)

    # Cleanup
    win32gui.SelectObject(hdc, old_brush)
    win32gui.DeleteObject(brush.GetSafeHandle())
    win32gui.ReleaseDC(hwnd, hdc)

if __name__ == '__main__':
    import time
    from .process import execute, kill
    app = 'notepad.exe'
    execute(app)
    time.sleep(1)

    hwnd = win32gui.FindWindow(None, "Untitled - Notepad")
    if hwnd:
        draw_point_on_window(hwnd, 100, 100, 4, RGB(255, 0, 0))
    time.sleep(5)
    kill(app)


