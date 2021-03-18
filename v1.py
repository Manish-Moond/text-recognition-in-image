from pytesseract import pytesseract
from PIL import Image
import pyscreenshot as ImageGrab
import pyautogui
import keyboard
import string
import threading
import time
import pyperclip


pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
x1 = y1 = x2 = y2 = -1
pressed_key = ''


def position():
    global pressed_key, x1, y1, x2, y2
    while True:
        time.sleep(1)
        print(pyautogui.position())
        if pressed_key != '':
            if pressed_key == 's':
                x1, y1 = pyautogui.position()
                print(x1, y1, "x1y1")
                pressed_key = ''
            if pressed_key == 'e':
                x2, y2 = pyautogui.position()
                print(x2, y2, "x2y2")
                pressed_key = ''
            # x, y = pyautogui.position()
            # print(x, y)
            # pressed_key = ''


keys = list(string.ascii_lowercase)

# Optional code(extra keys):

keys.append("space_bar")
keys.append("backspace")
keys.append("shift")
keys.append("esc")


def listen(key):
    global pressed_key
    while True:
        keyboard.wait(key)
        print("[+] Pressed", key)
        pressed_key = key


def take_screenshot():
    global x1, y1, x2, y2
    while True:
        time.sleep(0.1)
        print(x1, y1, x2, y2)
        if x1 >= 0 and y1 >= 0 and x2 >= 0 and y2 >= 0:
            img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            img.save('img.png')
            x1 = x2 = y1 = y2 = -1


def convert_to_text():
    while True:
        time.sleep(1)
        image = Image.open('img.png')
        txt = pytesseract.image_to_string(image)
        pyperclip.copy(txt)
        print(txt)


key_threads = [threading.Thread(
    target=listen, kwargs={"key": key}) for key in keys]
for thread in key_threads:
    thread.start()

position_thread = threading.Thread(target=position)
position_thread.start()

image_thread = threading.Thread(target=take_screenshot)
image_thread.start()

txt_thread = threading.Thread(target=convert_to_text)
txt_thread.start()
