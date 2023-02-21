import json
import pandas as pd
import fastapi as _fastapi
import uvicorn

client = _fastapi.FastAPI()
@client.get('/blockchain/')
def get_chain():
    with open('cloud/data.json') as f:
        data = json.load(f)
    return data
@client.post("/add_new_data_req/")
def add_new_data_req(data:str) -> str:
    with open('cloud/req.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return data

# @client.get('/Updated Chain block/')
# def get_chain_pd():
#     with open('cloud/data.json') as f:
#         data = json.load(f)
#     return pd.DataFrame(data)

if __name__ == '__main__':
    uvicorn.run('run_client_api:client',  port=8080, log_level="info", reload = True)
