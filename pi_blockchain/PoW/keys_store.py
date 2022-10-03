import base64
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Random import get_random_bytes
import ecdsa

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
