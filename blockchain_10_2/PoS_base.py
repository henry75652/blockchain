###信任機制

##### """是幫你標出那個function 至於要怎麼改信任機制進去，你要自己加，再去debug 

# block.py
## 信任值的初始值 --> 100
## 信任值格式 --> id\timestamp\nonce\prev_hash\information\source\credence(信任值)

# block.py
## 信任值計算 
### AES解密錯誤 ==> 信任值 = credence / 1.5
""" #####自己去對名稱找
    def conv_str_to_block(self,sData):  #return 
        try:
            pass
            list_block = sData.split('\n')  #['Tue Dec 14 00:21:29 2021\\hello\\0\\0\\172.30.5.59:5000', '']
            list_block = list_block[0]          #  id    timestamp                   nonce  prev_hash                                                           information source
            list_block = list_block.split('\\') #['56', 'Mon Feb 21 14:42:57 2022', '178', '00079bcd42436498efda60b225436ec25c8db797be85775b0271bbba4a776ddf', 'Hello', '0.0.0.0']

            self.id = int(list_block[0])
            self.timestamp = float(list_block[1])
            self.nonce = int(list_block[2])
            self.prev_hash = str(list_block[3])
            #self.information = Information(list_block[4])
            self.information = Information(self.AES1.decrypt(list_block[4]))   ####解密在這邊
            self.source = str(list_block[5])
            return self
        except:
            pass
            return False
"""

# main.py
## 信任值計算 
### 是否在白名單中(否) ==> 信任值 = credence - 13
"""
if __name__ == "__main__":
    init()
    
    #flag
    STOP = 0

    nodelist = ['172.30.1.128 5000', '172.30.1.128 5001', '172.30.1.128 5002', '172.30.1.128 5003'] ####白名單
    info = 20000000 ##

    #run
    blockchain.run(node.server_port)
    while STOP == 0:
        
        if (str(node.server_ip)+" "+str(node.server_port)) == nodelist[0]: ##
            time.sleep(7)
            msg = "new block"
        elif (str(node.server_ip)+" "+str(node.server_port)) == nodelist[1]:
            time.sleep(11)
            msg = "new block"
        elif (str(node.server_ip)+" "+str(node.server_port)) == nodelist[2]:
            time.sleep(17)
            msg = input()
        elif (str(node.server_ip)+" "+str(node.server_port)) == nodelist[3]:
            time.sleep(25)
            msg = "new block"
"""

# blockchain.py
## 信任值計算 
### 資料驗證正確(錯) ==> 信任值 = credence - 26
""" ##### 驗證機制待改善
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

# main.py
## 信任值計算 
### 金鑰錯誤(ECC) ==> 信任值 = credence / 1.3
"""
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
                ver_block_hash = (data["msg"]["appendix"]).encode()
                compar_block_hash = data["msg"]["content"].get_blockhash()
                if ECC_1.validate_signature(ver_block_hash,compar_block_hash):
                    blockchain.append_blockqueue(data["msg"]["content"])
                else:
                    print("not pass verification")
            
            elif data["msg"]["tag"] == "cmd":
                print("[retriever]:data is string type")
                print("[retriever]",data["msg"]["content"])
            
            elif data["msg"]["tag"] == "update":
                print("[retriever]:data is for updating blockchain",blockchain)
                data["msg"]["content"].print_block("call by update")
                #ver_blockchain_hash = (data["msg"]["appendix"]).encode()
                ver_blockchain_hash = (appendix.verification(data["msg"]["appendix"])).encode()
                compar_blockchain_hash = data["msg"]["content"].get_blockhash()
                if ECC_1.validate_signature(ver_blockchain_hash,compar_blockchain_hash):       #### 這邊，這裡其實滿複雜的
                    #print("[go_fuck is]:",go_fuck_yourself().go_fuck(data["msg"]["appendix"]))
                    if data["msg"]["content"].nonce % 2 == 0: ###====###零知識
                        for a in range(len(str(data["msg"]["content"].nonce))):
                            sudoku_verification = zero_knowledge_change.all_digits_exist_once(go_fuck_yourself().go_fuck(data["msg"]["appendix"])[a])
                            assert sudoku_verification == True
                            receiver_verification_commitment = zero_knowledge_change.puzzle_commitment(go_fuck_yourself().go_fuck(data["msg"]["appendix"])[a], go_fuck_yourself().go_fuck(data["msg"]["appendix"])[a + len(str(data["msg"]["content"].nonce))])
                            for b in range(9):
                                if go_fuck_yourself().go_fuck(data["msg"]["appendix"])[a + 2 * len(str(data["msg"]["content"].nonce))][b] != receiver_verification_commitment[b]:
                                    raise AssertionError
                                else:
                                    pass                      ###====###零知識
                        blockchain.update_blockchain(data["msg"]["content"])
"""

# blockchain.py
## 信任值計算 
### 出塊效率過低 ==> 信任值 = credence - 3
##### 帶禾琴完成這邊驗證機制

#####總結

# 目前機制 PoW + 零知識
# 難度 PoW -> 3 ； 零知識 -> 迴圈一次
## 信任值參與
### 50< credence <= 75 ----> PoW -> 4 ； 零知識 -> 迴圈一次
### 25< credence <= 50 ----> PoW -> 5 ； 零知識 -> 迴圈三次
### 0< credence <= 25 ----> PoW -> 6 ； 零知識 -> 迴圈五次
### credence <= 0 ----> 移除任務參與
#### credence 負之後直接移除此節點，因為負號不好爬字，寫入帳本很麻煩

#  id    timestamp                   nonce  prev_hash                                                           information source       mark_1_trust    mark_2_trust    mark_3_trust      mark_4_trust PoS       mine
#[ '56', 'Mon Feb 21 14:42:57 2022', '178', '00079bcd42436498efda60b225436ec25c8db797be85775b0271bbba4a776ddf', 'Hello',    '0.0.0.0',   '100',          '90',           '80',            '70',         '1 or 0', '1~4']

