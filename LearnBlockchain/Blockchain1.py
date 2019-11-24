
import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4
from flask import Flask


class Blockchain(object):
    def ___init___(self):
        self.chain = []
        self.current_transactions = []

        # "genesis" block - has no predecessor
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        # create new block
        # proof: <int> 
        # previous_hash: optional string hash of previous block
        # return dictionary of new block
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.current_transactions,
            "proof":proof,
            "previous_hash":previous_hash or self.hash(self.chain[-1])
        }
        
        # reset current list of transactions
        self.current_transactions = []

        # add block to chain
        self.chain.append(block)
        return block
    
    def new_transaction(self, sender, recipient, amount):
        # sender: address of the sender
        # recipient: address of recipient
        # amount: amount
        # return index of block that holds transaction

        # Add new transaction
        self.current_transactions.append({
            "sender":sender,
            "recipient:recipient,
            "amount":amount,
        })

        # return index of next block, where transaction is added
        return self.last_block["index"] + 1

    @property #(???)
    def last_block(self):
        # return last block in chain
        return self.chain[-1]

    @staticmethod #(???)
    def hash(block):
        # hashes a block: hard to find, easy to verify, uses info from previous
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self,last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof +=1 # what does this do?
        return proof

    @staticmethod #(???)
    def valid_proof(last_proof, proof):
        # validates proof
        # last proof: previous proof
        # proof: current proof
        # return: true if correct, false if not

        guess = f"{last_proof}{proof}".encode() # don't know this syntax
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000" # arbitrary constraint for validity


# instantiate node (???)
app = Flask(__name__)

# globally unique address for node
node_identifier = str(uuid4()).replace("-","")

# instantiate blockchain
blockchain = Blockchain()

@app.route("/mine", methods=["GET"])
def mine():
    return "we'll mine a new Block"

@app.route("/transactions/new", methods = ["POST"])
def new_transaction():
    return "we'll add a new transaction"

