#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import json
from base64 import b64encode, b64decode
from os import path
from Crypto.Cipher import AES
import random

aes_key = os.urandom(16)
iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])
rsa_block_size = 2



# Encrypting message from provided file using provided public key storing in provided file name
def encrypt(key_name, encrypt_file, output_file, aes_key, rsa_block_size):
    
    
    # Getting plaintext
    with open(encrypt_file) as open_file:
        line_msg = [line.rstrip() for line in open_file]
    message = ' '.join([str(elem) for elem in line_msg]) 
    
    
    #AES Encryption using CFB. IV and Data ciphertext is stored in JSON format
    cipher = AES.new(aes_key, AES.MODE_CFB)
    ct_bytes = cipher.encrypt(message.encode())
    iv = b64encode(cipher.iv).decode('utf-8')
    aes_cipher_text = b64encode(ct_bytes).decode('utf-8')
    aes_result = json.dumps({'iv':iv, 'ciphertext':aes_cipher_text})
    
    cipher_file = open(output_file, "w")
    cipher_file.write(aes_result)
    cipher_file.close()

    # Getting public key
    key_file = open(key_name, 'r')
    n = int(key_file.readline())
    e = int(key_file.readline())
    key_file.close()

    encrypted_blocks = []
    ciphertext = -1
    aes_key = str(aes_key)
    
    if (len(aes_key) > 0):
        # Initializing ciphertext to ASCII version of 1st ciphertext character
        ciphertext = ord(aes_key[0])

    for i in range(1, len(aes_key)):
        if (i % rsa_block_size == 0):
            encrypted_blocks.append(ciphertext)
            ciphertext = 0

        # Multiplying 1000 to move digits over to MSB
        ciphertext = ciphertext * 1000 + ord(aes_key[i])

    # Adding ciphertext to list
    encrypted_blocks.append(ciphertext)

    # Encrypting values by using power of e
    for i in range(len(encrypted_blocks)):
        encrypted_blocks[i] = str(pow(encrypted_blocks[i],e, n))

    # Creating a string from the numbers
    encrypted_message = " ".join(encrypted_blocks)

    #Storing the ciphertext of the AES key into file
    with open(output_file, 'a') as f:
        f.write("\n")
        f.write(encrypted_message)
    

# Decrypting message from provided file using provided private key storing in provided file name
def decrypt(key_name, encrypt_file, output_file, rsa_block_size):
    
    #Extracting RSA private key
    key_file = open(key_name, 'r')
    n = int(key_file.readline())
    d = int(key_file.readline())
    key_file.close()
    
    #Extracting AES Key Cipher and RSA encrypted Data
    message_file = open(encrypt_file, 'r')
    aes_cipher_text_str = message_file.readline()
    rsa_cipher_text_list_str = message_file.readlines() 
    
    #Converting the extracted key cipher into blocks
    aes_key_blocks = rsa_cipher_text_list_str[0].split(' ')
    aes_int_blocks = []
    
    for aes_key_block in aes_key_blocks:
        aes_int_blocks.append(int(aes_key_block))
    
    aes_message = ""
    
    for i in range(len(aes_int_blocks)):
        # Decrypting all blocks by raising to the power of d
        aes_int_blocks[i] = pow(aes_int_blocks[i],d, n)
        temp = ""
        
        #Splitting values into its corresponding ASCII codes
        for c in range(rsa_block_size):
            temp = chr(aes_int_blocks[i] % 1000) + temp
            aes_int_blocks[i] //= 1000
            
        aes_message += temp
    
    #Converting the message into the byte formatted AES Key
    key_cipher = aes_message[2:-1].encode()
    key_cipher_decoded = key_cipher.decode('unicode-escape')
    key_cipher_encoded = key_cipher_decoded.encode('ISO-8859-1')
    key_plaintext = key_cipher_encoded[:16]
    
    #Decrypting the Data using AEs Key and CFB mode
    b64 = json.loads(aes_cipher_text_str)
    iv = b64decode(b64['iv'])
    ct = b64decode(b64['ciphertext'])
    cipher = AES.new(key_plaintext, AES.MODE_CFB, iv=iv)
    pt = cipher.decrypt(ct)
    plain_text = pt.decode()

    #Storing Decrypted data in file
    with open(output_file, 'w') as f:
        f.write(plain_text)
        f.write("\n")

def main():
    # Taking value from command for file's name
    raw_cmd = sys.argv[1:]
    do_encrypt= raw_cmd[0]
    key_name =raw_cmd[1]
    encrypt_file = raw_cmd[2]
    output_file = raw_cmd[3]

    # Encrypting or decrypting based on command
    if  do_encrypt == "-e":
        if "pub" in key_name:
            if path.exists(encrypt_file):
                encrypt(key_name, encrypt_file, output_file,aes_key,rsa_block_size)
            else:
                print(f"{encrypt_file} does not exist")
        else:
            print("Public key should be used")
    
    elif do_encrypt == "-d":
        if "prv" in key_name:
            if path.exists(encrypt_file):
                decrypt(key_name, encrypt_file, output_file, rsa_block_size)
            else:
                print(f"{encrypt_file} does not exist")
        else:
            print("Private key should be used")
    
if __name__ == "__main__":
    main()
