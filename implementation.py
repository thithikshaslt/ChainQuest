
import hashlib      

i = int(input())
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
    if i == 1:
        data = input(f"Enter data for node {i + 1}: ")
        node = Node(i + 1, data)
        nodes.append(node)
    else:
        data = hash(i-1)
    
    return nodes

def print_nodes(nodes):
    for node in nodes:
        print(f"Node {node.index}: Index = {node.index}, Data = {node.data}, Hash = {node.hash}")