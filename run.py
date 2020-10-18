import os
import numpy as np
import time
import slack

import win32gui
import win32ui
from ctypes import windll

import pytesseract
from PIL import Image

def chdir():
    os.chdir(os.path.dirname(__file__))

def load_token():
    with open('slack_token.txt', 'r') as f:
        token = f.read()
    return token

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
    assert img.shape[0] > 500, "녹스 플레이어 창을 띄워주세요."
    img = img[380:410, 330:630]
    img = np.where(img < 70, 0, img)
    text = pytesseract.image_to_string(img, lang='kor', config='--psm 4')
    text = text.strip()
    return text

def check(text):
    return text == '연속 전투가 종료되었습니다.'

def send_message(channel, token):
    text = '연속 전투가 종료되었습니다. 확인 해주세요.'
    client = slack.WebClient(token)
    client.chat_postMessage(channel=channel, text=text)    


def main():
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'
    hwnd = win32gui.FindWindow(None, '녹스 플레이어')
    
    chdir()
    token = load_token()
    patience = 0

    while True:
        img = screenshot(hwnd)
        text = ocr(img)
        done = check(text)
        if done and patience < 3:
            send_message('#game', token)
            patience += 1
        elif done:
            pass
        else:
            patience = 0
        print(patience)
        time.sleep(60)

if __name__ == '__main__':
    main()