import hashlib

class Node:
    def __init__(self, index, data, original_data):
        self.index = index
        self.data = data
        self.original_data = original_data
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(self.data.encode('utf-8'))
        return sha.hexdigest()

def create_nodes():
    while True:
        try:
            num_nodes = int(input("Enter the number of nodes: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    nodes = []
    data = input("Enter data for node 1: ")
    for i in range(num_nodes):
        original_data = data
        node = Node(i + 1, data, original_data)
        nodes.append(node)
        data = node.hash  
    
    return nodes

def print_nodes(nodes):
    for node in nodes:
        print(f"Node {node.index}: Original Data = {node.original_data}, Hashed Data = {node.hash}")

def main():
    nodes = create_nodes()
    print_nodes(nodes)

if __name__ == "__main__":
    main()
