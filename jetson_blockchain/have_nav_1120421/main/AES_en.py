from Crypto.Cipher import AES  
from base64 import b64decode, b64encode
import hashlib

BLOCK_SIZE = AES.block_size
# 不足BLOCK_SIZE的补位(s可能是含中文，而中文字符utf-8编码占3个位置,gbk是2，所以需要以len(s.encode())，而不是len(s)计算补码)
pad = lambda s: s + (BLOCK_SIZE - len(s.encode()) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s.encode()) % BLOCK_SIZE)
# 去除补位
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

keys_path = ['keys.txt']

class AESCipher(object):
    def __init__(self, secretkey: str, keys_path = keys_path[0]):
        self.Keys_path = keys_path
        self.secretkey = secretkey
        #self.iv = secretkey[0:16]  # 偏移量
        


    def encrypt(self, text,nonce):

        self.nonce = nonce
        if len(str(self.nonce)) == 3:
            s_3 = self.nonce // 100
            s_2 = self.nonce // 10 - (self.nonce // 100 * 10)
            s_1 = self.nonce % 10
            self.hash_str = self.secretkey[0:s_3] + self.secretkey[s_3:s_3 + s_2] + self.secretkey[s_3 + s_2:s_3 + s_2 + s_1]
            self.hash = hashlib.sha256(self.hash_str.encode()).hexdigest()
            self.iv = self.hash[s_3:s_3 + 5] + self.hash[s_2:s_2 + 5] + self.hash[s_1:s_1 + 6]
        elif len(str(self.nonce)) == 2:
            s_2 = self.nonce // 10
            s_1 = self.nonce % 10
            self.hash_str = self.secretkey[0:s_2] + self.secretkey[s_2:s_2 + s_1]
            self.hash = hashlib.sha256(self.hash_str.encode()).hexdigest()
            self.iv = self.hash[s_2:s_2 + 8] + self.hash[s_1:s_1 + 8]
        else:
            s_1 = self.nonce % 10
            self.hash_str = self.secretkey[0:s_1]
            self.hash = hashlib.sha256(self.hash_str.encode()).hexdigest()
            self.iv = self.hash[s_1:s_1 + 16]
        #print("iv",self.iv)
        with open(self.Keys_path,mode='rb') as f:
            keys = f.read()
            
        text = pad(text).encode()  # 包pycryptodome 的加密函数不接受str
        cipher = AES.new(keys, mode=AES.MODE_CBC, IV=self.iv.encode())
        encrypted_text = cipher.encrypt(text)
        # 进行64位的编码,返回得到加密后的bytes，decode成字符串
        return b64encode(encrypted_text).decode('utf-8')

    def decrypt(self, encrypted_text,nonce):

        self.nonce = nonce
        if len(str(self.nonce)) == 3:
            s_3 = self.nonce // 100
            s_2 = self.nonce // 10 - (self.nonce // 100 * 10)
            s_1 = self.nonce % 10
            self.hash_str = self.secretkey[0:s_3] + self.secretkey[s_3:s_3 + s_2] + self.secretkey[s_3 + s_2:s_3 + s_2 + s_1]
            self.hash = hashlib.sha256(self.hash_str.encode()).hexdigest()
            self.iv = self.hash[s_3:s_3 + 5] + self.hash[s_2:s_2 + 5] + self.hash[s_1:s_1 + 6]
        elif len(str(self.nonce)) == 2:
            s_2 = self.nonce // 10
            s_1 = self.nonce % 10
            self.hash_str = self.secretkey[0:s_2] + self.secretkey[s_2:s_2 + s_1]
            self.hash = hashlib.sha256(self.hash_str.encode()).hexdigest()
            self.iv = self.hash[s_2:s_2 + 8] + self.hash[s_1:s_1 + 8]
        else:
            s_1 = self.nonce % 10
            self.hash_str = self.secretkey[0:s_1]
            self.hash = hashlib.sha256(self.hash_str.encode()).hexdigest()
            self.iv = self.hash[s_1:s_1 + 16]
        #print("iv",self.iv)
        with open(self.Keys_path,'rb') as f:
            keys = f.read()
            
        encrypted_text = b64decode(encrypted_text)
        cipher = AES.new(keys, mode=AES.MODE_CBC, IV=self.iv.encode())
        decrypted_text = cipher.decrypt(encrypted_text)
        return unpad(decrypted_text).decode('utf-8')
    
if __name__ == "__main__":
    
    secretkey = '6agrioBE1D9yoGOX4yyDMyMFs72jYvJ8'  # 密钥 重要，之後要換金鑰可從這裡改
    aes_obj = AESCipher(secretkey)
#    text = '使用 pycryptodome 进行 AES/CBC/PKCS5(算法/模式/补码方式) 加密sdmcbskcj'  # 待加密的明文
#    encrypted_text = aes_obj.encrypt(text)  # 加密
#    print(encrypted_text)
#    print(type(encrypted_text))
#    decrypted_text = aes_obj.decrypt(encrypted_text)  # 解密
#    print(decrypted_text)
#    print(type(decrypted_text))