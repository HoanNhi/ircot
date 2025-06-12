import json
from collections import defaultdict

# File paths
question_file = '/media/thomas/ircot/raw_data/MultiHopRAG.json'
ground_truth_file = 'ground_truth__multihop_to_multihop__test_subsampled.json'
prediction_file = 'prediction__multihop_to_multihop__test_subsampled.json'

# Output base path (you can adjust this)
output_dir = './'

# Step 1: Read questions and create mapping
with open(question_file, 'r') as f:
    questions = json.load(f)

question_id_map = {}  # (query, question_type) -> question_id
id_to_type = {}       # question_id -> question_type
question_id = 1

for q in questions:
    key = (q['query'], q['question_type'])
    question_id_map[key] = str(question_id)
    id_to_type[str(question_id)] = q['question_type']
    question_id += 1

# Step 2: Read ground truth and prediction
with open(ground_truth_file, 'r') as f:
    ground_truth = json.load(f)

with open(prediction_file, 'r') as f:
    prediction = json.load(f)

# Step 3: Group answers by question_type
gt_by_type = defaultdict(dict)
pred_by_type = defaultdict(dict)

for qid, ans in ground_truth.items():
    q_type = id_to_type.get(qid)
    if q_type:
        gt_by_type[q_type][qid] = ans

for qid, ans in prediction.items():
    q_type = id_to_type.get(qid)
    if q_type:
        pred_by_type[q_type][qid] = ans

# Step 4: Write out files for each type
for q_type in gt_by_type:
    with open(f'{output_dir}ground_truth_{q_type}.json', 'w') as f:
        json.dump(gt_by_type[q_type], f, indent=2)

for q_type in pred_by_type:
    with open(f'{output_dir}prediction_{q_type}.json', 'w') as f:
        json.dump(pred_by_type[q_type], f, indent=2)

print("Done. Output files written by question_type.")
