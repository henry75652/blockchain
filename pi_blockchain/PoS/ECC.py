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
       #print("test_1_1",type(msg_hash.encode()))
       #print("test_1_1_1",msg_hash.encode())
       byte_msg_hash = msg_hash.encode()
       sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)
       signature = base64.b64encode(sk.sign(byte_msg_hash))
       while (len(signature) - 1) == 0: ##test
           signature = base64.b64encode(sk.sign(byte_msg_hash))  ##test
       #print("[test_type_1]",type(sk.sign(byte_msg_hash)))
       #print("[test_type_1_con]",sk.sign(byte_msg_hash))
       #print("[test_type_1_con_len]",len(sk.sign(byte_msg_hash)))
       #print("test_1",type(signature))
       #print("test_1_1",signature)    ###debug用
       #print("test_1_1_len",len(signature))
       #signature = base64.b64decode(signature)
       #print("test_2",type(signature))
       #print("test_2_1",signature)
       return signature
         #return signature, msg_hash

   def validate_signature(self,signature, msg_hash):
       
        #signature = signature.encode('utf-8')
        #signature = base64.b64decode(signature.encode('utf-8')+ b'=' * (-len(signature) % 4)) ####改，不然會出事
        #print("[test]",type(signature))
        #print("[test_con]",signature)    ###debug用
        #print("[test_con_1]",(signature + b'=' * (-len(signature) % 4)))    ###debug用
        signature = base64.b64decode(signature + b'=' * (4-len(signature) % 4)) ####改，不然會出事
        #signature = base64.b64decode(signature) ####改，不然會出事
        #print("[test_con_2]",signature)
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
    #msg_hash = '我是真心喜歡你的。skjbkj'
    msg_hash = '000c67ed65205018492ffcc37f21c0ea12e8ba49e1a710f22159912bb0f1cb5c'
    print("msg_hash:",msg_hash)
    signature = ecc_obj.sign_ECDSA_msg(msg_hash) # 簽章
    print("[test_type]",type(signature))
    print("en_plain:",signature)
    #signature = signature.decode('utf-8')
    print(type(signature))
    print("en_plain_1:",signature)
    #print(signature,msg_hash)
    ecc_obj.validate_signature(signature,msg_hash) # 驗證
    
    import libnum
    import math
    import gmpy2
    p=libnum.generate_prime(1024)
    q=libnum.generate_prime(1024)
    print("p:",p)
    print("q:",q)
    e1=7
    e2=8191
    n=p*q
    m = "canyoubemyfriend"
    m_dec = 132099465064143360681164975903831584356
    c1=pow(m_dec,e1,n)
    c2=pow(m_dec,e2,n)
    print("n1=",n)
    print("e1=",e1)
    print("c1=",c1)
    print("n2=",n)
    print("e2=",e2)
    print("c2=",c2)
    
    def rsa_gong_N_def(e1,e2,c1,c2,n):
        e1, e2, c1, c2, n=int(e1),int(e2),int(c1),int(c2),int(n)
        s = gmpy2.gcdext(e1, e2)
        s1 = s[1]
        s2 = s[2]
        if s1 < 0:
            s1 = - s1
            c1 = gmpy2.invert(c1, n)
        elif s2 < 0:
            s2 = - s2
            c2 = gmpy2.invert(c2, n)
        m = (pow(c1,s1,n) * pow(c2 ,s2 ,n)) % n
        return int(m)
    
    m = rsa_gong_N_def(e1,e2,c1,c2,n)
    print("m",m)
    
    id_1 = [100,100,100,100]
    id_1_str = str(id_1)
    
    id_1_str = id_1_str.replace("[","").replace("]","")
    data = list()
    id_1_str = id_1_str.split(",")
    for _ in id_1_str:
        data.append(int(_))
    
    print("type",type(data))
    print("info",data)

    import AES_en
    import fake_AES_en
    
    secretkey = ['6agrioBE1D9yoGOX4yyDMyMFs72jYvJ8', '6agru3BE1D9yoGOX4u3DMyMFs72jYvJ8'] ##
    AES0 = AES_en.AESCipher(secretkey[0])        ##
    AES1 = fake_AES_en.AESCipher(secretkey[1])        ##
    
    a = "aaa"
    a_en = AES0.encrypt(a)
    a_de = AES1.decrypt(a_en)
    
    print("[tses]",a_de)
    
    a = None
    
    print("type",type(a))
    print("none",a)
    
    a = 15
    a /= 15
    print("num",a)
    
    b = [1,2,3]
    
    print("b_2",b[2])

    """
    from datetime import datetime
    import time
    import random

    date_s = (datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

    print(date_s)
    
    print(type(date_s))
    
    print(type(time.ctime(time.time())))
    
    r = random.getrandbits(32)
    
    print(r)
    
    print("true_test_len",(b'HP4eU3LQT5SMGX9pYVlnIraizv1tk5z+aQzo0nBVRu5eMAVFD36tw//+vnmx8MkBoIV8Ag1KpQQ5CTSgl2XZhA==').decode())
    
    print("true_test",base64.b64decode(b'HP4eU3LQT5SMGX9pYVlnIraizv1tk5z+aQzo0nBVRu5eMAVFD36tw//+vnmx8MkBoIV8Ag1KpQQ5CTSgl2XZhA=='))
    
    en_msg_hash = msg_hash.encode()
    
    print("encode",en_msg_hash)
    
    de_msg_hash = en_msg_hash.decode()
    
    print("decode",de_msg_hash)
    """
    """
    def go_fuck(string):
            #print("[go_fuck_yourself.go_fuck]======================")
            #print("[go_fuck_yourself.go_fuck]string:",string)
            if("fuck:" in string):
                #print("fuck: is in string")
                string = string.split("fuck:")
                #print(string)
                #print(string[1])    #[(9, 8, 7, 6, 5, 4, 3, 2, 1)(1, 2, 3, 4, 5, 6, 7, 8, 1)]
                string = string[1].replace("[","").replace("]","")
                #print(string)   #(9, 8, 7, 6, 5, 4, 3, 2, 1)(1, 2, 3, 4, 5, 6, 7, 8, 1)
                string = string.replace("(","")
                #print(string)
                string = string.split(")")
                string = string[0:-1]
                #print(string)   #['9, 8, 7, 6, 5, 4, 3, 2, 1', '1, 2, 3, 4, 5, 6, 7, 8, 1', '']
                data = list()
                for _ in string:
                    temp = _.split(",")
                    row = list()
                    for x in temp:
                        try:
                            row.append(int(x))
                        except:
                            x = x.replace(" '","").replace("'","")
                            row.append(x)
                            pass 
                    #print(temp)
                    data.append(row)
                print("[go_fuck]",data)
                print("[go_fuck_1]",len(data[17][0]))
                print("[go_fuck_2]",data[17][1])
                return data
            else:
                pass
    
    a = "fuck:[(6, 4, 5, 9, 1, 2, 8, 3, 7)(7, 6, 8, 2, 9, 4, 1, 5, 3)(9, 7, 2, 3, 5, 8, 4, 1, 6)(7, 6, 8, 2, 9, 4, 1, 5, 3)(9, 7, 2, 3, 5, 8, 4, 1, 6)(4, 3, 1, 6, 8, 5, 2, 7, 9)(17934, 29872, 24487, 37369, 16237, 41697, 43017, 33453, 14488)(20693, 53774, 10472, 24351, 50020, 1666, 16060, 1352, 29349)(2575, 48755, 41416, 32062, 572, 35204, 48528, 831, 37820)(20693, 53774, 10472, 24351, 50020, 1666, 16060, 1352, 29349)(2575, 48755, 41416, 32062, 572, 35204, 48528, 831, 37820)(56462, 45589, 6417, 54428, 28293, 8596, 20171, 43253, 49048)('463fa93603ee1e88e1b997717d4ca9188dbb13f52337adde695e5d1fc94bacf1', 'cea0fd0b89097e1c9b7ccb44e0a5a349f4c5da8a74dcb34992d7ee22db3d7106', '4950fa48ff94fb26e8ecf002ed95ea97006b1b620c4f189c38ddddd7c564d475', '1faca35f2ce9d6612bcf147f7ab427e7dedfc4c4c3166500c1fb43fc08f99bad', '6f8e7fe41d92afe70373b5c27e25fcbbb6656caee50c686105520ac48762faa3', '948d3970a7e45812c1f755326a1551485539014765f0dfd50398ec1bccd0d2c6', 'ea1ace2ebeb27517626af91d6eccb89751adb5307d3e4bf56f71fc51bc380a18', '94fd419d9732940a8d903e0729554f56b292ea23e4faa22eb409ee98f7cc66c0', 'cdeeb31b449ac03d190ada9f0befaeebf5637d21d94017bd1cee3109375a545f')('94c5acc3ebe2763a8140c4fc8c26bc38c5baeffad8ec61dd54779d480697928d', 'c1bed37705b2a40190a0c4fb65d94ed84f66f96e8ab1ac25e35b78f800f127c5', '4b0cb955415fb749489f27a677bc89b9ae410f96cf1e79edd29d756b7274cb28', '72bd9519a92d4cc0f7f29b842da6c59200b3d675268cb17d5b4245244a94aeaf', 'e2cda74d0984933dc67f6f316c103f8b4d0301ac6125e08a5508134936b052fc', 'd8a9220e637c9a7b377eabb60059a170c30384f5704c0e81a49f31788d470c98', '5764412f7b7e6c11900fe6f51a8cca0a2bab54400cdfb173a9b0d6f60d1ed117', '2e1b9b762e6df07711fef278069048e380db1fb04c3d30799b85095f8845895e', 'a78f95a4d58dc514f1b7450e16511f097f71092c4330c6cf738266758671ca1f')('4ae6d3eaa39eb355c704f2c1ec4ddfe16a12f416f429a0a1d599ce2322a2ed14', '1a85f4e53396c5f409689aa7de19fa4b0abc5bca3d154c9860d9e77b2dca135c', '3f2a237f2741e0df160f5cb25b9ea19933eb7393d207ad734ecb3274ae5227a3', 'e316220c93754d95d49e3ed521934017e90957e8c23cb288a1a5a0c54309b506', '9cd990a7894fcb3ae3c016d7a1f1e0b009fc91cbc791df830a51f6e34630453a', 'dbc8a24558893a942470c2ff15cc43bb18fd4fa03d54f3b0549871bd31208df6', 'e7bd9fddf7889b1a45b01e180a9df4980484e98bd3f29214e12ca96a3ed6cf11', 'ca3b40e3f4a5398e09fb11f8eab42096630c3acbd6dce26656a90fdf72b87169', '605c9f920c8cbd27f63739b906652e7bb8102a9b9bc8e9d1034de0feeb8b9874')('94c5acc3ebe2763a8140c4fc8c26bc38c5baeffad8ec61dd54779d480697928d', 'c1bed37705b2a40190a0c4fb65d94ed84f66f96e8ab1ac25e35b78f800f127c5', '4b0cb955415fb749489f27a677bc89b9ae410f96cf1e79edd29d756b7274cb28', '72bd9519a92d4cc0f7f29b842da6c59200b3d675268cb17d5b4245244a94aeaf', 'e2cda74d0984933dc67f6f316c103f8b4d0301ac6125e08a5508134936b052fc', 'd8a9220e637c9a7b377eabb60059a170c30384f5704c0e81a49f31788d470c98', '5764412f7b7e6c11900fe6f51a8cca0a2bab54400cdfb173a9b0d6f60d1ed117', '2e1b9b762e6df07711fef278069048e380db1fb04c3d30799b85095f8845895e', 'a78f95a4d58dc514f1b7450e16511f097f71092c4330c6cf738266758671ca1f')('4ae6d3eaa39eb355c704f2c1ec4ddfe16a12f416f429a0a1d599ce2322a2ed14', '1a85f4e53396c5f409689aa7de19fa4b0abc5bca3d154c9860d9e77b2dca135c', '3f2a237f2741e0df160f5cb25b9ea19933eb7393d207ad734ecb3274ae5227a3', 'e316220c93754d95d49e3ed521934017e90957e8c23cb288a1a5a0c54309b506', '9cd990a7894fcb3ae3c016d7a1f1e0b009fc91cbc791df830a51f6e34630453a', 'dbc8a24558893a942470c2ff15cc43bb18fd4fa03d54f3b0549871bd31208df6', 'e7bd9fddf7889b1a45b01e180a9df4980484e98bd3f29214e12ca96a3ed6cf11', 'ca3b40e3f4a5398e09fb11f8eab42096630c3acbd6dce26656a90fdf72b87169', '605c9f920c8cbd27f63739b906652e7bb8102a9b9bc8e9d1034de0feeb8b9874')('826534ae96ffc3a0e0c4fff0928bbb5267e072c828866072bf1c17e756b2fedf', '0855687b4a7b3d94285881a3d9ccfbd662787dfa7691fdaab42742d4f2b1b96a', 'c2e2f89f124148b1ea5576e323f87225b6210cb65e5e0877498e045dbc64e0a9', 'e46680376148e549e39a63a627bd3bf0a98832d4b2410563421892de997e0f86', '3084bec84a1d786f1f9916bd7cb389729410797462bcae9d29e251d5fd73c39c', '0d4298d0b77faf9fba0b61b409959fc43bb3c3a2f9f48a3bc1f5dd70a40c69e7', 'cf49a19dc068c9d9d90c3af5db9851dd55a88bc728acf593b44030e6aea8cd96', '6a823c0a8e03d65ba7dccb02a7962dd2fb0f6859a22025da7dd804a383c4d877', '5ed7b9155273a7de4cec3a78537019e2383fb930a4bfdd0ca22c6eea6b40e871')]"
    
    go_fuck(a)
    """
