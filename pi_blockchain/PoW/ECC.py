import base64
import ecdsa
    
class Ecc(object):
   def __init__(self):
        
        pri_path = ['privkey_ECC_4.txt']
        self.public_key_path = ['pubkey_ECC_1.txt','pubkey_ECC_2.txt','pubkey_ECC_3.txt','pubkey_ECC_4.txt']
        self.privaue_key_path = pri_path[0]

   def sign_ECDSA_msg(self,msg_hash): #簽章
       
       with open(self.privaue_key_path,mode='r') as f:
             private_key = f.read()
             f.close()
         #message = '我是真心喜歡你的。skjbkj'
       byte_msg_hash = msg_hash.encode()
       sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)
       signature = base64.b64encode(sk.sign(byte_msg_hash))
       #print("test_1",type(signature))
       #print("test_1_1",signature)
       #signature = base64.b64decode(signature)
       #print("test_2",type(signature))
       #print("test_2_1",signature)
       return signature
         #return signature, msg_hash

   def validate_signature(self,signature, msg_hash):
       
        #signature = signature.encode('utf-8')
        #signature = base64.b64decode(signature.encode('utf-8')+ b'=' * (-len(signature) % 4)) ####改，不然會出事
        signature = base64.b64decode(signature + b'=' * (-len(signature) % 4)) ####改，不然會出事
        for a in range(len(self.public_key_path)):
            #print(a)
            with open(self.public_key_path[a],mode='r') as f:
                public_key = f.read()
                f.close()
            public_key = (base64.b64decode(public_key)).hex()
            vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key), curve=ecdsa.SECP256k1)
            # Try changing into an if/else statement as except is too broad.
            try:
                vk.verify(signature, msg_hash.encode())
                print(vk.verify(signature, msg_hash.encode()))
                #print(type(vk.verify(signature, msg_hash.encode())))
                #if vk.verify(signature, msg_hash.encode()) == True:
                #    print("in")
                return vk.verify(signature, msg_hash.encode())
            except:
                #pass
                #print("None")
                if a == len(self.public_key_path) - 1:
                    #print("None")
                    return None
            
if __name__ == "__main__":
    ecc_obj = Ecc() # 例項化 
    msg_hash = '我是真心喜歡你的。skjbkj'
    print("msg_hash:",msg_hash)
    signature = ecc_obj.sign_ECDSA_msg(msg_hash) # 簽章
    print(type(signature))
    print("en_plain:",signature)
    signature = signature.decode('utf-8')
    print(type(signature))
    print("en_plain_1:",signature)
    #print(signature,msg_hash)
    ecc_obj.validate_signature(signature,msg_hash) # 驗證
    
    from datetime import datetime
    import time
    import random

    date_s = (datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

    print(date_s)
    
    print(type(date_s))
    
    print(type(time.ctime(time.time())))
    
    r = random.getrandbits(32)
    
    print(r)
