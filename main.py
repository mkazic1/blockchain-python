# Module 1 - Create a Blockchain

# To be installed:
# Flask==0.12.2: pip install Flask==0.12.2
# Postman HTTP Client: https://www.getpostman.com/

# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify


# Part 1 - Building a Blockchain
# Flow: Define a chain, create genesis block and new blocks, make sure to have a solid blockchain
class Blockchain:
    # Always start with a init method in a class
    def __init__(self):
        # Chain that contains all the blocks in blockchain
        self.chain = []
        self.create_block(proof=1, previous_hash="0")

    def create_block(self, proof, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "proof": proof,
            "previous_hash": previous_hash
        }
        self.chain.append(block)
        return block

    # Get the previous block of the current chain
    def get_previous_block(self):
        return self.chain[-1]

    # Make a proof of work to define the problem that the minors will have to solve to mine a block
    # In programmers logic it is the function that the minors have to execute to get the proof
    # Returns proof needed to create a new block
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            # Function sha256 receives a string encoded in the right format that suits sha256 function
            # The hexdigest is attached so we get the hexdecimal format
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    # Hashing the one whole block
    def hash(self, block):
        encoded_block = hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()
        return encoded_block

    def is_blockchain_valid(self, chain):
        # Starting the check up from the first block
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            # First validation: Check if the previous hash of the current block is equal to the hash of the previos block
            if block["previous_hash"] != self.hash(previous_block):
                return False
            # Second validation: Check if the proof of work is valid
            previous_proof = previous_block["proof"]
            proof = block["proof"]
            hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != "0000":
                return False
            previous_block = block
            block_index += 1
        return True


# Mining a Blockchain

# Creating a app using Flask framework
app = Flask(__name__)

# Making an instance/object of Blockchain defined class
blockchain = Blockchain()


# Setting up routes

# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_hash = blockchain.hash(previous_block)
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    # New block created
    block = blockchain.create_block(proof, previous_hash)
    current_hash = blockchain.hash(block)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'hash': current_hash,
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200


# Get the whole blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }
    return jsonify(response), 200


# Check if the Blockchain is valid
@app.route('/get_validation', methods=['GET'])
def get_validation():
    if (blockchain.is_blockchain_valid(blockchain.chain)):
        response = {"message": "Valid"}
    else:
        response = {"message": "Invalid"}
    return jsonify(response), 200


# Running the app
if __name__ == '__main__':
    app.run(port=5000)
