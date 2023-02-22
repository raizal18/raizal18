import json2html
import json
import os

import json

# Open the JSON file and read it in chunks
with open('trans copy.json') as f:
        data = json.load(f)

sample  = data[0:200]

