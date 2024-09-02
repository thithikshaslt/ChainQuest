import hashlib

class Node:
    def __init__(self, index, data):
        self.index = index
        self.data = data
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.index).encode('utf-8') + str(self.data).encode('utf-8'))
        return sha.hexdigest()

def create_nodes():
    while True:
        try:
            num_nodes = int(input("Enter the number of nodes: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    nodes = []
    for i in range(num_nodes):
        data = input(f"Enter data for node {i + 1}: ")
        node = Node(i + 1, data)
        nodes.append(node)
    
    return nodes

def print_nodes(nodes):
    for node in nodes:
        print(f"Node {node.index}: Index = {node.index}, Data = {node.data}, Hash = {node.hash}")

def main():
    nodes = create_nodes()
    print_nodes(nodes)

if __name__ == "__main__":
    main()

#send single data thru multiple nodes, hash it, give it as input to the next node and so on. at the last node decode the originally sent data. 
#layer-wise decode
#create db , username pwd, close, same hash, compare
#encrypt that data, same key, give at decrypt
#client to server , 4 client, diff username, pwd
#enc key in client (seed-time) decryp key at server