# -*- coding: utf-8 -*-
from Crypto.Hash import HMAC, MD5, SHA256
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
#f336c40951b7df021ed6ab6cff65109ad53567ea
#1.0.0  162636
# 'commit_hash': encrypt(pid, SECRET, latest_commit_hash)#最新一次的commit进行加密
#decrypt(pid, SECRET, origin_hash)
def generateKIV(project_id: str, secret: str):
    project_id = project_id.encode('utf-8')
    secret = secret.encode('utf-8')
    # K is 256bits, IV is 16bytes=128bit
    hK = HMAC.new(secret, digestmod=SHA256)
    hIV = HMAC.new(secret, digestmod=MD5)
    hK.update(project_id)
    hIV.update(project_id)
    K = hK.digest()
    IV = hIV.digest()
    return K, IV


def encrypt(project_id: str, secret: str, plain_text: str) -> str:
    plain_text = plain_text.encode('utf-8')
    K, IV = generateKIV(project_id, secret)
    cipher = AES.new(K, AES.MODE_CFB, IV)
    cipher_bytes = cipher.encrypt(plain_text)
    # ciphertext contain only ASCII
    return b64encode(cipher_bytes).decode('utf-8')


def decrypt(project_id: str, secret: str, cipher_text: str) -> str:
    cipher_text = b64decode(cipher_text)
    K, IV = generateKIV(project_id, secret)
    cipher = AES.new(K, AES.MODE_CFB, IV)
    plain_bytes = cipher.decrypt(cipher_text)
    return plain_bytes.decode('utf-8')
if __name__ == "__main__":
    print(encrypt("whosbug_test_1","162636","f336c40951b7df021ed6ab6cff65109ad53567ea"))
    #print(decrypt("1.0.0","162636","RkbehL7mbXWMxWcom6b+6RldmMgWmP2SmY54onTsJPDzyo++/+B3ug=="))
