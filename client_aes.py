import socket
import hashlib

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def calculate_hash(self, data):
        sha = hashlib.sha256()
        sha.update(data)
        return sha.digest()  

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            print('Connected to the server.')

            
            data = s.recv(1024)
            print(f"Data received: {data.hex()}")

            if len(data) > 16:  
                iv = data[:16]
                encrypted_data = data[16:]
                s.sendall(data)  

           
            hash_result = self.calculate_hash(data)
            print(f"Hashed data to send back: {hash_result.hex()}")
            s.sendall(hash_result)

def main():
    host = 'localhost'
    port = 65432
    client = Client(host, port)
    client.start()

if __name__ == "__main__":
    main()
