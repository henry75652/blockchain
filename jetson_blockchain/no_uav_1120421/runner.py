import os
import threading
import sys

anaconda = "C:/Users/user/Anaconda3/python.exe"
python = "C:/Users/user/Anaconda3/python.exe"
cmd = "main/main.py"
log = "D:/文件/實作需要/進階/真實作/blockchain/new_blockchain/胖子/blockchain/log/log{}.log"

def runner(num):
    #if num == 0: num = "" 原本是log.log

    #payload = "{runner} {cmd} > log/{node}/log{log}.log 2>&1".format(runner = python,cmd = cmd,node = num + 4999,log = "")
    payload = "{runner} {cmd}".format(runner = python,cmd = cmd,log = num)
    
    print("[runner]payload = ",payload)
    os.system(payload)
    
if __name__ == "__main__":
    runner(int(sys.argv[1]))
    
