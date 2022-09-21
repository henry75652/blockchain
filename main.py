from node import Node
from blockchain import Blockchain
from block import Block
from appendix import go_fuck_yourself
import time
import threading
import ECC
import appendix
import zero_knowledge_change

#global variable
STOP = int()    # 0 run, 1 stop
node = Node()
blockchain = Blockchain()
ECC_1 = ECC.Ecc()
#GO_FUCK = appendix.go_fuck_yourself()
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
    
    for _ in node.port_list:
        if node.server_port == _:
            for i in node.port_list:
                if i != _:
                    port = i
                    node.client_init(port)
        else:
            print("[main.init]unknown error!")

def miner(blockchain):
    while STOP == 0:
        while len(blockchain.blockqueue) >= 1:
            block = blockchain.mine()
            if block == False:  #代表有人先挖到 有更新
                break
            block.print_block("[main.miner]I mined a block")
            
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
                    
            concent = "update||"+block.conv_block_to_str(0)+"||appendix||verification: "+ECC_1.sign_ECDSA_msg(block.get_blockhash()).decode()+"\\fuck:["
            for a in range(len(sender_solution)):
                concent = concent + go_fuck_yourself(sender_solution[a]).to_string()
            for a in range(len(sender_solution_nonce)):
                concent = concent + go_fuck_yourself(sender_solution_nonce[a]).to_string()
            for a in range(len(sender_solution_commitment)):
                concent = concent + go_fuck_yourself(sender_solution_commitment[a]).to_string()
            concent = concent +"]"
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
                if ECC_1.validate_signature(ver_blockchain_hash,compar_blockchain_hash):
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
                    if blockchain.verify_change(data["msg"]["content"],count):
                        blockchain.update_blockchain(data["msg"]["content"])
                        count += 1
                        print("[inn]")
                        #寫交換條件在這裡
                    """
                else:
                    print("not pass verification")
                    
                #count += 1
                
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
    block = Block(info_str,node.server_ip+":"+str(node.server_port))
    #block.id = len(blockchain.chain)
    node.broadcast("block||"+block.conv_block_to_str(0)+"||appendix||"+ECC_1.sign_ECDSA_msg(block.get_blockhash()).decode())
    #node.broadcast("block//"+block.conv_block_to_str(0)+"//appendix//"+ECC_1.sign_ECDSA_msg(block.get_blockhash()))
    #node.broadcast("block//"+block.conv_block_to_str(0)+"//appendix//test")
    #blockchain.update_blockqueue(block) ## 6.27
    blockchain.append_blockqueue(block)

def terminal_stop():
    info = input("stop node ip_port:")
    node.broadcast("stop||"+info+"||appendix||this is from node||"+str(node.server_port)+" "+str(node.server_ip))

if __name__ == "__main__":
    init()
    
    #flag
    STOP = 0

    info = 20000000 ##

    #run
    blockchain.run(node.server_port)
    while STOP == 0:
        
        if (str(node.server_ip)+" "+str(node.server_port)) == node.node_list[0]: ##
            time.sleep(7)
            #msg = "new block"
            msg = input()
            #node.broadcast(msg)
        elif (str(node.server_ip)+" "+str(node.server_port)) == node.node_list[1]:
            time.sleep(11)
            #msg = "new block"
            #msg = " "
            msg = input()
            #node.broadcast(msg)
        elif (str(node.server_ip)+" "+str(node.server_port)) == node.node_list[2]:
            print("in")
            time.sleep(17)
            #msg = " "
            msg = input()
        elif (str(node.server_ip)+" "+str(node.server_port)) == node.node_list[3]:
            time.sleep(25)
            #msg = "new block"
            #msg = " "
            msg = input()
            #node.broadcast(msg)  ##

        #node.broadcast(msg)
        
        blockchain.write_log(port = node.server_port) ##

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
