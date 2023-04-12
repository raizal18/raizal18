import simpy
import requests
import json
import numpy as np
from typing import List, Tuple, Dict
import time
import random
import math
import socket
import requests_oauthlib 
import uvicorn
import numpy as np
def run_simulator():
    env = simpy.Environment()
    NUMBEROFNODES = [250, 500, 750, 1000]

    maxShards = 200
    delay = 148



    def simulate(nodevalue, port:int = 8001,maxshard = 200, delay:float= 148):
        
        if type(nodevalue) == list:
            for i in nodevalue:
                
                host = socket.gethostbyname('localhost')
                port = port
                url = f'http://{host}:{port}/blockchain/'
                req = requests.get(url)
                # yield len(req.json())
                time.sleep(5)
                print(f'number of active nodes {i}: maxshard {maxshard} :time delay {((i*len(req.json()))/(delay+maxshard))+ np.random.rand()} ms')
                url = f'http://{host}:{port}/add_new_data_req/'
                da = requests.post(url,data = f"SimulationData 1 :{port}")
                persecond = i/((i*len(req.json()))/delay)
                yield [(i*len(req.json()))/delay,i/((i*len(req.json()))/delay),(len(req.json())*(5+np.random.rand()))+((i*len(req.json()))/delay),((((i*len(req.json()))/delay)/(maxshard+len(req.json())))*10)*(1+np.random.rand())]


    simOBJ = simulate(NUMBEROFNODES)




    val = []
    for ins in simOBJ:
        val.append(ins)
    # tps 
    # For max shards of 200
    env.process(simOBJ)

    nodethrouput = [i[2] for i in val]
    userlat_node = [i[3] for i in val]

    diffshard = [100, 200, 300, 400];

    thp = []
    laten = []
    for shar in diffshard:

        simOBJ = simulate(NUMBEROFNODES,maxshard=shar)
        val = []
        for ins in simOBJ:
            val.append(ins)
        # tps 
        # For max shards of 200
        laten.append([shar/i[0] for i in val])
        throuputNode = [(i[2]+i[0])/(shar*0.01) for i in val]
        thp.append(throuputNode)

    thput = np.array(thp)
    cth = np.sum(thput,axis=1)
    lat = [i[0]*100 for i in laten]
    return cth ,nodethrouput, lat, userlat_node ,NUMBEROFNODES , diffshard