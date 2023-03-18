import socket
import threading
import sys
import time
from block import Block
import specification

#server 接收 只會有一個執行緒
#client 傳送 會有好幾個 connected的client(socket物件) 被self.client_list紀錄
#socket.timeout https://vimsky.com/zh-tw/examples/detail/python-method-socket.timeout.html

class timeout(): ...


class Node():
    def __init__(self):
        #flag
        self.flag_stop = "run"   # 0 run,1 stop
        self.double_attack = False

        #attribute
            #server
        self.server = socket.socket()
        self.server_ip = str()
        self.server_port = int()
        self.server_list_client = []    #接上我server的client
        self.server_data = []   #接收到所有資料都放入此佇列
            #client
        self.client_list_server = []   #client(連接別人) 列表
            #白名單
        #self.node_list = ['10.1.1.123 5000', '10.1.1.35 5001', '10.1.1.35 5002', '10.1.1.35 5003']
        #self.ip_list = ['10.1.1.123', '10.1.1.35', '10.1.1.35', '10.1.1.35']
        self.node_list = ['140.132.105.52 5000', '140.132.105.52 5001', '140.132.105.52 5002', '140.132.105.52 5003']
        self.ip_list = ['140.132.105.52', '140.132.105.52', '140.132.105.52', '140.132.105.52']
        self.port_list = [5000, 5001, 5002, 5003]
        self.attack_decide_list = [0 for _ in range(len(self.port_list))]

        #init
        self.server_init()
        time.sleep(3)
        
        #現在好像已經不需要這兩行了?
        #while self.server_list_client == []:
            #pass
        
        #t = threading.Thread(target = self.server_retriever)
        #t.start()

#init
#==============================================
#server

    def server_init(self):
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_ip = socket.gethostbyname(socket.gethostname())
        self.server_port = 5000
        while True:
            try:
                self.server.bind((self.server_ip,self.server_port))
                break
            except:
                self.server_port += 1
                continue
        print('ip and port:',self.server_ip,self.server_port)
        self.server.listen(5)
        t = threading.Thread(target = self.server_listen)
        t.start()

    def server_listen(self):
        while True:
            try:
                self.server.settimeout(5)   #時間到引發例外跳到except
                client,addr = self.server.accept()
                for _ in range(len(self.node_list)):
                    if self.attack_decide_list[_] == 0 and self.server_port % 5000 != _:
                        self.attack_decide_list[_] = client.getpeername()[1]
                        break
                #print("[attack]",self.attack_decide_list)
                #print("[server_listen]accept client ",client)
                print("[server_listen]accept addr ",addr)
                client.send(("welcome! I'm "+str(self.server_ip)+" "+str(self.server_port)).encode("utf-8"))

                t = threading.Thread(target = self.server_recv_runner,args = (client,))
                t.start()
                self.server_list_client.append(client)

            except socket.timeout:
                if self.flag_stop == "stop":
                    print("[server_listen]stop")
                    self.server_data_recv_flag = "end"
                    break

            except:
                print("[server_listen]unknown error")

    def server_recv_runner(self,client):
        
        while self.flag_stop == "run":
            msg = self.server_recv(client)
            if(msg == False):
                time.sleep(5)
                break
            if(msg == timeout):
                continue
            if msg == "":
                try:
                    self.server_del_client(client)  #這裡用try因為預計在blockchain接收到exit就會移除
                except:
                    pass
                finally:
                    break
            flag = True
            spec = specification.specification(msg)
            for i in range(len(self.node_list)):
                if spec["content"] == self.node_list[i]:
                    self.server_data.append({"msg":{"tag":spec["tag"],"content":"FAKE","Appendix":self.port_list[i]},"source":client})
                    #print("[test_node.py]",self.port_list[i])
                    flag = False
                    break
                    
            #print("[test_node.py_i]",i)
            if (flag):
                """
                if(spec["tag"] == "block"):
                    for _ in range(len(self.node_list)):
                        if spec["content"].source == self.node_list[_]:
                            attack_decide_port = client.getpeername()[1]
                            self.attack_decide_list[_] = attack_decide_port
                """
                self.server_data.append({"msg":spec,"source":client.getpeername()[0]}) ###固定source做測試
                #print("[node]",self.attack_decide_list)
            #server_data = {{"msg":{"tag":tag,"content":content,"appendix":appendix}} ,"source":來源的socket物件}
            try:
                index = self.server_list_client.index(client)
            except:
                break

    def server_recv(self,client):
        try:
            #print("[server_listen]accept client_type ",client.raddr)
            #print("[server_listen]accept client ",client)
            #print("[server_listen]accept client_test ",client.getpeername()[0])
            #print("[server_listen]accept client_test_type ",type(client.getpeername()[0]))
            client.settimeout(5)
            msg = client.recv(65535).decode("utf-8")
            if(self.double_attack):
                self.broadcast(msg)
            else:
                #print("[server_recv]",msg,type(msg))
                if msg == "":
                    print("[server_recv] msg == \"\"")
                    time.sleep(5)
                return msg
        except ConnectionResetError:
            print("[server_recv]ConnectionResetError")
            return False
        except socket.timeout:
            return timeout
        except:
            print("[server_recv]unknown error")
            return False

    def server_del_client(self,client):
        try:
            self.server_list_client.remove(client)
        except:
            print("[server_del_client]error")

    def server_retriever(self): #回傳前會阻塞
        while self.flag_stop == "run":
            if len(self.server_data) > 0:
                try:
                    data = self.server_data.pop(0)
                    return data
                except:
                    print("[server_retriever]error")
        return None
