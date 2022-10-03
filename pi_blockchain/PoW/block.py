import hashlib
import time
import AES_en
import fake_AES_en
from appendix import commitment_cal

class Information():
    def __init__(self,data = 'Hello',pos_trust = [100,100],pos_miner = 'random'):
        self.data = data
        #print("(debuf)[block.Indormation.__init__ = ",pos_trust," addr = ",hex(id(pos_trust)))
        #self.pos_trust = [100,100,100,100]  #改！！！！
        self.pos_trust = pos_trust
        self.pos = 0
        self.pos_miner = pos_miner

    def get(self):
        return self.data
        
    def duplication(self):
        information = Information()
        information.data = self.data
        information.pos_trust = self.pos_trust
        #print("type",type(information.pos_trust),"addr",)
        information.pos = self.pos
        information.pos_miner = self.pos_miner
        return information

class Block():
    def __init__(self,information = "",pos_trust = [],server_ip_port = "",pos_miner = 'random',id = 0):
        self.id = int(0)
        #self.timestamp = time.ctime(time.time())
        self.timestamp = round(time.time(),2)    #float #6.27
        #if information == 'this is genesis block': #6.27
        #    self.timestamp = '000 000 00 00 00' 
        #else:
        #    self.timestamp = time.ctime(time.time())
        self.nonce = int(0)
        self.prev_hash = '0'
        self.info = Information(information,pos_trust,pos_miner)
        #self.pos_trust = pos_trust
        #self.information.pos_trust = pos_trust
        self.source = str(server_ip_port)
        self.en_flag = 1
        self.fake_flag = 1
        secretkey = ['6agrioBE1D9yoGOX4yyDMyMFs72jYvJ8', '6agru3BE1D9yoGOX4u3DMyMFs72jYvJ8'] ##
        self.AES0 = AES_en.AESCipher(secretkey[0])        ##
        self.AES1 = fake_AES_en.AESCipher(secretkey[1])        ##
        self.list_info = str()
        # id\timestamp\nonce\prev_hash\information\source
        self.attritube = ["id","timestamp","nonce","prev_hash","information.data","source"]

    def conv_block_to_str(self,en_flag,fake_flag):
        str_block = str()
        #inf = str(self.information.data)
        if en_flag == 0:
            if fake_flag == 0:
                str_block += str(self.id) \
                    + "\\" + str(self.timestamp) \
                    + "\\" + str(self.nonce) \
                    + "\\" + str(self.prev_hash) \
                    + "\\" + self.AES0.encrypt(str(self.info.data) + "//" + str(self.info.pos_trust) + "//" + str(self.info.pos) + "//" + str(self.info.pos_miner)) \
                    + "\\" + str(self.source) \
                        
            else:
                str_block += str(self.id) \
                    + "\\" + str(self.timestamp) \
                    + "\\" + str(self.nonce) \
                    + "\\" + str(self.prev_hash) \
                    + "\\" + self.AES1.encrypt(str(self.info.data) + "//" + str(self.info.pos_trust) + "//" + str(self.info.pos) + "//" + str(self.info.pos_miner)) \
                    + "\\" + str(self.source) \
                #print("[before_send_en]",self.AES1.encrypt(str(self.information.data)),"\n")
        elif en_flag == 1:
            str_block += str(self.id) \
                + "\\" + str(self.timestamp) \
                + "\\" + str(self.nonce) \
                + "\\" + str(self.prev_hash) \
                + "\\" + str(self.info.data) + "//" + str(self.info.pos_trust) + "//" + str(self.info.pos) + "//" + str(self.info.pos_miner) \
                + "\\" + str(self.source) \
                #print("[own_no_en]",str(self.information.data),"\n")
        return str_block

    def conv_str_to_block(self,sData):  #return 
        # 56\Mon Feb 21 14:29:13 2022\177\00079bcd42436498efda60b225436ec25c8db797be85775b0271bbba4a776ddf\Hello\0.0.0.0
        list_block = sData.split('\n')  #['Tue Dec 14 00:21:29 2021\\hello\\0\\0\\172.30.5.59:5000', '']
        #print("[conv_str_to_block]\nsData\n",sData,"\nlist_block\n",list_block)
        list_block = list_block[0]          #  id    timestamp                   nonce  prev_hash                                                           information source
        list_block = list_block.split('\\') #['56', 'Mon Feb 21 14:42:57 2022', '178', '00079bcd42436498efda60b225436ec25c8db797be85775b0271bbba4a776ddf', 'Hello', '0.0.0.0']

        self.id = int(list_block[0])
        self.timestamp = float(list_block[1])
        self.nonce = int(list_block[2])
        self.prev_hash = str(list_block[3])
        #if self.test_flag == 1:
            #print("[after_rec_en]",list_block[4],"\n")
            #self.test_flag = 1
        #self.information = Information(list_block[4])
        self.source = str(list_block[5])
        #print("[test2_block.py]",self.source)
        try:
            self.list_info = self.AES0.decrypt(list_block[4])
            #print("[test_block.py]",self.list_info)
        #if self.list_info == "":
            #print("[conv_str_to_block]unknown error!")
            #return False
        except:
            #print("test_block.py_fake")
            return {"msg":{"Tag":"Fake","Content":self.source}}
        list_info_total = self.list_info.split('//')
        self.info.data = list_info_total[0]
        self.info.pos_trust = commitment_cal().sequence_info(list_info_total[1])
        #print("test_block.py_pass_2")
        self.info.pos = int(list_info_total[2])
        self.info.pos_miner = str(list_info_total[3])
        #self.information = Information(self.AES0.decrypt(list_block[4]))
        
        #if self.test_flag == 1:
            #print("[after_rec_de]",self.AES1.decrypt(list_block[4]),"\n")
            #self.test_flag = 0
        #print("[after_send_en]",self.AES1.decrypt(Information(list_block[4])),"\n")
        return self

    def is_same_as(self,block):
        result = self.cmp(block)
        if "timestamp" in result and "information.data" and "source" in result:
            #print("[block.is_same_as]True")
            return True
        else:
            #print("[block.is_same_as]False")
            return False
    
    def cmp(self,block):    #return list ex. ["id","timestamp"]
        pass
        result = []
        if self.id == block.id:
            result.append("id")
        #print("[block.cmp]two timestamp = ",self.timestamp,block.timestamp)
        if float(self.timestamp) == float(block.timestamp):
            result.append("timestamp")
        if self.nonce == block.nonce:
            result.append("nonce")
        if self.prev_hash == block.prev_hash:
            result.append("prev_hash")
        if self.info.data == block.info.data:
            result.append("information.data")
        if self.source == block.source:
            result.append("source")
        #print("[cmp]result = ",result)
        return result

    def duplication(self):
        block = Block()
        block.id = self.id
        block.timestamp = self.timestamp
        block.nonce = self.nonce
        block.info = self.info.duplication()
        block.source = self.source
        #block.pos_trust = self.pos_trust
        return block

    def get_blockhash(self):
        new_block = self.duplication()
        new_block.id = 0
        return hashlib.sha256(new_block.conv_block_to_str(1,0).encode()).hexdigest()

    def is_same_as__(self,block):
        pass
        if self.id == block.id and self.timestamp == block.timestamp and self.source == block.source:
            #print("[block.is_same_as]True")
            return True
        else: 
            #print("[block.is_same_as]False")
            return False

    def print_block(self,debug = ""):
    
        # id\timestamp\nonce\prev_hash\information\source
        msg = str()
        msg += "====block===="+str("debug:" * (not(len(debug) == 0)))+str(debug)+   \
            "\nid:"+str(self.id)+   \
            "\ntimestamp:"+str(self.timestamp)+ \
            "\nnonce:"+str(self.nonce)+ \
            "\nprev_hash:"+str(self.prev_hash)+ \
            "\ninformation.data:"+str(self.info.data)+   \
            "\n           .pos_trust:"+str(self.info.pos_trust)+   \
            "\n           .pos:"+str(self.info.pos)+   \
            "\n           .pos_mine:"+str(self.info.pos_miner)+   \
            "\nsource:"+str(self.source)+   \
            "\n============="+  \
            "\nhash:"+str(self.get_blockhash())+    \
            "\n=============\n"
        print("[msg]\n",msg,"sep\n",sep = "",end = "")
        
        return msg

            


if __name__ == "__main__":
    pass
