import simpy 
import requests
import random
import numpy as np

class Simulator:
    def __init__(self, env, agend, process) -> None:
        self._upsream_band = 33
        self._downstream_band = 20
        self._memory_ = 4
        self.cpu_ability = [4030, 8050]
        self.delay = 7
        self.chain_instruction = 6
        self.power = [1.4, 20]
        self.number_shards = [100, 200, 300, 400]
        self.number_nodes = [250, 500, 750, 1000]
        self.metric = ["Throughput", "user-latency"]
        self.environment = env
        self.agend = agend
        self.process = process

    def config_environment(self):
        env = self.environment
        pass

    def set_param(self):
        pass
    
    def run_simulation(self):
        pass
    
    def early_stop(self):
        pass
    
    def upload_result(self):
        pass
    def process(self):
        pass
    def __getattribute__(self, __name: str) -> Any:
        pass
    





