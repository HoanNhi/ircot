import json
import pandas as pd 
import copy

path = r"C:\viettel\MultiHopRAG.json"
template_path = r"C:\viettel\template.json"
context_path = r"C:\viettel\context_template.json"
output_path = r"C:\viettel\MultiHopRAG_hotpot_tmp.jsonl"
with open(path, 'r') as file:
    df = json.load(file)['data']

dataset = []
with open(template_path, "r") as file:
    template = json.load(file)

with open(context_path, "r") as file:
    context = json.load(file)

for index, row in enumerate(df):
    instance = copy.deepcopy(template)
    # print(row['answer'])
    # break
    instance["question_id"] = str(index + 1)
    instance["question_text"] = row['query']
    instance["answers_objects"][0]['spans'].append(row['answer'])
    instance['contexts'] = []
    if "comparison" in row['question_type']:
        instance['type'] = "comparison"
    else:
        instance['type'] = "bridge"
    
    for idx, evidence in enumerate(row['evidence_list']):
        obj = context.copy()
        obj['title'] = evidence['title']
        obj['paragraph_text'] = evidence['fact']
        obj['idx'] = idx + 1
        instance['contexts'].append(obj)
    dataset.append(instance.copy())
    instance = None

with open(output_path, "w") as f:
    for record in dataset:
        f.write(json.dumps(record) + "\n")