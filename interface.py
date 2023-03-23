import requests
import requests_oauthlib
from requests.exceptions import ConnectionError

ac = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyYXN1IiwiZXhwIjoxNjc5NTU1MTk2fQ.Ql2cfpiR6qSKHadGMOzugydCXuDxDTsOISUyVnc4JyU"

endpoint_url = "http://127.0.0.1:8000/blockchain/"

headers = {
    "Authorization": f"Bearer {ac}"
}

try:

    response = requests.get(endpoint_url, headers=headers)
    print(response.json())

except ConnectionError as e:

    print("Server Not Running")