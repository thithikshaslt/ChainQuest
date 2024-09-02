import socket
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

class Server:
    def __init__(self, host, port, num_nodes):
        self.host = host
        self.port = port
        self.num_nodes = num_nodes
        self.key = get_random_bytes(16)  
        self.clients = []

    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
        return cipher.iv, ct_bytes

    def decrypt(self, iv, ct):
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode('utf-8')

    def start(self):
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()

            print('Server is listening for clients...')
            
            while len(self.clients) < self.num_nodes:
                conn, addr = s.accept()
                self.clients.append(conn)
                print(f'Client connected from {addr}')
            
            
            data = input("Enter data for node 1: ")
            iv, encrypted_data = self.encrypt(data)
            print(f"Original data: {data}")
            print(f"Encrypted data (hex): {iv.hex() + encrypted_data.hex()}")
            self.clients[0].sendall(iv + encrypted_data)

            
            for i in range(1, len(self.clients)):
                data = self.clients[i-1].recv(1024)
                hash_hex = data.hex()
                print(f"Hashed data at node {i}: {hash_hex}")
                self.clients[i].sendall(data)

            
            final_data = self.clients[-1].recv(1024)
            final_hash = final_data.hex()
            print(f"Final hashed data at last node: {final_hash}")

            
            decrypted_data = self.decrypt(iv, encrypted_data)
            print(f"\nDecrypted data: {decrypted_data}")

        
        with open('key.bin', 'wb') as key_file:
            key_file.write(self.key)

def main():
    host = 'localhost'
    port = 65432
    num_nodes = int(input("Enter the number of nodes: "))
    server = Server(host, port, num_nodes)
    server.start()

if __name__ == "__main__":
    main()
