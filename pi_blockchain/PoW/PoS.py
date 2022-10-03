import random

class calculate():
    def __init__(self,list_pos_trust = [100,100]):
        self.list_pos_trust = list_pos_trust
        #self.node = Node()
        
    def get_pos(self):
        pos_num = list()
        for i in range(len(self.list_pos_trust)):
            pos_num.append(self.list_pos_trust[i])
        return pos_num
    
    def calculate_num(self,NODE ,AES ,ECC ,MINE ,DEDICATE ,port):
        if NODE == False:
            self.list_pos_trust[port % 5000] -= 26
        elif AES == False:
            self.list_pos_trust[port % 5000] -= 16
        elif AES == "True":
            self.list_pos_trust[port % 5000] += 1
            """
            block_test = Block().information.pos_trust[port % 5000] / 1.5
            print("[test_aes]",block_test)
            """
        elif ECC == False:
            self.list_pos_trust[port % 5000] -=18
        elif ECC == "True":
            self.list_pos_trust[port % 5000] += 1
        #print("loc_port",port)
        #print("loc_port_5000",port % 5000)
        #elif ECC == False:
            #self.list_pos_trust[port % 5000] +=5
        elif MINE == True:
            self.list_pos_trust[port % 5000] += 9
            #print("[test_pos.py]")
        elif DEDICATE == True:
            self.list_pos_trust[port % 5000] += 2
            
        print("[PoS.py]loc_pos",self.list_pos_trust)
        return self
    """
    def POS(self,block):
        List = [block.number_1, block.number_2, block.number_3, block.number_4]
        mine_node = random.choices(List, weights=(block.PoS_num_1, block.PoS_num_2, block.PoS_num_3 , block.PoS_num_4), k=4)
        return mine_node
    """
    
if __name__ == "__main__":
    
    stop = 1

