import json
import os


with open("annual copy.json", "r") as f:
    data = f.read()

data = json.loads(data)
print(data)
print("over?")

# with open("annual_c.json", "w" ) as f:
#     data


