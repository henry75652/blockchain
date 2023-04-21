import os
import threading
import time

anaconda = "C:/Users/user/anaconda3/python.exe"
python3 = "python3"
cmd = "D:/文件/實作需要/進階/真實作/blockchain/new_blockchain/胖子/blockchain/main.py"
log = "D:/文件/實作需要/進階/真實作/blockchain/new_blockchain/胖子/blockchain/log"



def node1():
    #os.system("conda activate base")
    os.system("start \"node1\" /wait C:/Users/user/Anaconda3/python.exe runner.py 1")
def node2():
    #os.system("conda activate base")
    os.system("start \"node2\" /wait C:/Users/user/Anaconda3/python.exe runner.py 2")
def node3():
    #os.system("conda activate base")
    os.system("start \"node3\" /wait C:/Users/user/Anaconda3/python.exe runner.py 3")
def node4():
    #os.system("conda activate base")
    os.system("start \"node4\" /wait C:/Users/user/Anaconda3/python.exe runner.py 4")
    
if __name__ == "__main__":
    os.system("{log}\\del.bat".format(log = log))
    t1 = threading.Thread(target = node1)
    t2 = threading.Thread(target = node2)
    t3 = threading.Thread(target = node3)
    t4 = threading.Thread(target = node4)
    t1.start()
    time.sleep(0.3)
    t2.start()
    time.sleep(0.3)
    t3.start()
    time.sleep(0.3)
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    print("[main]done")


