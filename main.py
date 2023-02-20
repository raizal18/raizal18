import fastapi as _fastapi
import blockchain as _blockchain
import uvicorn
import json
# from fastapi import Depends, FastAPI
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
blockchain = _blockchain.Blockchain()
app = _fastapi.FastAPI()

# token_url = "service_that_will_generate_token/token"
# oauth2 = OAuth2PasswordBearer(tokenUrl=token_url)

# @app.post("/token")
# async def gen_token_to_login(input_data : OAuth2PasswordRequestForm = Depends()):
#    # check if user exists in db if required by username and hashed password
#    # we can also compute a JWT token instead of returning access_token as the username
#     return {"access_token": input_data.username, "token_type": "bearer"}

# endpoint to mine a block
@app.post("/mine_block/")
def mine_block(data: str):
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")
    block = blockchain.mine_block(data=data)
    return block


# endpoint to return the blockchain
@app.get("/blockchain/")
def get_blockchain():
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")
    chain = blockchain.chain
    with open('cloud/data.json', 'w', encoding='utf-8') as f:
        json.dump(chain, f, ensure_ascii=False, indent=4)
    return chain

# endpoint to see if the chain is valid
@app.get("/validate/")
def is_blockchain_valid():
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")

    return blockchain.is_chain_valid()


# endpoint to return the last block
@app.get("/blockchain/last/")
def previous_block():
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")
        
    return blockchain.get_previous_block()
@app.get('/request/')
def get_request() -> str:
    with open('cloud/req.json') as f:
        data = json.load(f)
    blockchain.req = data
    return data 

    
@app.get('/request_logging/')
def request_logging(aprovel:bool):
    if aprovel == True:
        block = mine_block(blockchain.req)
        return "Aproved"
    else:
        return "not Aproved"


if __name__ == '__main__':
    uvicorn.run(app)

# Authentication Oauth2.0
# Kalfka # Hpose # raft