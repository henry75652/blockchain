from block import Block
import time
import threading
import random
import os

class Blockchain():
    def __init__(self):
        self.chain = []
        self.difficulty = 4
        self.blockqueue = []    # 待挖區塊
        self.count = 0
        random.seed()

        #flag
        self.STOP = int()
        self.UPDATE = int(0)    #是否有更新
        self.UPDATING = False   #是否正在更新
        self.UPDATED = False

        #node
        self.port = int()

    def run(self,port):
        pass
        self.port = port
        genesis_block = Block("this is genesis block",[100,100],"0.0.0.0 0",'random')
        #self.update_blockchain(genesis_block) 6.27
        genesis_block.timestamp = float(0)
        self.chain.append(genesis_block)
        
    def update_blockchain(self,block):
        self.UPDATED = False
        while self.UPDATING == True: pass #有別的執行續正在更新
        self.UPDATING = True
        verify = self.verify(block)
        if(verify == True):
            #print("[blockchain.update_blockchain]self.UPDATE = 1")
            self.UPDATE = 1
            for _ in self.blockqueue:
                if _.is_same_as(block):
                    #print("[test]")
                    self.remove_blockqueue(_)
            block.id = len(self.chain)  #6.27
            self.chain.append(block)
            self.UPDATED = True
        else:
            print("[blockchain.update_blockchain]verify failed!") 
            #print("[blockchain.update_blockchain]block") #6.27
            block.print_block() #6.27
        self.UPDATING = False

    def request_ledger(self,node = None):   #和別的節點要求帳本
        if(node ==  None): print("[blockchain.request_ledger]error:plz input node!")
        else:
            node.broadcast("request_ledger")
            pass
        
    def append_blockqueue(self,block):
        self.blockqueue.append(block)
        #print("[append_blockqueue]new update,len is ",len(self.blockqueue))

    def remove_blockqueue(self,block):
        self.blockqueue.remove(block)
        #print("[append_blockqueue]new update,len is ",len(self.blockqueue))


    def print_blockqueue(self):
        print("\n[print_blockqueue]\n")
        for _ in self.blockqueue:
            _.print_block()
        print("\n[print_blockqueue]\n")

    #def verify(self,block): #if block has in the chain, failed  #大改
    #    for _ in self.chain:
    #        if _.is_same_as(block):
    #            print("[blockchain.verify]fail:there had the same block!")
    #            return False
    #    print("[blockchain.verify]success!")
    #    return True

    def verify(self,block): #input:block, output:True(bool),(str)
        #fake hash (假hash)
            #check prev_hash (檢查prev_hash欄位是否不符規則)
        if(block.prev_hash != self.chain[-1].get_blockhash()):
            print("fake prev_hash")
            return "fake prev_hash"
        
            #check current hash (檢查區塊的hash是否符合規則)
        if(block.get_blockhash()[0:self.difficulty] != '0' * self.difficulty):
            print("current hash is fake")
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
                print("same content")
                return "same content"

        print("[blockchain.verify]successful!")
        return True

    def verify_change(self,temp_blockchain,count):  #改爆_1
        if count == 0:
            print("[genesis]")
            return True
        else:
            if temp_blockchain.prev_hash == self.chain[-1].get_blockhash():
                print("[correct_chain]")
                return True
            if temp_blockchain.prev_hash == self.chain[-1].prev_hash:
                print("[correct_chain_but_other_has]")
                return False
            print("[fake_chain]")
            return False
            """
            if temp_blockchain.id - self.chain[-1].id == 1: 
                if temp_blockchain.prev_hash == self.chain[-1].get_blockhash():
                    print("[correct_chain]")
                    return True
                else:
                    print("[fake_chain]")
                    return False
            else:
                    #if self.get_blockhash(temp_blockchain.chain[-1]) == self.get_blockhash(self.chain[-1]):
                if temp_blockchain.prev_hash == self.chain[-1].prev_hash:   
                    print("[correct_chain]")
                    return True
                else:
                    print("[fake_chain]")
                    return False
            """

    def print_blockchain(self):
        print("[print_blockchain]",self)
        for _ in self.chain:
            _.print_block()
            time.sleep(0.5)

    def blockchain_stop(self):
        self.STOP = 1

    def mine(self):
        if(len(self.blockqueue) >= 1):
            block_hash = self.blockqueue[0].get_blockhash()
            self.UPDATE = 0

            #print("[blockchain.mine]self.UPDATE = 0")
            #self.blockqueue[0].nonce = random.getrandbits(32)
            self.blockqueue[0].nonce = 0
            print("[blockchain.mine]original nonce = ",self.blockqueue[0].nonce)
            self.blockqueue[0].prev_hash = str(self.chain[-1].get_blockhash())
            while block_hash[0:self.difficulty] != '0' * self.difficulty:
                try:
                    self.blockqueue[0].nonce += 1
                    block_hash = self.blockqueue[0].get_blockhash()
                except IndexError:
                    print("[blockchain.mine]IndexError!")
                if self.UPDATE == 1:
                    #進度 重挖
                    print("[blockchain.mine]interrupt")
                    #time.sleep(1)
                    return False
                if self.STOP == 1:
                    break
            
            block = self.blockqueue.pop(0)
            self.update_blockchain(block)
            return block

    def write_log_check(self,port = 0,final_time = "",miner = ""): 

        if port == 5000:
            f = open("blockchain_check.log",'a')
        elif port == 5001:
            f = open("blockchain2_check.log",'a')
        elif port == 5002:
            f = open("blockchain3_check.log",'a')
        elif port == 5003:
            f = open("blockchain4_check.log",'a')
        elif port == 5004:
            f = open("blockchain5_check.log",'a')
        else:
            f = open("blockchain_secial_check.log",'a')
        

        msg = str()
        msg = self.chain[-1].print_block("write_log port:"+str(port))
        msg += "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
        msg += "finish_time:"
        msg += final_time
        msg += "\n"
        msg += "miner:"
        msg += miner
        msg += "\n"
        msg += "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
        
        f.write(msg)
        f.close()

    def write_log(self,port = 0,debug = "writelog"): 
        """
        for _ in Node().port_list:
            if port == _:
                f = open("blockchain"+str(port % 5000)+".log",'w')
        """
        if port == 5000:
            f = open("blockchain.log",'w')
        elif port == 5001:
            f = open("blockchain2.log",'w')
        elif port == 5002:
            f = open("blockchain3.log",'w')
        elif port == 5003:
            f = open("blockchain4.log",'w')
        elif port == 5004:
            f = open("blockchain5.log",'w')
        

        msg = str()
        for _ in self.chain:
            msg += _.print_block("write_log port:"+str(port))
        
        f.write(msg)
        f.close()

    def getCPU(self):
        f = open("blockchain_2_cpu.log","w")
        msg = str(os.popen("top -n | awk '/Cpu\(s\):/ {print $2}'").readline().strip())
        f.write(msg)
        f.close
        return (str(os.popen("top -n | awk '/Cpu\(s\):/ {print $2}'").readline().strip()))

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
