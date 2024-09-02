from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

def encrypt(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    return cipher.iv, ct_bytes

def main():
    num_nodes = int(input("Enter the number of nodes: "))
    key = get_random_bytes(16)  
    print(key)
    nodes = []
    for i in range(num_nodes):
        data = input(f"Enter data for node {i + 1}: ")
        iv, encrypted_data = encrypt(data, key)
        nodes.append((iv.hex(), encrypted_data.hex()))
        print(f"Node {i + 1}:  Encrypted Data = {encrypted_data.hex()}")

    # Save key for decryption
    with open('key.bin', 'wb') as key_file:
        key_file.write(key)

if __name__ == "__main__":
    main()
