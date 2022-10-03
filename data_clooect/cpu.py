import psutil
import hashlib    
import time
import node
import threading
import sys
import random
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("CPU&Memory.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
#記憶體

def writelog(self):
        f = open("CPU&Memory.log",'a')
        msg = str(ysy) + "," + cpu + ","
        f.write(msg)
        f.close()
        
i = 0
while i<= 360:
    mem = psutil.virtual_memory()
    # 系統總計記憶體
    zj = float(mem.total) / 1024 / 1024 / 1024
    # 系統已經使用記憶體
    ysy = float(mem.used) / 1024 / 1024 / 1024
    # 系統空閒記憶體
    kx = float(mem.free) / 1024 / 1024 / 1024

    cpu = (str(psutil.cpu_percent(1))) + '%'
    dk = psutil.disk_usage('/')
    total = dk.total / 1024 / 1024 / 1024
    used = dk.used / 1024 / 1024 / 1024
    #logging.info('')
    f = open("CPU&Memory.log",'a')
    msg = str(ysy) + "," + cpu + "\n"
    f.write(msg)
    f.close()
    i += 1;
    print(u"磁碟使用率: %s%%" % dk.percent)
    print(i)
    time.sleep(5)
