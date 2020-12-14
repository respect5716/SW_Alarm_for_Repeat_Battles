import os
import numpy as np
import time
from simplepush import send
from playsound import playsound

import win32gui
import win32ui
from ctypes import windll

import pytesseract
from PIL import Image

def chdir():
    os.chdir(os.path.dirname(__file__))

def screenshot(hwnd):
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left + 200
    h = bot - top + 100

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    img = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)
    
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
    return img


def ocr(img):
    img = np.array(img)
    if img.shape[0] < 100:
        return "녹스 플레이어 창을 띄워주세요"
    # img = img[380:410, 330:630]
    text = pytesseract.image_to_string(img, lang='kor', config='--psm 4')
    text = text.strip()
    return text

def check(text):
    allowed_text = [
        "녹스 플레이어 창을 띄워주세요",
        "연속 전투가 종료되었습니다."
    ]
    for allowed in allowed_text:
        if allowed in text:
            return True, allowed
    return False, ''
    


def main():
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'
    hwnd = win32gui.FindWindow(None, '녹스 플레이어')
    chdir()
    patience = 0

    while True:
        img = screenshot(hwnd)
        text = ocr(img)
        done, text = check(text)
        if text and patience < 3:
            send('Fhg5gw', '서머너즈워', text)
            playsound('asset/sound.mp3')
            patience += 1
        elif done:
            pass
        else:
            patience = 0
        time.sleep(60)

if __name__ == '__main__':
    main()