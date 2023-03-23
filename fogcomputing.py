import simpy
from leaf.application import Task
from leaf.infrastructure import Node
from leaf.power import PowerModelNode, PowerMeter

# Processes modify the model during the simulation
def place_task_after_2_seconds(env, node, task):
    """Waits for 2 seconds and places a task on a node."""
    yield env.timeout(2)
    task.allocate(node)

node = Node("node1", cu=100, power_model=PowerModelNode(max_power=30, static_power=10))
task = Task(cu=100)
power_meter = PowerMeter(node, callback=lambda m: print(f"{env.now}: Node consumes {int(m)}W"))

env = simpy.Environment()  
# register our task placement process
env.process(place_task_after_2_seconds(env, node, task))
# register power metering process (provided by LEAF)
env.process(power_meter.run(env))
env.run(until=100)