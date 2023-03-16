import base64
import ecdsa
    
class Ecc(object):
   def __init__(self):
        
        pri_path = ['privkey_ECC_fake.txt']
        self.public_key_path = ['pubkey_ECC_fake.txt']
        self.privaue_key_path = pri_path[0]

   def sign_ECDSA_msg(self,msg_hash): #簽章
       
       with open(self.privaue_key_path,mode='r') as f:
             private_key = f.read()
             f.close()
         #message = '我是真心喜歡你的。skjbkj'
       byte_msg_hash = msg_hash.encode()
       sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)
       signature = base64.b64encode(sk.sign(byte_msg_hash))
       while (len(signature) - 1) == 0: ##test
           signature = base64.b64encode(sk.sign(byte_msg_hash))  ##test
       return signature
         #return signature, msg_hash

   def validate_signature(self,signature, msg_hash):
       
        #signature = signature.encode('utf-8')
        signature = base64.b64decode(signature + b'=' * (4-len(signature) % 4)) 
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
    
    decimal = 13


    # Convert
    binary = bin(decimal)
    octal = oct(decimal)
    hexadecimal = hex(decimal)
    
    print("hex",hexadecimal)
    print("type",type(hexadecimal))
    
    
    # Print
    print('Bin => Dec:', int(binary, 2))
    print('Oct => Dec:', int(octal, 8))
    print('Hex => Dec:', int(hexadecimal, 16))
    print('Hex => bin:', bin(int(hexadecimal, 16)))
    
    
    hex_1 = "ff0b844a0853bf7c6934ab4364148fb9"
    
    k = ""
    for i in range(16):
        c = "0x"
        j = ""
        for a in range(2):
            j = j + hex_1[2*i + a]
        c = c + j
        print("hex_test",c)
        print("bin_test",bin(int(c, 16)))
        #print("len_bin_test",len(bin(int(c, 16))))
        if len(bin(int(c, 16))) != 10:
            bin_1 = ""
            for i in range(10 - len(bin(int(c, 16)))):
                bin_1 = bin_1 + "0"
            bin_1 = bin_1 + bin(int(c, 16))[2:]
            print('Hex => bin:', bin_1)
        else:
            print('Hex => bin:', bin(int(c, 16))[2:])
        k = k + bin(int(c, 16))[2:]
    print("final_bin",k)
