import win32gui
import win32con

def send_key(hwnd: int, c: str) -> None:
    """Send a single key press to the specified window.

    Args:
        hwnd (int): Handle to the window where the key press is sent.
        c (str): The character to send.
    """
    win32gui.SendMessage(hwnd, win32con.WM_CHAR, ord(c), 0)

def send_text(hwnd: int, text: str) -> None:
    """Send a string of text to the specified window, character by character.

    Args:
        hwnd (int): Handle to the window where the text is sent.
        text (str): The text string to send.
    """
    for c in text:
        send_key(hwnd, c)

def replace_text_in_edit_control(hwnd: int, new_text: str = ''):
    # Select all text in the Edit control
    win32gui.SendMessage(hwnd, win32con.EM_SETSEL, 0, -1)
    
    # Delete the selected text
    win32gui.SendMessage(hwnd, win32con.EM_REPLACESEL, True, new_text)

def get_text_from_control(hwnd: int, enc='utf-16-le') -> str:
    # Send the WM_GETTEXT message to get the length of the text
    text_length = win32gui.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH, 0, 0)
    
    if text_length == 0:
        return ""  # No text available

    # Create a buffer to hold the text
    # Allocate enough for UTF-16 (2 bytes per character)
    buffer_length = text_length * 2 
    buffer = bytes(buffer_length) 
    
    # Get the text from the control
    win32gui.SendMessage(hwnd, win32con.WM_GETTEXT, buffer_length, buffer)

    return buffer.decode(enc)

if __name__ == '__main__':
    import time
    from .process import execute, kill
    app = 'notepad.exe'
    execute(app)
    time.sleep(1)

    hwnd = win32gui.FindWindow(None, "Untitled - Notepad")
    if hwnd:
        edit = win32gui.FindWindowEx(hwnd, None, 'Edit', None)
        if edit:
            send_text(edit, 'Hello World!')
            time.sleep(1)
            replace_text_in_edit_control(edit)
    time.sleep(1)
    kill(app)
   
