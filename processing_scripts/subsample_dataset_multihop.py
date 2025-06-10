import argparse
import random
import time
import json
import os

from tqdm import tqdm

random.seed(210114)


def main():
    dev_sample = 100
    training_sample = 20

    base_dir = "processed_data/multihop"
    prompt_dir = "prompt_generator/data_annotations"
    original_dataset_path = os.path.join(base_dir, "Original_MultiHopRAG_hotpot.jsonl")
    multihop_path = os.path.join(prompt_dir, "multihop_wrong.jsonnet")
    annotated_output_path = os.path.join(base_dir, "train.jsonl")
    dev_output_path = os.path.join(base_dir, "dev_subsampled.jsonl")
    test_output_path = os.path.join(base_dir, "test_subsampled.jsonl")

    # Load original dataset (jsonl format: list of JSON objects per line)
    with open(original_dataset_path, "r") as f:
        original_data = [json.loads(line.strip()) for line in f if line.strip()]

    # Index original data by question_id
    original_data_dict = {item["question_id"]: item for item in original_data}

    # Load hotpotqa.json to get annotated question_ids
    with open(multihop_path, "r") as f:
        hotpotqa_data = json.load(f)
    annotated_ids = {item["question_id"] for item in hotpotqa_data}

    # Extract annotated objects and save them
    annotated_data = [original_data_dict[qid] for qid in annotated_ids if qid in original_data_dict]
    with open(annotated_output_path, "w") as f:
        for item in annotated_data:
            f.write(json.dumps(item) + "\n")

    # Prepare the rest of the dataset (excluding annotated question_ids)
    remaining_data = [item for item in original_data if item["question_id"] not in annotated_ids]

    # Shuffle the remaining data
    random.shuffle(remaining_data)

    # Sample dev and test sets
    dev_data = remaining_data[:dev_sample]
    test_data = remaining_data[dev_sample:dev_sample + (len(remaining_data) - dev_sample)]

    # Save dev and test sets
    with open(dev_output_path, "w") as f:
        for item in dev_data:
            f.write(json.dumps(item) + "\n")

    with open(test_output_path, "w") as f:
        for item in test_data:
            f.write(json.dumps(item) + "\n")

    print(f"Annotated (train): {len(annotated_data)}")
    print(f"Dev set size: {len(dev_data)}")
    print(f"Test set size: {len(test_data)}")


if __name__ == "__main__":
    main()
