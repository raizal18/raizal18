import requests
import requests_oauthlib
from requests.exceptions import ConnectionError
from fastapi import Depends, FastAPI, HTTPException, status
import pandas as pd

# Authorization data

client = FastAPI()
import base64
import requests

username = 'admin'
password = 'password'
consumer_key = 'ggczWttBWlTjXCEtk3Yie_WJGEIa'
consumer_secret = 'uuzPjjJykiuuLfHkfgSdXLV98Ciga'
consumer_key_secret = consumer_key+":"+consumer_secret
consumer_key_secret_enc = base64.b64encode(consumer_key_secret.encode()).decode()

# Your decoded key will be something like:
#zzRjettzNUJXbFRqWENuuGszWWllX1iiR0VJYTpRelBLZkp5a2l2V0xmSGtmZ1NkWExWzzhDaWdh


headersAuth = {
    'Authorization': 'Basic '+ str(consumer_key_secret_enc),
}

data = {
  'grant_type': 'password',
  'username': username,
  'password': password
}

## Authentication request

response = requests.post('http://127.0.0.1:8000/token', headers=headersAuth, data=data, verify=True)
j = response.json()

try:
    ac = j['access_token']

    endpoint_url = "http://127.0.0.1:8000/blockchain/"

    headers = {
        "Authorization": f"Bearer {ac}"
    }

    try:

        response = requests.get(endpoint_url, headers=headers)
        print(response.json())
        
    except ConnectionError as e:

        print("Server Not Running")
except:
    response = 'Creditional invalid'

