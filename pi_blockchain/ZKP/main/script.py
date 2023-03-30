import pyautogui
import time

time.sleep(3)

for a in range(11):
    if a == 0:
        pyautogui.moveTo(292,319,1)
    pyautogui.click()

pyautogui.moveTo(51,335,1) #下載所選log
#滑鼠左鍵點擊一下
pyautogui.click()
time.sleep(1.5)

pyautogui.moveTo(64,379,1) #下載所選log
#滑鼠左鍵點擊一下
pyautogui.click()
time.sleep(1.5)

pyautogui.moveTo(763,42,1) #下載所選log
#滑鼠左鍵點擊一下
pyautogui.click()
time.sleep(1.5)

pyautogui.moveTo(9,71,1) #下載所選log
#滑鼠左鍵點擊一下
pyautogui.click()
time.sleep(1.5)

pyautogui.moveTo(72,695,1) #下載所選log
#滑鼠左鍵點擊一下
pyautogui.click()
time.sleep(25)

