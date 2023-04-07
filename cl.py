import uvicorn 
if __name__ == '__main__':

    uvicorn.run('run_client_api:client', host = '127.0.0.1',
                port = 8081, log_level="info", reload = True)
