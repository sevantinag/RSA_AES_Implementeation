The RSA and AES programming consists of following files:
1. genkeys.py
2. crypt.py
3. message.txt
4. message2.txt

It is to be noted that no external code/library was used to implement RSA functionality. Pycrypto Library was used for AES algorithm. To install Pycrypto, type the following in command prompt or terminal: pip install pyCrypto

1. genkeys.py
  This python file is to generate RSA public and private keys. It accepts input from user through command prompt. The input would be a name that will be used to generate filenames of private and public key in keyGeneration() function. Miller-Rabin Algorithm is used to check the generated odd number to be prime in checkPrime() function. Euclid algorithm and Extensive Euclid Algorithm is used to find GCD and find the multiplicative inverse of 2 numbers respectively. Main() function is used to take in the input from command and send it to keyGeneration() function. Files {file_name}.pub.txt, and {file_name}.pub.txt are generated, which contain publc and private RSA keys respectively

2. crypt.py
  This python file is to encrypt and decrypt key and data using AES-128 and RSA. It accepts input from user through command prompt. The input would be a list of items, where 1st is to encrypt or decrypt, 2nd is the public or private key file, 3rd is the file to encrypt or decrypt, and 4th is the output file.
  As per the input value, if it is encryption, it goes to encrypt() function. The values of public key file, input plaintext file and output ciphertext file is passed. First the Plaintext is converted to ciphertext using AES CFB mode encryption and the IV and ciphertext are stored in JSON Format in the output ciphertext file. Then the AES Key, which is random 16 byte value is encrypted using RSA. This cipher is again stored in the output ciphertext file.
  If the input value is decryption, it goes to decrypt() function. The values of private key file, input ciphertext file and output plaintext file is passed. First the RSA private key is extracted from the private key file, then RSA decryption is done to decrypt the AES Key. This AES key is then used to decrypt the data using AES CFB mode decryption. The decrypted plaintext is then stored in output plaintext file.

3. message.txt
  This file consists of plaintext, which is initially added, but gets updated when ciphertext is
  decrypted

4. message2.txt
  This file consists of plaintext, which is initially added, but gets updated when ciphertext is
  decrypted

message.cip, message2.cip: Generated Ciphertext files which store the AES key and Data in
encrypted format.

alice.prv.txt, alice.pub.txt, bob.prv.txt, bob.pub.txt: Generated RSA public and private key files
