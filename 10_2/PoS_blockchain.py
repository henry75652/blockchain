from node import Node
from blockchain import Blockchain
from block import Block
from appendix import commitment_cal
import time
import threading
import ECC
import test_ECC
import appendix
import zero_knowledge_change
from PoS import calculate
import random

#global variable
STOP = int()    # 0 run, 1 stop
node = Node()
blockchain = Blockchain()
ECC_1 = ECC.Ecc()
ECC_2 = test_ECC.Ecc()
Calculate = calculate()
#GO_FUCK = appendix.go_fuck_yourself()
count = 0

def init():
    #init

    t = threading.Thread(target = retriever,args = (node,))
    t.start()

    t = threading.Thread(target = miner,args = (blockchain,))
    #if node.server_port == 5000:t.start()
    t.start()
    
    #portlist = [5000, 5001, 5002, 5003] ##
    
    for _ in node.port_list:
        if node.server_port == _:
            for i in node.port_list:
                if i != _:
                    port = i
                    #print("[main.py]",port,_)
                    node.client_init(port)
        else:
            print("[main.init]unknown error!")

"""
    if node.server_port == 5000:
        for _ in portlist:
            if _ != 5000:
                port = _
                node.client_init(port)
    elif node.server_port == 5001:
        for _ in portlist:
            if _ != 5001:
                port = _
                node.client_init(port)
    elif node.server_port == 5002:
        for _ in portlist:
            if _ != 5002:
                port = _
                node.client_init(port)
    elif node.server_port == 5003:
        for _ in portlist:
            if _ != 5003:
                port = _
                node.client_init(port)
    else:
        print("[main.init]unknown error!")
"""

