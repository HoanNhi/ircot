import json
import random

# Paths to your files
random.seed(210114)
input_path = "multihop.jsonnet"

with open(input_path, "r") as f:
    data = json.load(f)

key = []
sampling = dict()
for instance in data:
    key.append(instance["question_id"])

for i in range(3):
    sampling_keys = random.sample(key, 15)
    sampling[f"{i+1}"] = sampling_keys
print(sampling)