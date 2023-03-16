import pyautogui
import time

#print(pyautogui.position())

#time.sleep(7)
time.sleep(3)

#滑鼠移動到註冊
#移動到 1951 , 792 花 1 秒的時間移動過去

### stage 1 載log ###
pyautogui.moveTo(64,486,1) #點log按鈕
#滑鼠左鍵點擊一下
pyautogui.click()
#暫停1秒，等待網頁載入
time.sleep(1.5)


pyautogui.moveTo(814,81,1) #找log
#滑鼠左鍵點擊一下
pyautogui.click()
#暫停1秒，等待網頁載入
time.sleep(1.5)

pyautogui.moveTo(9,141,1) #開始選log
#滑鼠左鍵點擊一下
pyautogui.click()
#暫停1秒，等待網頁載入
time.sleep(1.5)

pyautogui.moveTo(88,744,1) #下載所選log
#滑鼠左鍵點擊一下
pyautogui.click()
#暫停1秒，等待網頁載入
time.sleep(25)
