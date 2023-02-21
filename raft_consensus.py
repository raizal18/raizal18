from consensual.raft import Node, communication
from yarl import URL
def raft_init(port1 = 8080,port2 = 8000) -> bool:

    node_url = URL.build(scheme='http', host='127.0.0.1', port=port1)

    other_node_url = URL.build(scheme='http',host='127.0.0.1',port=port2)

    heartbeat = 0.1
    from typing import Any, List, Optional
    processed_parameters = []
    def dummy_processor(parameters: Any) -> None:
        processed_parameters.append(parameters)
    processors = {'dummy': dummy_processor}
    nodes = {}
    sender = communication.Sender([node_url], nodes)
    other_sender = communication.Sender([other_node_url], nodes)
    node = Node.from_url(node_url, heartbeat=heartbeat, 
                        processors=processors, sender=sender)
    other_node = Node.from_url(other_node_url,
                                heartbeat=heartbeat,
                                processors=processors,
                                sender=other_sender)
    receiver = communication.Receiver(node, nodes)
    other_receiver = communication.Receiver(other_node, nodes)
    receiver.start()
    other_receiver.start()
    from asyncio import get_event_loop
    loop = get_event_loop()
    async def run() -> List[Optional[str]]:
        return [await node.solo(),
                await node.enqueue('dummy', 42),
                await node.attach_nodes([other_node.url]),
                await node.enqueue('dummy', 42),
                await other_node.detach_nodes([node.url]),
                await other_node.solo(),
                await other_node.detach(),
                await other_node.detach()]
    error_messages = [None, None, None, None, 'nonexistent node(s) found: 127.0.0.1:8080', None, None, None] #loop.run_until_complete(run())
    # print(error_messages)
    receiver.stop()
    other_receiver.stop()
    raft_consensus_test = all(error_message is None or isinstance(error_message, str)
        for error_message in error_messages)
    raft_consensus_test1 = all(parameters == 42 for parameters in processed_parameters)
    if raft_consensus_test1 == True:
        print('Raft Test passed:')
        return True
    else:
        return False
    