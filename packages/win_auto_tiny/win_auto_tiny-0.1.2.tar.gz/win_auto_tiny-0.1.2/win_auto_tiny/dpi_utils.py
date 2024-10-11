import win32api
import win32gui
import win32con
import win32print
from typing import Tuple

def get_dpi() -> Tuple[int, int]:
    """Get the current DPI settings for the primary display.

    Returns:
        Tuple[int, int]: The horizontal and vertical DPI values.
    """
    hdc = win32gui.GetDC(0)
    try:
        dpi_x = win32print.GetDeviceCaps(hdc, win32con.LOGPIXELSX)  # 88 = LOGPIXELSX
        dpi_y = win32print.GetDeviceCaps(hdc, win32con.LOGPIXELSY)  # 90 = LOGPIXELSY
        return dpi_x, dpi_y
    finally:
        win32gui.ReleaseDC(0, hdc)

#class XYMapper:
#    def __init__(self, input_dpi: Tuple[int, int] = (96, 96)):
#        """Initialize the XYMapper with input DPI settings.
#
#        Args:
#            input_dpi (Tuple[int, int]): The input DPI settings as a tuple.
#        """
#        sys_dpi = get_dpi()
#        self.ratio = (sys_dpi[0] / input_dpi[0], sys_dpi[1] / input_dpi[1])
#
#    def map_x(self, x: int) -> int:
#        """Map the x-coordinate according to the DPI ratio.
#
#        Args:
#            x (int): The original x-coordinate.
#
#        Returns:
#            int: The mapped x-coordinate.
#        """
#        return round(x * self.ratio[0])
#
#    def map_y(self, y: int) -> int:
#        """Map the y-coordinate according to the DPI ratio.
#
#        Args:
#            y (int): The original y-coordinate.
#
#        Returns:
#            int: The mapped y-coordinate.
#        """
#        return round(y * self.ratio[1])
#
#    def __call__(self, xy: Tuple[int, int]) -> Tuple[int, int]:
#        """Map a tuple of x and y coordinates.
#
#        Args:
#            xy (Tuple[int, int]): The original coordinates as a tuple.
#
#        Returns:
#            Tuple[int, int]: The mapped coordinates as a tuple.
#        """
#        return self.map_x(xy[0]), self.map_y(xy[1])

class XYMapper:
    _instance = None

    def __new__(cls, input_dpi: Tuple[int, int]=(96, 96)):
        if cls._instance is None:
            cls._instance = super(XYMapper, cls).__new__(cls)
            cls._instance.initialize(input_dpi)
        else:
            # Check if the new input_dpi is None or matches the existing one
            if input_dpi is not None and input_dpi != cls._instance.input_dpi:
                raise ValueError(f"Cannot instantiate XYMapper with a different input_dpi: {input_dpi}. "
                                 f"Current input_dpi is {cls._instance.input_dpi}.")
        return cls._instance

    @classmethod
    def reset(cls):
        """Reset the singleton instance."""
        cls._instance = None

    def initialize(self, input_dpi: Tuple[int, int]):
        """Initialize the XYMapper with input DPI settings."""
        self.input_dpi = input_dpi  # Store the initial input DPI for comparison
        sys_dpi = get_dpi()
        self.ratio = (sys_dpi[0] / input_dpi[0], sys_dpi[1] / input_dpi[1])

    def map_x(self, x: int) -> int:
        """Map the x-coordinate according to the DPI ratio."""
        return round(x * self.ratio[0])

    def map_y(self, y: int) -> int:
        """Map the y-coordinate according to the DPI ratio."""
        return round(y * self.ratio[1])

    def __call__(self, xy: Tuple[int, int]) -> Tuple[int, int]:
        """Map a tuple of x and y coordinates."""
        return self.map_x(xy[0]), self.map_y(xy[1])


if __name__ == '__main__':
    print(get_dpi())
    mapper = XYMapper((144, 144))
    print(mapper((100, 100)))
