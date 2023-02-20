from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn

token_url = "service_that_will_generate_token/token"
oauth2 = OAuth2PasswordBearer(tokenUrl=token_url)

app = FastAPI()

@app.post("/token")
async def gen_token_to_login(input_data : OAuth2PasswordRequestForm = Depends()):
   # check if user exists in db if required by username and hashed password
   # we can also compute a JWT token instead of returning access_token as the username
    return {"access_token": input_data.username, "token_type": "bearer"}

@app.get("/my_data/")
async def get_data(token: str = Depends(oauth2)):
    return [{"some_data_key":"some_data_value"}]

if __name__ == '__main__':
    uvicorn.run(app)