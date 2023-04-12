import json
import os
import pandas as pd
import fastapi as _fastapi
import uvicorn
import pickle
from datetime import datetime, timedelta
from typing import Union
import requests
import requests_oauthlib
from fastapi import Depends, FastAPI, HTTPException, status, UploadFile,File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

client = FastAPI()

@client.get('/blockchain/')
def get_chain():
    with open('cloud/chain.pkl','rb') as f:
        bc_obj = pickle.load(f)
        f.close()
    return bc_obj.chain
@client.post("/add_new_data_req/")
def add_new_data_req(data:str) -> str:
    with open('cloud/chain.pkl','rb') as f:
        bc_obj = pickle.load(f)
        bc_obj.mine_block(data)

    return bc_obj.chain
@client.post("/upload_images/")
def upload_image(data: str,file: UploadFile = File(...)):
    try:
        contents = file.file.read()

        with open(os.path.join('cloud','cloudstore',file.filename), 'wb') as f:
            f.write(contents)
        with open(os.path.join('localnet',file.filename), 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    with open('cloud/req.json', 'w', encoding='utf-8') as f:
        json.dump(data+f' Image : {file.filename}', f, ensure_ascii=False, indent=4)
    with open('cloud/uploadList.json', 'w', encoding='utf-8') as g:
        json.dump(f'Image:{file.filename}', g, ensure_ascii=False, indent=4)

    return data+f' image: {file.filename}'

import uvicorn 
if __name__ == '__main__':
    uvicorn.run('simulator_config:client', host = '127.0.0.1',
                port = 8001, log_level="info", reload = True)
