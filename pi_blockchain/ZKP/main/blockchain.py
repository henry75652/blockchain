from inspect import Attribute
from operator import attrgetter
from block import Block
import time
import threading
import random
import os

class Blockchain():
    def __init__(self):
        self.chain = []
        self.difficulty = 3
        self.blockqueue = []    # 待挖區塊
        self.others_ledge = dict() #{"140.132.1.1":[...]}
        self.malicious_score = [] #[{"client":<obj>,"score":0},{"client":<obj>,"score":0},...]
        self.count = 0
        random.seed()

        #flag
        self.STOP = int()
        self.PAUSE = int()
        self.UPDATE = int(0)    #是否有更新
        self.UPDATING = False   #是否正在更新

        self.CONFLICT = False   #發生衝突 ex兩個節點都在傳帳本
        self.LEDGE = False #是否正在傳帳本
        self.RECV_LEDGE = False

        #node
        self.port = int()

    def run(self,port):
        pass
        self.port = port
        genesis_block = Block("this_is_genesis_block",[100,100,100,100],"0.0.0.0 0",'random')
        genesis_block.timestamp = float(0)
        self.chain.append(genesis_block)

    def append_blockqueue(self,block):
        self.blockqueue.append(block)
        #block.print_block(debug="[append_blockqueue]")

    def remove_blockqueue(self,block):
        self.blockqueue.remove(block)
        self.write_log_block(block,"remove_blockqueue","remove_blockqueue")
        block.print_block(debug="remove_blockqueue")

    def append_blockchain(self,listChain):
        try:
            for _ in listChain: #檢查是不是為一個block的list
                if type(_) != Block: return False
            for _ in listChain:
                self.chain.append(_)
        except Exception as e:
            print("(error)[blockchain.append_blockchain]error:",e)

    def remove_blockchain(self,indexHead,indexTail):
        try:
            for i in range(indexHead,indexTail):
                #print("(debug)[others_ledge_replace]i:",i)
                self.chain.pop(len(self.chain)-1)    
            return True       
        except Exception as e:
            print("(error)[blockchain.remove_blockchain]error:",e)
            return False
        
    def print_blockqueue(self):
        print("\n[print_blockqueue]==================\n")
        for _ in self.blockqueue:
            _.print_block()
        print("\n[print_blockqueue]==================\n")

    def others_ledge_set(self,source):
        if(source == None):
            print("(debug)[blockchain.others_ledge_set]parameter source is None!")
            return False
        else:
            self.others_ledge = {source:[]}
            return True

    def others_ledge_append(self,block):
        #print("(debug)[blockchain.others_ledge_append]start")
        if(type(block) != Block):
            print("(error)[blockchain.others_ledge_append]type is not block obj!")
            return False
        else:
            try:    #會報錯通常是因為沒有收到send_ledge 的設定，所以沒有call過self.others_ledge_set會出out of range
                print("(debug)[blockchain.others_ledge_append]",self.others_ledge[list(self.others_ledge.keys())[0]].append(block))
                return True
            except:
                print("(error)[blockchain.others_ledge_append]others_ledge hasn't been set")
                return False

    def others_ledge_verify(self):
        print("(debug)[others_ledge_verify]start")
        print("(debug)[others_ledge_verify]self.others_ledge:",self.others_ledge)
        #others_chain = self.others_ledge[list(self.others_ledge.keys())[0]]  #others_chain和others_ledge最大的差別在於後者是一個字典 key 是來源的資訊，前者則是單純的鏈(list)
        try:    #這裡會引發例外也是因為沒有收到others_ledge_set
            #print("(debug)[others_ledge_verify]head id:",self.others_ledge[list(self.others_ledge.keys())[0]][0].id,"tail id:",self.others_ledge[list(self.others_ledge.keys())[0]][-1].id) #self.others_ledge[list(self.others_ledge.keys())[0]]會得到一個list裡面有收來的block
        
            others_chain = self.others_ledge[list(self.others_ledge.keys())[0]]  #others_chain和others_ledge最大的差別在於後者是一個字典 key 是來源的資訊，前者則是單純的鏈(list)
            #print("(debug)[others_ledge_verify]others_chain:",others_chain)
            if(others_chain[0].prev_hash != self.chain[others_chain[0].id-1].get_blockhash()):  #其他帳本跟自己的接不上
                print("(debug)[others_ledge_verify]test verify failed!")
                return False
            print("(debug)[others_ledge_verify]len(others_chain)",len(others_chain))
            #self.others_ledge_show()
            #比對prevhash
            self.others_ledge_replace()
            print("(debug)[others_ledge_verify]test verify successful!")
            return True
        except:
            print("(debug)[others_ledge_verify]except")

    def others_ledge_replace(self): #驗證都通過才可以來這裡
        try:
            others_chain = self.others_ledge[list(self.others_ledge.keys())[0]]
            #self.print_blockchain(debug="before pop")
            if(not(self.remove_blockchain(others_chain[0].id,len(self.chain)))): return False
            self.append_blockchain(others_chain)
            print("(debug)[others_ldege_replace]===================================")
            for _ in self.blockqueue:
                for x in others_chain:
                    #_.print_block("_")
                    #x.print_block("x")
                    if _.is_same_as(x):
                        self.remove_blockqueue(_)
                        print("(debug)[ohters_ledge_replace]same")
                    else: print("(debug)[others_ledge_replace]diff")
        except Exception as e:
            print("(debug)[others_ledge_replace]except:\n\t",e)
        finally:
            #self.print_blockchain("(debug)[others_ledge_replace]")
            pass

    def others_ledge_show(self):
        if len(self.others_ledge) <= 0:
            return False
        for _ in self.others_ledge[list(self.others_ledge.keys())[0]]:
            _.print_block("others_ledge_show")
        return True

    def update_blockchain(self,block):#input:block
        self.UPDATED = False
        while self.UPDATING == True: pass #有別的執行續正在更新
        self.UPDATING = True
        verify = self.verify(block)
        if(verify == True):
            self.UPDATE = 1
            for _ in self.blockqueue:
                if _.is_same_as(block):
                    self.remove_blockqueue(_)
                    _.print_block(debug="[update_blockchain]")
            block.id = len(self.chain)
            self.chain.append(block)
            self.UPDATED = True

            self.write_log_block(block,"appended")
            #print("[blockchain.update_blockchain]the appended block is==================")
        else:
            if verify == "two same prev_hash":
                self.write_log_block(block,"dropped",debug = verify)
                return "two same prev_hash"
                
            #print("[blockchain.update_blockchain]the dropped block is==================")
        self.UPDATING = False

    def send_ledge(self,node = None):   #傳送帳本
        if(self.RECV_LEDGE == True):
            self.IS_conflict()
            return False
        self.LEDGE = True
        if(node ==  None):
            print("[blockchain.send_ledge]error:plz input node!")
            self.LEDGE = False
            return False
        else:
            print("[blockchain.send_ledge]run")
            node.broadcast("send_ledge from "+str(len(self.chain) - 9 - 1)+" to "+str(len(self.chain) - 1)) #都要減一是因為起始區塊佔一個
            pass
            time.sleep(3)
            for i in range(10):
                print("\nI am sending my chain!(self.LEDGE = ",self.LEDGE,"\n")
                #print("(debug)[blockchain.send_ledge]index value = ",-(10 - i))
                self.chain[-(10 - i)].print_block()
                #print("(debug)=======\n")
                #self.print_blockchain()
                node.broadcast("ledge//"+self.chain[-(10 - i)].conv_block_to_str()+"//appendix//test") #self.chain[-1 ~ -10]
                time.sleep(0.1)
                #pa = input("press any key to continue...")
                if(self.CONFLICT == True or self.STOP == 1):
                    self.LEDGE = False
                    return False

            self.LEDGE = False
            return True

    def IS_conflict(self):
        self.CONFLICT = True
        for i in range(10):
            print("===")
            if(self.STOP == 1):
                break

    def verify(self,block): #input:block, output:True(bool),(str)
        #fake hash (假hash)
            #check prev_hash (檢查prev_hash欄位是否不符規則)
        if(block.prev_hash != self.chain[-1].get_blockhash(CallBy="blockchain.verify")):
            if(block.prev_hash == self.chain[-2].get_blockhash(CallBy="blockchain.verify")):
                return "two same prev_hash"
            return "invalid prev_hash"
        
            #check current hash (檢查區塊的hash是否符合規則)
        info_str_hex = block.info.data[-4:-1].encode('utf-8')
        info_dec = int(info_str_hex.hex(), 16) % 10
        self.difficulty = (info_dec % 2) + 1
        #print("(debug)[blockchain.verify_dif]",self.difficulty)
        if(block.get_blockhash()[0:self.difficulty] != '0' * self.difficulty):
            return "current hash is fake"
        #same content
        attribute = ["timestamp","nonce","prev_hash","information.data","source"]
        for _ in self.chain:
            result = _.cmp(block)   #result == ["timestamp","nonce"]
            count = 0
            for x in attribute:
                if x in result:
                    count += 1
            if count >= len(attribute):
                return "same content"

        #print("[blockchain.verify]successful!")
        return True

    def print_blockchain(self,debug = ""):
        print("[print_blockchain]",self)
        for _ in self.chain:
            _.print_block(debug)
            #time.sleep(0.5)

    def blockchain_stop(self):
        self.STOP = 1
        print("[blockchain.blockchain_stop]stop,len of blockqueue is ",len(self.blockqueue))

    def blockchain_pause(self,call=""):
        self.PAUSE = 1
        print("[blockchain.blockchain_pause]pause,len of blockchain is ",len(self.chain),"call by",call)

    def blockchain_resume(self):
        self.PAUSE = 0
        self.CONFLICT = False   #發生衝突 ex兩個節點都在傳帳本
        self.LEDGE = False #是否正在傳帳本
        self.RECV_LEDGE = False
    
    def mine(self):
        #print("(debug)[blockchain.mine]start")
        if(len(self.blockqueue) >= 1):
            self.blockqueue[0].nonce = 1
            self.blockqueue[0].prev_hash = str(self.chain[-1].get_blockhash(CallBy="blockchain.mine::prev_hash"))
            block_hash = self.blockqueue[0].get_blockhash()
            
            info_str_hex = self.blockqueue[0].info.data[-4:-1].encode('utf-8')
            info_dec = int(info_str_hex.hex(), 16) % 10
            self.difficulty = (info_dec % 2) + 1
            
            self.UPDATE = 0

            #self.blockqueue[0].nonce = random.getrandbits(32)
            #print("[blockchain.mine]original nonce = ",self.blockqueue[0].nonce)
            #self.blockqueue[0].prev_hash = str(self.chain[-1].get_blockhash(CallBy="blockchain.mine::prev_hash"))
            while block_hash[0:self.difficulty] != '0' * self.difficulty:
                try:
                    self.blockqueue[0].nonce += 1
                    block_hash = self.blockqueue[0].get_blockhash(CallBy="blockchain.mine::try")
                except IndexError:
                    print("(error)[blockchain.mine]IndexError!")
                if self.UPDATE == 1:
                    print("(error)[blockchain.mine]interrupt")
                    #time.sleep(1)
                    return False
                if self.PAUSE == 1:
                    print("(debug)[blockchain.mine.pause]pause")
                    while(self.PAUSE != 0  and self.STOP != 1):
                        time.sleep(1)
                    return False
                if self.STOP == 1:
                    return False    #我從pass改成False原因是我發現main.miner好像在結束後還會跑一段


            block = self.blockqueue.pop(0)
            test = self.update_blockchain(block)
            if test == "two same prev_hash":
                block.nonce = 1
                block.prev_hash = str(self.chain[-1].get_blockhash(CallBy="blockchain.mine::prev_hash"))
                block_hash = block.get_blockhash()
                while block_hash[0:self.difficulty] != '0' * self.difficulty:
                    try:
                        block.nonce += 1
                        block_hash = block.get_blockhash(CallBy="blockchain.mine::try")
                    except IndexError:
                        print("(error)[blockchain.mine]IndexError!")
                self.UPDATING = False
                #while(1):
                    #print("blockchain.result = ",self.UPDATING)
                self.update_blockchain(block)
            return block

    def write_log(self,port = 0,debug = "writelog",bDebug = True,show=True):
        result = os.getcwd().split("\\")
        #print("blockchain.result = ",result)
        if result[-1] == "blockchain":
            path = "./log/"
        elif result[-1] == "main":
            path = "../log/"  
        else:
            print("[write_log]current path error!")    
        #print("[blockchain.write_log]result = ",result)
        #print("[blockchain.write_log]","{path}blockchain.log".format(path = path))
        '''
        if port == 5000:
            f = open("{path}5000/blockchain.log".format(path = path),'w')
        elif port == 5001:
            f = open("{path}5001/blockchain.log".format(path = path),'w')
        elif port == 5002:
            f = open("{path}5002/blockchain.log".format(path = path),'w')
        '''
        f = open("{path}{port}/blockchain.log".format(path = path,port = self.port),'w')
        msg = str()
        for _ in self.chain:
            #msg += _.print_block("write_log port:"+(str(port)))
            msg += _.print_block(("write_log port:"+(str(port))) * int(bDebug),show=show)
        
        f.write(msg)
        f.close()

    def write_log_block(self,block,type = "droppped",debug = ""):
        result = os.getcwd().split("\\")
        if result[-1] == "blockchain":
            path = "./log/"
        elif result[-1] == "main":
            path = "../log/"  
        else:
            print("[write_log]current path error!")
        #print("[blockchain.write_log]result = ",result)
        #print("[blockchain.write_log]","{path}blockchain.log".format(path = path))
 
        f = open("{path}{port}/verify_{port}_{type}.log".format(path = path,port = self.port,type = type),'a')

        msg = str()
        msg = block.print_block(show = False,debug = debug)
        
        f.write(msg)
        f.close()

    def write_check_log_block(self,block,type = "droppped",debug = "",final_time = "",miner = ""): ##改type
        result = os.getcwd().split("\\")
        if result[-1] == "blockchain":
            path = "./log/"
        elif result[-1] == "main":
            path = "../log/"  
        else:
            print("[write_log]current path error!")
        #print("[blockchain.write_log]result = ",result)
        #print("[blockchain.write_log]","{path}blockchain.log".format(path = path))

        f = open("{path}{port}/verify_{port}_{type}.log".format(path = path,port = self.port,type = type),'a')

        msg = str()
        msg = block.print_block(show = False,debug = debug)
        msg += "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
        msg += "str_data:"
        msg_str = self.chain[-1].info.data
        #print("[test_blockchain.py]")
        msg += msg_str
        msg += "\n"
        msg += "finish_time:"
        msg += final_time
        msg += "\n"
        msg += "miner:"
        msg += miner
        msg += "\n"
        msg += "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"

        f.write(msg)
        f.close()

    def write_log_blockqueue(self,type = "droppped"): ##改type
        result = os.getcwd().split("\\")
        if result[-1] == "blockchain":
            path = "./log/"
        elif result[-1] == "main":
            path = "../log/"  
        else:
            print("[write_log]current path error!")
        #print("[blockchain.write_log]result = ",result)
        #print("[blockchain.write_log]","{path}blockchain.log".format(path = path))

        f = open("{path}{port}/verify_{port}_{type}.log".format(path = path,port = self.port,type = type),'w')

        msg = str()
        for _ in range(len(self.blockqueue)):
            msg += str(self.blockqueue[_].source)
            msg += "\n"
            msg += str(self.blockqueue[_].timestamp)
            msg += "\n"
            msg += "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"

        f.write(msg)
        f.close()

    def ShowStatus(self,ident = 0):
        print("\t"*ident,"[Blockchain.ShowStatus]","\n",
            "\t"*(ident+1),"STOP:",self.STOP,"\n",
            "\t"*(ident+1),"PAUSE:",self.PAUSE,"\n",
            "\t"*(ident+1),"UPDATE:",self.UPDATE,"\n",
            "\t"*(ident+1),"UPDATING:",self.UPDATING,"\n",

            "\t"*(ident+1),"CONFLICT:",self.CONFLICT,"\n",
            "\t"*(ident+1),"LEDGE:",self.LEDGE,"\n",
            "\t"*(ident+1),"RECV_LEDGE:",self.RECV_LEDGE,"\n",
            sep="")

    def Set_malicious_score(self,node = None):
        if(node == None):
            print("(error)[Set_malicious_score]")
            return False
        print("(debug)[Set_malicious_score]node:",node)
        self.malicious_score = [] #先清空 讓這個方法可以用作renew
        for x in node.server_list_client:
            self.malicious_score.append({"client":x,"score":0})
        print("(debug)[Set_malicious_score]malicious_score:",self.malicious_score)

    def Inc_malicious_score(self,client = None):
        if(client == None):
            print("(error)[Inc_malicious_score]client = None")
            return False
        #print("(debug)[Inc_malicious_score]self.malicious_score:",self.malicious_score)
        #print("(debug)[Inc_malicious_score]client:",client)
        i = -1
        for x in self.malicious_score:
            if(x["client"] == client):
                i = self.malicious_score.index(x)
        print("(debug)[Inc_malicious_score]i:",i)
        print("(deubg)[Inc_malicious_score]self.malicious_score:",self.malicious_score)
        if(i != -1): self.malicious_score[i]["score"] += 5

    def MinusAll_malicious_score(self,score = 0):
        if(type(score) != int):
            print("(error)[MinusAll_malicious_score]")
            return False
        for x in self.malicious_score:
            x["score"] -= score
            if(x["score"] <= 0): x["score"] = 0
        
        return True

if __name__ == "__main__":
    block1 = Block("this is block1")
    block1.id = 1
    block2 = Block("this is block2")
    block2.id = 2
    
    block1.print_block()
    blockchain = Blockchain()
    blockchain.run()
    blockchain.update_blockchain(block1)
    blockchain.update_blockchain(block2)
    print("\n\n\n")
    blockchain.print_blockchain()