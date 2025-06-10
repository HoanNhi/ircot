import json
import os
import re

# Paths to your files
input_path = "multihop_wrong.jsonnet"
passages_path = "/media/thomas/ircot/raw_data/passages.json"
output_path = "multihop.jsonnet"

# Load passages into a dictionary for quick lookup
with open(passages_path, "r", encoding="utf-8") as f:
    passages = json.load(f)
    title_to_first_sentence = {
        p["title"]: re.split(r'(?<=[.!?]) +', p["text"].strip())[0] for p in passages
    }

# Load input data
with open(input_path, "r", encoding="utf-8") as f:
    input_data = json.load(f)

# Replace text_substring with the first sentence from matching title
for item in input_data:
    for step in item.get("reasoning_steps", []):
        for para in step.get("paragraphs", []):
            title = para.get("title")
            if title in title_to_first_sentence:
                para["text_substring"] = title_to_first_sentence[title]

# Save the updated data
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(input_data, f, indent=2, ensure_ascii=False)

print(f"Updated data saved to {output_path}")
