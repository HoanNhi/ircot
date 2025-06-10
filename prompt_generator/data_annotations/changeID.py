import _jsonnet
import json

# Step 1: Evaluate and parse multihop_old.jsonnet using jsonnet
jsonnet_path = 'multihop_2.jsonnet'
multihop_json_str = _jsonnet.evaluate_file(jsonnet_path)
multihop_data = json.loads(multihop_json_str)
# with open('multihop_old.jsonnet', 'r', encoding='utf-8') as f:
#     multihop_data = json.load(f)

# Step 2: Load the JSONL file and create a mapping
jsonl_path = '/processed_data/multihop/Original_MultiHopRAG_hotpot.jsonl'
question_text_to_id = {}

with open(jsonl_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        question_text = obj['question_text'].strip()
        question_id = obj['question_id']
        question_text_to_id[question_text] = question_id

# Step 3: Replace question_ids in the evaluated JSON data
updated = 0
for item in multihop_data:
    qt = item['question_text'].strip()
    if qt in question_text_to_id:
        item['question_id'] = question_text_to_id[qt]
        updated += 1
    else:
        print(f"Warning: question_text not found in JSONL: '{qt}'")

print(f"Updated {updated} entries.")

# Step 4: Dump the updated data back as JSON
output_path = 'multihop_wrong.jsonnet'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(multihop_data, f, indent=4, ensure_ascii=False)
