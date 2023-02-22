import blockchain as _blockchain
idx = 0
blockchain = _blockchain.Blockchain()
for s in sample:
    idx = idx + 1
    print(idx)
    blockchain.mine_block(data = str(s))

import pickle 

with open('cloud/chain.pkl', 'wb') as f: 
    pickle.dump(blockchain, f)
    f.close()