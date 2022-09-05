import rsa #之後註解
import base64
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Random import get_random_bytes
import ecdsa

#RSA的密鑰對
# 一、生成公鑰及私鑰,並儲存
public_key,private_key = rsa.newkeys(1024) # 生成公鑰和私鑰
# 將生成的公鑰和私鑰進行轉換，以便儲存
pub = public_key.save_pkcs1()
pri = private_key.save_pkcs1('PEM') # save_pkcsl()是內建方法，其預設引數是‘PEM'
with open('pubkey_1.txt',mode='wb') as f,open('privkey_1.txt',mode='wb') as f1:
  f.write(pub) # 開啟兩個檔案，分別儲存公鑰及私鑰
  f1.write(pri)
  f.close()
  f1.close()

public_key,private_key = rsa.newkeys(1024)
#print(public_key,private_key)
pub = public_key.save_pkcs1()
pri = private_key.save_pkcs1('PEM') 
with open('pubkey_2.txt',mode='wb') as f,open('privkey_2.txt',mode='wb') as f1:
  f.write(pub) 
  f1.write(pri)
  f.close()
  f1.close()
  
public_key,private_key = rsa.newkeys(1024) 
#print(public_key,private_key)
pub = public_key.save_pkcs1()
pri = private_key.save_pkcs1('PEM') 
with open('pubkey_3.txt',mode='wb') as f,open('privkey_3.txt',mode='wb') as f1:
  f.write(pub) 
  f1.write(pri)
  f.close()
  f1.close()
  
public_key,private_key = rsa.newkeys(1024) 
#print(public_key,private_key)
pub = public_key.save_pkcs1()
pri = private_key.save_pkcs1('PEM') 
with open('pubkey_4.txt',mode='wb') as f,open('privkey_4.txt',mode='wb') as f1:
  f.write(pub) 
  f1.write(pri)
  f.close()
  f1.close()

public_key,private_key = rsa.newkeys(1024) 
#print(public_key,private_key)
pub = public_key.save_pkcs1()
pri = private_key.save_pkcs1('PEM') 
with open('pubkey_fake.txt',mode='wb') as f,open('privkey_fake.txt',mode='wb') as f1:
  f.write(pub) 
  f1.write(pri)
  f.close()
  f1.close()

#AES的密鑰對
keys = get_random_bytes(32)
with open('keys.txt',mode='wb') as f:
    f.write(keys) 
    f.close()
    
keys = get_random_bytes(32)
with open('fake_keys.txt',mode='wb') as f:
    f.write(keys) 
    f.close()
  
#ECC的密鑰對   
def generate_ECDSA_keys():

    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1) #this is your sign (private key)
    private_key = sk.to_string().hex() #convert your private key to hex
    vk = sk.get_verifying_key() #this is your verification key (public key)
    public_key = vk.to_string().hex()
    #we are going to encode the public key to make it shorter
    public_key = base64.b64encode(bytes.fromhex(public_key))
    return public_key.decode(), private_key

public_key, private_key = generate_ECDSA_keys()

with open('pubkey_ECC_1.txt',mode='w') as f,open('privkey_ECC_1.txt',mode='w') as f1:
        f.write(public_key) # 開啟兩個檔案，分別儲存公鑰及私鑰
        f1.write(private_key)
        f.close()
        f1.close()
                
public_key, private_key = generate_ECDSA_keys()

with open('pubkey_ECC_2.txt',mode='w') as f,open('privkey_ECC_2.txt',mode='w') as f1:
        f.write(public_key) # 開啟兩個檔案，分別儲存公鑰及私鑰
        f1.write(private_key)
        f.close()
        f1.close()

public_key, private_key = generate_ECDSA_keys()

with open('pubkey_ECC_3.txt',mode='w') as f,open('privkey_ECC_3.txt',mode='w') as f1:
        f.write(public_key) # 開啟兩個檔案，分別儲存公鑰及私鑰
        f1.write(private_key)
        f.close()
        f1.close()

public_key, private_key = generate_ECDSA_keys()

with open('pubkey_ECC_4.txt',mode='w') as f,open('privkey_ECC_4.txt',mode='w') as f1:
        f.write(public_key) # 開啟兩個檔案，分別儲存公鑰及私鑰
        f1.write(private_key)
        f.close()
        f1.close()

public_key, private_key = generate_ECDSA_keys()

with open('pubkey_ECC_fake.txt',mode='w') as f,open('privkey_ECC_fake.txt',mode='w') as f1:
        f.write(public_key) # 開啟兩個檔案，分別儲存公鑰及私鑰
        f1.write(private_key)
        f.close()
        f1.close()
        
 #==================================================================== =============
"""
pubkey = []
prikey = []
with open('pubkey_1.txt',mode='r') as f:
    f1 = f.read()
    pubkey.append(f1)
    f.close()
    
with open('privkey_1.txt',mode='r') as f:
    f1 = f.read()
#    print(type(f1))
    prikey.append(f1)
    f.close()
    
print('pubkey:',pubkey)
print('prikey:',prikey)
"""