def miner(blockchain):
    while STOP == 0:
        while len(blockchain.blockqueue) >= 1:
            block = blockchain.mine()
            timestamp = round(time.time(),2)
            Calculate.calculate_num(True ,True ,True ,True ,False ,node.server_port)
            Calculate.calculate_num(True ,True ,True ,False ,True ,node.server_port)
            if block == False:  #代表有人先挖到 有更新
                break
            block.print_block("[main.miner]I mined a block")
            blockchain.write_log_check(port = node.server_port,final_time = str(timestamp),miner = node.node_list[node.server_port % 5000])
            
            """
            puzzle, presets = zero_knowledge_change.gen_sudoku_puzzle()
            solution = zero_knowledge_change.solve_sudoku_puzzle(puzzle)

            permutations = zero_knowledge_change.create_permutations()
            permuted_solution = zero_knowledge_change.puzzle_permute(solution, permutations)
            nonces = zero_knowledge_change.gen_nonces()
            commitment = zero_knowledge_change.puzzle_commitment(permuted_solution, nonces)

            sender_solution = []
            sender_solution_nonce = []
            sender_solution_commitment = []
            
            random_nonce = block.nonce
            
            if block.nonce % 2 == 0:
                for a in range(len(str(block.nonce))):
                    if random_nonce % 10 != 9:
                        sender_solution_column = zero_knowledge_change.puzzle_columns(permuted_solution)[random_nonce % 10]
                        sender_solution.append(sender_solution_column)
                        sender_solution_nonce_column = zero_knowledge_change.puzzle_columns(nonces)[random_nonce % 10]
                        sender_solution_nonce.append(sender_solution_nonce_column)
                        sender_solution_commitment_column = zero_knowledge_change.puzzle_columns(commitment)[random_nonce % 10]
                        sender_solution_commitment.append(sender_solution_commitment_column)
                    else:
                        sender_solution_column = zero_knowledge_change.puzzle_columns(permuted_solution)[0]
                        sender_solution.append(sender_solution_column)
                        sender_solution_nonce_column = zero_knowledge_change.puzzle_columns(nonces)[0]
                        sender_solution_nonce.append(sender_solution_nonce_column)
                        sender_solution_commitment_column = zero_knowledge_change.puzzle_columns(commitment)[0]
                        sender_solution_commitment.append(sender_solution_commitment_column)
                    random_nonce = random_nonce // 10
            else:
                for a in range(len(str(block.nonce))):
                    if random_nonce % 10 != 9:
                        sender_solution_row = zero_knowledge_change.puzzle_rows(permuted_solution)[random_nonce % 10]
                        sender_solution.append(sender_solution_row)
                        sender_solution_nonce_row = zero_knowledge_change.puzzle_rows(nonces)[random_nonce % 10]
                        sender_solution_nonce.append(sender_solution_nonce_row)
                        sender_solution_commitment_row = zero_knowledge_change.puzzle_rows(commitment)[random_nonce % 10]
                        sender_solution_commitment.append(sender_solution_commitment_row)
                    else:
                        sender_solution_row = zero_knowledge_change.puzzle_rows(permuted_solution)[0]
                        sender_solution.append(sender_solution_row)
                        sender_solution_nonce_row = zero_knowledge_change.puzzle_rows(nonces)[0]
                        sender_solution_nonce.append(sender_solution_nonce_row)
                        sender_solution_commitment_row = zero_knowledge_change.puzzle_rows(commitment)[0]
                        sender_solution_commitment.append(sender_solution_commitment_row)
                    random_nonce = random_nonce // 10
            """
            concent = "update||"+block.conv_block_to_str(0,0)+"||appendix||verification: "+ECC_1.sign_ECDSA_msg(block.get_blockhash()).decode()+"\\miner: "+str(node.server_port)+"\\finish_time: "+str(timestamp)
            """
            concent = "update||"+block.conv_block_to_str(0,0)+"||appendix||verification: "+ECC_1.sign_ECDSA_msg(block.get_blockhash()).decode()+"\\miner: "+str(node.server_port)+"\\commitment:["
            for a in range(len(sender_solution)):
                concent = concent + commitment_cal(sender_solution[a]).to_string()
            for a in range(len(sender_solution_nonce)):
                concent = concent + commitment_cal(sender_solution_nonce[a]).to_string()
            for a in range(len(sender_solution_commitment)):
                concent = concent + commitment_cal(sender_solution_commitment[a]).to_string()
            concent = concent +"]"
            """
            #print("[concent]",concent)
            node.broadcast(concent)
            #node.broadcast("update//"+block.conv_block_to_str(0)+"//appendix//"+ECC_1.sign_ECDSA_msg(block.get_blockhash()).decode('utf-8')+"//this is mined by node//"+str(node.server_port)+" "+str(node.server_ip))
            #node.broadcast("update||"+block.conv_block_to_str(0)+"||appendix||"+ECC_1.sign_ECDSA_msg(block.get_blockhash()).decode())
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
            #print("[retriever_main.py]",data["msg"]["tag"])
            if data["msg"]["tag"] == "block":
                print("[retriever]:data is block type")
                if data["msg"]["content"] == "FAKE":
                    Calculate.calculate_num(True ,False ,True ,False ,False ,data["msg"]["Appendix"])
                    print("[test_fake_pos_block]",Calculate.get_pos()[data["msg"]["Appendix"] % 5000])
                else:
                    print("[block_in]")
                    data["msg"]["content"].print_block("call by block")
                    ver_block_hash = (data["msg"]["appendix"]).encode()
                    compar_block_hash = data["msg"]["content"].get_blockhash()
                    if ECC_1.validate_signature(ver_block_hash,compar_block_hash):
                        print("[ecc_in_block]")
                        if data["msg"]["content"].info.pos_miner == (str(node.server_ip)+" "+str(node.server_port)):
                            blockchain.append_blockqueue(data["msg"]["content"])
                    else:
                        print("not pass verification_block")
                        for i in range(len(node.node_list)):
                            if data["msg"]["content"].source == node.node_list[i]:
                                node_port = node.port_list[i]
                                print("[retriever_main.py]",node_port)
                                break
                        Calculate.calculate_num(True ,True ,False ,False ,False ,node_port)
            
            elif data["msg"]["tag"] == "cmd":
                print("[retriever]:data is string type")
                print("[retriever]",data["msg"]["content"])
            
            elif data["msg"]["tag"] == "update":
                #print("[retriever]:data is for updating blockchain",blockchain)
                if data["msg"]["content"] == "FAKE":
                    Calculate.calculate_num(True ,False ,True ,False ,False ,data["msg"]["Appendix"])
                    print("[test_fake_pos_update]",Calculate.get_pos()[data["msg"]["Appendix"] % 5000])
                    #for i in range(len(blockchain.chain)):
                        #print("(debug)[main.new_block]2   ",blockchain.chain[i].pos_trust,"type = ",type(blockchain.chain[i].pos_trust),"addr = ",hex(id(blockchain.chain[i].pos_trust)))
                else:
                    print("[update_in]")
                    Calculate.calculate_num(True ,"True" ,True ,False ,False ,int(appendix.miner(data["msg"]["appendix"])))
                    data["msg"]["content"].print_block("call by update")
                    #ver_blockchain_hash = (data["msg"]["appendix"]).encode()
                    ver_blockchain_hash = (appendix.verification(data["msg"]["appendix"])).encode()
                    compar_blockchain_hash = data["msg"]["content"].get_blockhash()
                    if ECC_1.validate_signature(ver_blockchain_hash,compar_blockchain_hash):
                        #print("[go_fuck is]:",go_fuck_yourself().go_fuck(data["msg"]["appendix"]))
                        Calculate.calculate_num(True ,True ,"True" ,False ,False ,int(appendix.miner(data["msg"]["appendix"])))
                        print("[ecc_in_update]")
                        """
                        for a in range(len(str(data["msg"]["content"].nonce))):    ###====###零知識
                            sudoku_verification = zero_knowledge_change.all_digits_exist_once(commitment_cal().sequence(data["msg"]["appendix"])[a])
                            assert sudoku_verification == True
                            receiver_verification_commitment = zero_knowledge_change.puzzle_commitment(commitment_cal().sequence(data["msg"]["appendix"])[a], commitment_cal().sequence(data["msg"]["appendix"])[a + len(str(data["msg"]["content"].nonce))])
                            for b in range(9):
                                if commitment_cal().sequence(data["msg"]["appendix"])[a + 2 * len(str(data["msg"]["content"].nonce))][b] != receiver_verification_commitment[b]:
                                    raise AssertionError
                                else:
                                    pass                      ###====###零知識
                        """
                        Calculate.calculate_num(True ,True ,True ,True ,False ,int(appendix.miner(data["msg"]["appendix"])))
                        for i in range(len(node.node_list)):
                            if data["msg"]["content"].source == node.node_list[i]:
                                node_port = node.port_list[i]
                                break
                        Calculate.calculate_num(True ,True ,True ,False ,True ,node_port)
                        #Calculate.list_pos_trust = data["msg"]["content"].pos_trust
                        blockchain.update_blockchain(data["msg"]["content"])
                        blockchain.write_log_check(port = node.server_port,final_time = appendix.finish_time(data["msg"]["appendix"]),miner = node.node_list[int(appendix.miner(data["msg"]["appendix"])) % 5000])
                    else:
                        print("not pass verification_update")
                        for i in range(len(node.node_list)):
                            if data["msg"]["content"].source == node.node_list[i]:
                                node_port = node.port_list[i]
                                print("[retriever_main.py]",node_port)
                                break
                        Calculate.calculate_num(True, True, False ,False ,False ,node_port)
                
            elif data["msg"]["tag"] == "stop":
                print("[retriever]:data is stop cmd")
                print("[retriever]",data["msg"]["content"])
                ip_port = node.server_ip+" "+str(node.server_port)
                print("test",ip_port)
                if data["msg"]["content"] == ip_port:
                    print("in")
                    STOP = 1
                    node.stop()
                    blockchain.blockchain_stop()
                    
            """
            elif data["msg"]["tag"] == "stop_mine":
            blockchain.blockchain_stop()
            """
                    
            """
            elif block.id % 20 == 0:
                node.broadcast("stop_mine")
                node.broadcast("chande_ledger")
            """
            """
            elif data["msg"]["tag"] == "chande_ledger":
                node.broadcast(blockchain.chain)
                blockchain = self.chain
            """

            #print("[go_fuck is]:",go_fuck_yourself().go_fuck(data["msg"]["appendix"]))
        else:
            print("[retriever]:data is not type dict")
        pass

