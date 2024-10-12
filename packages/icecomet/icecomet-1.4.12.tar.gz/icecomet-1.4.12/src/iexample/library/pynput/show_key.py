import cv2 as cv
from iprint import *
import numpy as np




from pynput import keyboard

def on_press(key):
    try:
        ij(key.char,end=' : ')
        ij(key.char,'t')
    except AttributeError:
        ij(key,end=' ')
        ij(key,'t')

def on_release(key):
    ij(str(key)[1:-1]+' : releas',c=ct.set)
    ij(key,'ti')
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()













