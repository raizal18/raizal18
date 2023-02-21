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
    "rasu": {
        "username": "rasu",
        "full_name": "rasukrish",
        "email": "rasukrish6@gmail.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
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


if __name__ == '__main__':
    uvicorn.run('main:app',port=8000, reload = True)

# Authentication Oauth2.0
# Kalfka # Hpose # raft