def new_block():
    #info = input("new block:")
    global info ##
    info = info + 1 ##
    info_str = "test {info} port {port}".format(info = info,port = node.server_port) ##7/6
    temp_pos = [0 for i in range(len(Calculate.get_pos()))]

    for i in range(len(Calculate.get_pos())):
        temp_pos[i] = Calculate.get_pos()[i]

    
    #print("[test_pos_trust_main.py]",Calculate.pos_trust_list)
    if blockchain.chain[-1].info.pos == 1:
        List = node.node_list
        turst = random.choices(List, weights=(Calculate.get_pos()[0], Calculate.get_pos()[1], Calculate.get_pos()[2], Calculate.get_pos()[3]), k=1)
        block = Block(info_str,Calculate.get_pos(),node.server_ip+" "+str(node.server_port),turst[0])
    else:
        block = Block(info_str,Calculate.get_pos(),node.server_ip+" "+str(node.server_port))
    #print("(debug)[main.new_block]1   ",temp_pos,"type = ",type(temp_pos),"addr = ",hex(id(temp_pos)))
    #for i in range(len(blockchain.chain)):
    #    print("(debug)[main.new_block]2   ",blockchain.chain[i].info.pos_trust,"type = ",type(blockchain.chain[i].info.pos_trust),"addr = ",hex(id(blockchain.chain[i].info.pos_trust)))
    #block.id = len(blockchain.chain)
    node.broadcast("block||"+block.conv_block_to_str(0,0)+"||appendix||"+ECC_1.sign_ECDSA_msg(block.get_blockhash()).decode())
    #node.broadcast("block//"+block.conv_block_to_str(0)+"//appendix//"+ECC_1.sign_ECDSA_msg(block.get_blockhash()))
    #node.broadcast("block//"+block.conv_block_to_str(0)+"//appendix//test")
    #blockchain.update_blockqueue(block) ## 6.27
    blockchain.append_blockqueue(block)
    
