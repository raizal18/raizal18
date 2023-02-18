import pandas  as pd
import json
import gradio as gr

import blockchain as _blockchain

blockchain = _blockchain.Blockchain()

def mine_block(data: str):
    if not blockchain.is_chain_valid():
        return "Not Valid"
    block = blockchain.mine_block(data=data)

    return block

def get_blockchain():
    if not blockchain.is_chain_valid():
        return "The blockchain is invalid"
    chain = blockchain.chain
    return chain
def is_blockchain_valid():
    if not blockchain.is_chain_valid():
        return "The blockchain is invalid"

    return blockchain.is_chain_valid()

def previous_block():
    if not blockchain.is_chain_valid():
        return "The blockchain is invalid"
        
    return blockchain.get_previous_block()

for i in range(0,5):
    block = mine_block(str(i+1))

bch = get_blockchain()
df = pd.DataFrame(bch)







