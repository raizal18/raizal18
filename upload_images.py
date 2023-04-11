import os
import numpy as np
import requests

from fastapi import File, UploadFile,FastAPI

app = FastAPI()
@app.post("/upload")
def upload(patient,file: UploadFile = File(...)):
    try:
        contents = file.file.read()

        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}

import uvicorn 
if __name__ == '__main__':

    uvicorn.run('upload_images:app', host = '127.0.0.1',
                port = 8090, log_level="info", reload = True)