#server
#==============================================
#client

    def client_init(self,port = None):
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        while 1:
            try:
                # original
                # ipt = input('plz input ip and port:').split()
                # ip = ipt[0]
                # port = int(ipt[1])
                # original

                # debug mode
                #if port == None:
                    #if self.server_port == 5000:
                        #port = 5001
                        #ip = self.server_ip
                    #elif self.server_port == 5001:
                        #port = 5000
                        #ip = self.server_ip
                    #else:
                        #ipt = input('plz input ip and port:').split()
                        #ip = ipt[0]
                        #port = int(ipt[1])
                
                if type(port) != int:
                    print("[client_init]type(port) != int")
                    raise TypeError
                else:
                    for _ in range(len(self.node_list)):
                        if port == self.port_list[_]:
                            #print("[node.client_init]client.connect(",self.port_list[_],",",port,")")
                            ip = self.ip_list[_]
                            client.connect((ip,port))
                            #print("[client_receive_port]",port)
                            #print("[client_receive_clientport]",client)
                            #print("[node.client_init]client.connect(",ip,",",port,")")
                    break
                """
                elif port == 5000:
                    ip = "140.132.99.115"
                elif port == 5001:
                    ip = "140.132.99.115"
                elif port == 5002:
                    ip = "140.132.99.115"
                elif port == 5003:
                    #print("it is problemmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
                    #break
                    ip = "140.132.99.115"
                else:
                    #print("0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo0 0 ooooo")
                    ip = self.server_ip
                client.connect((ip,port))
                #print("[node.client_init]client.connect(",ip,",",port,")")
                break
                """
                # debug mode
            except:
                print("[client_init]error:plz input angin!")
        self.client_list_server.append(client)
        print("[node.client_init]connect done!")

    def client_send(self,msg = "",client = ""):
        if client == "":    #沒有輸入client
            #client = self.client_list_server[0]
            print("[node.client_send]no pass client!")
        msg = str(msg)
        try:
            client.send((msg).encode("utf-8"))
        except:
            print("[client_send]error")
    
    def broadcast(self,msg = ""):
        for _ in self.client_list_server:
            self.client_send(msg,_)
#client
#==============================================
#others
    
    def stop(self):
        self.server_list_client = []
        self.client_list_server = []
        self.flag_stop = "stop"


if __name__ == "__main__":
    node = Node()
    #flag
    stop = 0    # 0 run, 1 stop
    while 1:
        msg = input()
        node.client_send(msg)
        if msg == 'exit':
            node.stop()
            break
        if msg == "show":
            print(node.server_data)

    time.sleep(2)

    
    stop = 1


