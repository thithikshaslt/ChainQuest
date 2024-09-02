from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def decrypt(iv, ct, key):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode('utf-8')

def load_key():
    with open('key.bin', 'rb') as key_file:
        return key_file.read()

def main():
    key = load_key()
    print(key)
    num_nodes = int(input("Enter the number of nodes: "))

    for i in range(num_nodes):
        # iv_hex = input(f"Enter IV for node {i + 1}: ")
        encrypted_data_hex = input(f"Enter encrypted data for node {i + 1}: ")
        
        # iv = bytes.fromhex(iv_hex)
        encrypted_data = bytes.fromhex(encrypted_data_hex)
        
        decrypted_data = decrypt('',encrypted_data, key)
        print(f"Node {i + 1}: Decrypted Data = {decrypted_data}")

if __name__ == "__main__":
    main()
