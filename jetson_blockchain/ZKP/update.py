
import time

f = open("update_record.txt",'a+',encoding = "utf-8")
f.seek(0)
buffer = f.read()
try:
    buffer = buffer.split("==========")[-2]
    print("上一筆紀錄:\n==========",buffer,"==========",sep = "")
except IndexError:
    print("沒有上一筆紀錄")
except:
    print("未知的錯誤")
version = input("\n新版本號:")
print("紀錄訊息(輸入 qq 終止)")
msg = str()

while True:
    temp = input(">")
    if(temp[0:2] == "qq"): break
    msg += temp + '\n'
payload = str()
payload = "==========\n時間:"+time.ctime(time.time())+"\n版本號:"+str(version)+"\n紀錄訊息:\n"+str(msg)+"==========\n"
f.write(payload)
f.close()
