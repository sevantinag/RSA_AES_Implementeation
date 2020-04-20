#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import random
from random import randrange, getrandbits

#Perform Euclidean algorithm and return gcd of e and phi
def euc_algo(e, phi):
    while phi != 0:
        e, phi = phi, e % phi
    return e

#Perform extended Euclidean algorithm and find the multiplicative inverse of 2 nos
def ext_euc_algo(e, phi):
    new_x, old_x = 0, 1
    new_y, old_y = 1, 0

    while (phi != 0):
        quotient = e // phi
        e, phi = phi, e - quotient * phi
        old_x, new_x = new_x, old_x - quotient * new_x
        old_y, new_y = new_y, old_y - quotient * new_y

    return e, old_x, old_y

#Testing whether given number is prime using Miller-Rabin Algorithm
def checkPrime(n, k=128):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    
    # Finding r and s 
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    
    # Doing k number of tests
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True

#Generating random odd integer
def generateOddNum(length):
    odd_num = getrandbits(length)
    
    #  Masking for MSB and LSB setting to 1
    odd_num |= (1 << length - 1) | 1
    return odd_num

#Generate prime no.
def generatePrimeNum(length=1024):
    odd_num = 4
   
    # Generating prime no.
    while not checkPrime(odd_num, 128):
        odd_num = generateOddNum(length)
    return odd_num

#Generating 2 random prime numbers of 1024 bits and computing public and private keys, store in 2 txt files
def keyGeneration(file_name):
    # Generating 2 prime nos.
    first_prime = generatePrimeNum()
    second_prime = generatePrimeNum()
    
    n = first_prime * second_prime
    phi = (first_prime - 1) * (second_prime - 1)
    
    # Choosing integer e
    e = random.randrange(1, phi) 
    
    # Using Euclid's Algorithm to verify that e and phi(n) are comprime
    coprime_check = euc_algo(e, phi)
    while coprime_check != 1:
        e = random.randrange(1, phi)
        coprime_check = euc_algo(e, phi)
    
    # Using Extended Euclid's Algorithm to generate  private key
    gcd_val, old_x, old_y = ext_euc_algo(e, phi)

    # Checking if d is positive
    if (old_x < 0):
        d = old_x + phi
    else:
        d = old_x
    
   
    # Writing public keys n and e to a files
    f_public = open(f'{file_name}.pub.txt', 'w')
    f_public.write(str(n) + '\n')
    f_public.write(str(e) + '\n')
    f_public.close()

    # Writing private keys n and e to a files
    f_private = open(f'{file_name}.prv.txt', 'w')
    f_private.write(str(n) + '\n')
    f_private.write(str(d) + '\n')
    f_private.close()
    
def main():
    # Taking value from command for file's name
    raw_filename = sys.argv[1:]
    file_name = ' '.join([str(elem) for elem in raw_filename])


    keyGeneration(file_name)
    
if __name__ == "__main__":
    main()