def fake_aes_new_block():
    global fake_info ##
    info = fake_info + 1 ##
    info_str = "test {info} port {port}".format(info = info,port = node.server_port) ##7/6
    block = Block(info_str,Calculate.get_pos(),node.server_ip+" "+str(node.server_port))
    node.broadcast("block||"+block.conv_block_to_str(0,1)+"||appendix||"+ECC_1.sign_ECDSA_msg(block.get_blockhash()).decode())
    blockchain.append_blockqueue(block)
    
def fake_ecc_new_block():
    global fake_info ##
    info = fake_info + 1 ##
    info_str = "test {info} port {port}".format(info = info,port = node.server_port) ##7/6
    block = Block(info_str,Calculate.get_pos(),node.server_ip+" "+str(node.server_port))
    node.broadcast("block||"+block.conv_block_to_str(0,0)+"||appendix||"+ECC_2.sign_ECDSA_msg(block.get_blockhash()).decode())
    blockchain.append_blockqueue(block)

def terminal_stop():
    info = input("stop node ip_port:")
    node.broadcast("stop||"+info+"||appendix||this is from node||"+str(node.server_port)+" "+str(node.server_ip))

if __name__ == "__main__":
    init()
    
    #flag
    STOP = 0

    #nodelist = ['172.30.4.219 5000', '172.30.4.219 5001', '172.30.4.219 5002', '172.30.4.219 5003'] ##
    info = 20000000 ##
    fake_info = 33333332 ##

    #run
    blockchain.run(node.server_port)
    while STOP == 0:
        
        if (str(node.server_ip)+" "+str(node.server_port)) == node.node_list[0]: ##
            #print("[in_1]")
            time.sleep(5)
            msg = "new block"
            #msg = input()
            #node.broadcast(msg)
        elif (str(node.server_ip)+" "+str(node.server_port)) == node.node_list[1]:
            #print("[in_2]")
            time.sleep(7)
            msg = "new block"
            #msg = " "
            #msg = input()
            #node.broadcast(msg)
        elif (str(node.server_ip)+" "+str(node.server_port)) == node.node_list[2]:
            #print("[in_3]")
            time.sleep(9)
            msg = "new block"
            #msg = " "
            #msg = input()
        elif (str(node.server_ip)+" "+str(node.server_port)) == node.node_list[3]:
            #print("[in_4]")
            time.sleep(10)
            msg = "new block"
            #msg = " "
            #msg = input()

            #print("[test_main.py]",str(node.server_ip)+" "+str(node.server_port),node.node_list[0])
            #node.broadcast(msg)  ##
        #msg = "hello"
        #node.broadcast(msg)
        
        blockchain.write_log(port = node.server_port) ##

        if msg == 'exit':
            break
        if msg == "show blockchain":
            #blockchain.print_blockchain()
            blockchain.write_log(port = node.server_port)
            print("[pos_main,py]",Calculate.get_pos())
            print("[pos_list_main,py]",Calculate.list_pos_trust)
            #for i in range(len(blockchain.chain)):
                #print("pos_test",blockchain.chain[i].info.data)
        if msg == "show blockqueue":
            print(blockchain.blockqueue)
        if msg == "show block":
            if len(blockchain.blockqueue) >= 1:
                blockchain.blockqueue[int(input("input index:"))].print_block()
            else: print("[main]there is not anything in blockqueue!")
        if msg == "new block":
            block = new_block()
        if msg == "fake aes":
            block = fake_aes_new_block()
        if msg == "fake ecc":
            block = fake_ecc_new_block()
        if msg == "stop":
            terminal_stop()
        if msg == "show serverlist":
            print("[main]show serverlist:",node.server_list_client)
        if msg == "show clientlist":
            print("[main]show clientlist:",node.client_list_server)
        if msg == "pause":
            #print("(debuf)[block.Indormation.__init__ = ",pos_trust," addr = ",hex(id(pos_trust)))
            while(1): pass

    blockchain.blockchain_stop()

    time.sleep(1)
    node.stop()
    STOP = 1
