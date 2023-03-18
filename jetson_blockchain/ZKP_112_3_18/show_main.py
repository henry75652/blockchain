from node import Node
from blockchain import Blockchain
from block import Block
import time
import threading
import ECC

#global variable
STOP = int()    # 0 run, 1 stop
node = Node()
blockchain = Blockchain()
ECC_1 = ECC.Ecc()
#golbal variable
count = 0

def init():
    #init

    t = threading.Thread(target = retriever,args = (node,))
    t.start()

    t = threading.Thread(target = miner,args = (blockchain,))
    #if node.server_port == 5000:t.start()
    t.start()
    
    test_blockchain_queue = []  #改_1  #驗證更新區塊鏈佇列
    test_block_queue = []    #改_1 驗證佇列

    if node.server_port == 5000:
        port = 5001
        node.client_init(port)
        port = 5002
        node.client_init(port)
        #port = 5003
        #node.client_init(port)
    elif node.server_port == 5001:
        port = 5000
        node.client_init(port)
        port = 5002
        node.client_init(port)
        #port = 5003
        #node.client_init(port)
    elif node.server_port == 5002:
        port = 5000
        node.client_init(port)
        port = 5001
        node.client_init(port)
        #port = 5003
        #node.client_init(port)
    #elif node.server_port == 5003:
        #port = 5000
        #node.client_init(port)
        #port = 5001
        #node.client_init(port)
        #port = 5002
        #node.client_init(port)
    else:
        print("[main.init]unknown error!")
    

def miner(blockchain):
    while STOP == 0:
        while len(blockchain.blockqueue) >= 1:
            block = blockchain.mine()
            if block == False:  #代表有人先挖到 有更新
                break
            block.print_block("[main.miner]I mined a block")
            #node.broadcast("update//"+block.conv_block_to_str(0)+"//appendix//"+ECC_1.sign_ECDSA_msg(block.get_blockhash()).decode('utf-8')+"//this is mined by node//"+str(node.server_port)+" "+str(node.server_ip))
            node.broadcast("update//"+block.conv_block_to_str(0)+"//appendix//"+ECC_1.sign_ECDSA_msg(block.get_blockhash()).decode('utf-8'))
    pass


def retriever(node):
    global STOP
    global count
    while STOP == 0:
        data = node.server_retriever()  #if node stop, data == None
        # data = {{"msg":{"tag":tag,"content":content,"appendix":appendix}} ,"source":來源的socket物件}
        if(data == None): 
            # node stop
            break

        if(type(data) == dict):
            
            if data["msg"]["tag"] == "block":
                print("[retriever]:data is block type")
                data["msg"]["content"].print_block("call by block")
                ver_block_hash = data["msg"]["appendix"]
                compar_block_hash = data["msg"]["content"].get_blockhash()
                if ECC_1.validate_signature(ver_block_hash,compar_block_hash):
                    blockchain.update_blockqueue(data["msg"]["content"])
                else:
                    print("not pass verification")
            
            elif data["msg"]["tag"] == "cmd":
                print("[retriever]:data is string type")
                print("[retriever]",data["msg"]["content"])
            
            elif data["msg"]["tag"] == "update":
                print("[retriever]:data is for updating blockchain",blockchain)
                data["msg"]["content"].print_block("call by update")
                ver_blockchain_hash = data["msg"]["appendix"]
                compar_blockchain_hash = data["msg"]["content"].get_blockhash()
                if ECC_1.validate_signature(ver_blockchain_hash,compar_blockchain_hash):
                    if blockchain.verify_change(data["msg"]["content"],count):
                        blockchain.update_blockchain(data["msg"]["content"])
                else:
                    print("not pass verification")
                    
                count += 1
                
            elif data["msg"]["tag"] == "stop":
                print("[retriever]:data is stop cmd")
                print("[retriever]",data["msg"]["content"])
                ip_port = node.server_ip+" "+str(node.server_port)
                print("test",ip_port)
                if data["msg"]["content"] == ip_port:
                    print("in")
                    STOP = 1
                    node.stop()

            print("[main.retriever]appendix:",data["msg"]["appendix"])
        
        else:
            print("[retriever]:data is not type dict")

        pass


def new_block():
    info = input("new block:")
    #global info ##
    #info = info + 1 ##
    block = Block(info,node.server_ip+":"+str(node.server_port))
    block.id = len(blockchain.chain)
    node.broadcast("block//"+block.conv_block_to_str(0)+"//appendix//"+ECC_1.sign_ECDSA_msg(block.get_blockhash()).decode('utf-8'))
    #node.broadcast("block//"+block.conv_block_to_str(0)+"//appendix//test")
    blockchain.update_blockqueue(block) ##

def terminal_stop():
    info = input("stop node ip_port:")
    node.broadcast("stop//"+info+"//appendix//this is from node//"+str(node.server_port)+" "+str(node.server_ip))
    

if __name__ == "__main__":
    init()
    
    #flag
    STOP = 0

    #nodelist = ['140.132.26.237 5000', '140.132.26.237 5001', '140.132.26.237 5002'] ##
    info = 10 ##

    #run
    blockchain.run(node.server_port)
    while STOP == 0:
        
        #if (str(node.server_ip)+" "+str(node.server_port)) == nodelist[0]: ##
            #print("in")
            #time.sleep(30)
            #msg = "new block"
            #node.broadcast(msg)
        #elif (str(node.server_ip)+" "+str(node.server_port)) == nodelist[1]:
            #time.sleep(30)
            #msg = ""  
        #elif (str(node.server_ip)+" "+str(node.server_port)) == nodelist[2]:
            #time.sleep(30)
            #msg = ""
            #node.broadcast(msg)  ##
        
        msg = input()
        node.broadcast(msg)
        
        #blockchain.write_log(port = node.server_port) ##

        if msg == 'exit':
            break
        if msg == "show blockchain":
            #blockchain.print_blockchain()
            blockchain.write_log(port = node.server_port)
        if msg == "show blockqueue":
            print(blockchain.blockqueue)
        if msg == "show block":
            if len(blockchain.blockqueue) >= 1:
                blockchain.blockqueue[int(input("input index:"))].print_block()
            else: print("[main]there is not anything in blockqueue!")
        if msg == "new block":
            block = new_block()
        if msg == "stop":
            terminal_stop()
        if msg == "show serverlist":
            print("[main]show serverlist:",node.server_list_client)
        if msg == "show clientlist":
            print("[main]show clientlist:",node.client_list_server)

    blockchain.blockchain_stop()

    time.sleep(1)
    node.stop()
    STOP = 1

    