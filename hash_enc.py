import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

class Node:
    def __init__(self, index, data, original_data, iv=None):
        self.index = index
        self.data = data
        self.original_data = original_data
        self.iv = iv
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(self.data.encode('utf-8'))
        return sha.hexdigest()

def encrypt(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    return cipher.iv, ct_bytes

def decrypt(iv, ct, key):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode('utf-8')

def create_nodes():
    while True:
        try:
            num_nodes = int(input("Enter the number of nodes: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    key = get_random_bytes(16)  
    nodes = []

    data = input("Enter data for node 1: ")
    iv, encrypted_data = encrypt(data, key)
    encrypted_data_hex = encrypted_data.hex()

    
    first_node = Node(1, encrypted_data_hex, data, iv.hex())
    nodes.append(first_node)

    
    current_data = first_node.hash
    for i in range(1, num_nodes):
        node = Node(i + 1, current_data, current_data)
        nodes.append(node)
        current_data = node.hash  

    with open('key.bin', 'wb') as key_file:
        key_file.write(key)
    
    return nodes, key

def print_nodes(nodes):
    for node in nodes:
        if node.iv:
            print(f"Node {node.index}: Original Data = {node.original_data}, Encrypted Data = {node.data}, IV = {node.iv}, Hashed Data = {node.hash}")
        else:
            print(f"Node {node.index}: Data = {node.data}, Hashed Data = {node.hash}")

def main():
    nodes, key = create_nodes()
    print_nodes(nodes)

    
    first_node = nodes[0]
    iv = bytes.fromhex(first_node.iv)
    encrypted_data = bytes.fromhex(first_node.data)
    decrypted_data = decrypt(iv, encrypted_data, key)
    print(f"\nDecrypted data at first node: {decrypted_data}")

if __name__ == "__main__":
    main()
