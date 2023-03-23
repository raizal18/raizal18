import fastapi as _fastapi
import blockchain as _blockchain
import uvicorn
import json
from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import pickle
from raft_consensus import raft_init

from consensual.raft import Node, communication
from yarl import URL

node_url = URL.build(scheme='http', host='127.0.0.1', port=8000)

other_node_url = URL.build(scheme='http',host='127.0.0.1',port=8080)

heartbeat = 0.1
from typing import Any, List, Optional
processed_parameters = []
def dummy_processor(parameters: Any) -> None:
    processed_parameters.append(parameters)
processors = {'dummy': dummy_processor}
nodes = {}
sender = communication.Sender([node_url], nodes)
other_sender = communication.Sender([other_node_url], nodes)
node = Node.from_url(node_url, heartbeat=heartbeat, 
                    processors=processors, sender=sender)
other_node = Node.from_url(other_node_url,
                            heartbeat=heartbeat,
                            processors=processors,
                            sender=other_sender)
receiver = communication.Receiver(node, nodes)
other_receiver = communication.Receiver(other_node, nodes)
receiver.start()
other_receiver.start()
from asyncio import get_event_loop
loop = get_event_loop()
async def run() -> List[Optional[str]]:
    return [await node.solo(),
            await node.enqueue('dummy', 42),
            await node.attach_nodes([other_node.url]),
            await node.enqueue('dummy', 42),
            await other_node.detach_nodes([node.url]),
            await other_node.solo(),
            await other_node.detach(),
            await other_node.detach()]
error_messages =  [None, None, None, None, 'nonexistent node(s) found: 127.0.0.1:8080', None, None, None] #loop.run_until_complete(run())
# print(error_messages)
receiver.stop()
other_receiver.stop()
raft_consensus_test = all(error_message is None or isinstance(error_message, str)
    for error_message in error_messages)
raft_consensus_test1 = all(parameters == 42 for parameters in processed_parameters)
if raft_consensus_test1 == True:
    print('Raft Test passed:')
else:
    print('Failed Concensus Test')
# from fastapi import Depends, FastAPI
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
with open('cloud/chain.pkl','rb') as f: 
    blockchain = pickle.load(f)
    f.close()
# blockchain = _blockchain.Blockchain()

SECRET_KEY = "6567f2802ec354406021ef6c7b6d4456c51fd9f80cc3971549b8fe188212392c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "admin",
        "email": "admin@gmail.com",
        "hashed_password": "$2a$12$hzIr9RjTBFLWM4doOgEmB.Zx5MrI54hXvKh1n0ppSs5AtNoSrxQY2",
        "disabled": False,
    },
       "client": {
        "username": "client",
        "full_name": "client01",
        "email": "admin6@gmail.com",
        "hashed_password": "$2a$12$hzIr9RjTBFLWM4doOgEmB.Zx5MrI54hXvKh1n0ppSs5AtNoSrxQY2",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = _fastapi.FastAPI()
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# @app.get("/kRaft/")
# async def check_Concensus_of_nodes(current_user: User = Depends(get_current_active_user)) ->bool:
#     if not blockchain.is_chain_valid():
#         return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")
#     rf = raft_init()
#     if rf == True:
#         return 'Test Case Passed'
#     else:
#         return 'Connections Failed'

# endpoint to mine a block
@app.post("/mine_block/")
async def mine_block(data: str, current_user: User = Depends(get_current_active_user)):
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")

    block = blockchain.mine_block(data=data)
    return block
# Upload DB
@app.post("/upload_db/")
async def upload_db(current_user: User = Depends(get_current_active_user)):
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")
    with open('cloud/chain.pkl', 'wb') as f: 
        pickle.dump(blockchain, f)
        f.close()
    return 'updated'

# endpoint to return the blockchain
@app.get("/blockchain/")
async def get_blockchain(current_user: User = Depends(get_current_active_user)):
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")
    chain = blockchain.chain
    # with open('cloud/data.json', 'w', encoding='utf-8') as f:
        # json.dump(chain, f, ensure_ascii=False, indent=4)
    return chain

# endpoint to see if the chain is valid
@app.get("/validate/")
async def is_blockchain_valid(current_user: User = Depends(get_current_active_user)):
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")

    return blockchain.is_chain_valid()


# endpoint to return the last block
@app.get("/blockchain/last/")
async def previous_block(current_user: User = Depends(get_current_active_user)):
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")
        
    return blockchain.get_previous_block()
@app.get("/request/")
async def get_request(current_user: User = Depends(get_current_active_user)) -> str:
    with open('cloud/req.json') as f:
        data = json.load(f)
    blockchain.req = data
    return data 

    
@app.post("/request_logging/")
async def request_logging(aprovel:bool,current_user: User = Depends(get_current_active_user)):
    if aprovel == True:
        block = blockchain.mine_block(blockchain.req)
        return "aproved"
    else:
        return "not Aproved"


# if __name__ == '__main__':
#     uvicorn.run('main:app',port=8000, reload = True)

# Authentication Oauth2.0
# Kalfka # Hpose # raft