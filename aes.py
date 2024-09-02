from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

# Function to pad the plaintext to a multiple of the block size
def pad(data):
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    return padded_data

# Function to unpad the decrypted plaintext
def unpad(data):
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(data) + unpadder.finalize()
    return unpadded_data

# Function to encrypt plaintext using AES-128 with a fixed IV
def aes_encrypt(plaintext, key):
    iv = b'\x00' * 16  # Fixed IV (16 bytes of zeros)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_plaintext = pad(plaintext)
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    return iv + ciphertext

# Function to decrypt ciphertext using AES-128 with a fixed IV
def aes_decrypt(ciphertext, key):
    iv = ciphertext[:16]
    actual_ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()
    plaintext = unpad(padded_plaintext)
    return plaintext

def main():
    key = b'\x00' * 16  # Fixed 128-bit key (16 bytes of zeros)
    plaintext = input("Enter the plaintext to encrypt: ").encode()  # Get plaintext from user

    # Encrypt the plaintext
    ciphertext = aes_encrypt(plaintext, key)
    print(f'Ciphertext: {ciphertext.hex()}')

    # Decrypt the ciphertext
    decrypted_plaintext = aes_decrypt(ciphertext, key)
    print(f'Decrypted Plaintext: {decrypted_plaintext.decode()}')
   # print(iv)

if __name__ == "__main__":
    main()
