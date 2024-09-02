import hashlib
import json
from time import time

class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")

    def add_block(self, block):
        block.previous_hash = self.chain[-1].hash
        block.hash = block.calculate_hash()
        self.chain.append(block)

    def print_blocks(self):
        for block in self.chain:
            print(f"Block {block.index}: Data = {block.data}, Hash = {block.hash}")

def main():
    # Create a new blockchain instance
    blockchain = Blockchain()

    # Take input from the user for the initial data
    initial_data = input("Enter initial data for the first block: ")

    # Add the first block to the blockchain with the initial data
    blockchain.add_block(Block(1, initial_data, "0"))

    # Hash the data from one block to the next until the specified number of blocks is reached
    num_blocks = int(input("Enter the number of blocks in the blockchain: "))
    for i in range(2, num_blocks + 1):
        previous_data = blockchain.chain[-1].data
        new_data = hashlib.sha256(previous_data.encode()).hexdigest()  # Hash previous block's data
        blockchain.add_block(Block(i, new_data, ""))

    # Print all blocks in the blockchain
    blockchain.print_blocks()

if __name__ == "__main__":
    main()
