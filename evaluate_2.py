import json
import argparse
from metrics.drop_answer_em_f1 import DropAnswerEmAndF1


def evaluate(prediction_file: str, ground_truth_file: str):
    # Load prediction and ground truth
    with open(prediction_file, 'r', encoding='utf-8') as pred_f:
        predictions = json.load(pred_f)

    with open(ground_truth_file, 'r', encoding='utf-8') as gt_f:
        ground_truths = json.load(gt_f)

    metric = DropAnswerEmAndF1()

    # Loop through all prediction entries
    for qid, pred_answer in predictions.items():
        if qid not in ground_truths:
            print(f"Warning: {qid} not found in ground truth. Skipping.")
            continue
        gt_answers = ground_truths[qid]
        metric([pred_answer], [gt_answers])

    # Get final metric
    results = metric.get_metric()
    print("Evaluation Results:")
    for key, value in results.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", type=str, required=True, help="Path to the prediction JSON file")
    parser.add_argument("--ground_truth", type=str, required=True, help="Path to the ground truth JSON file")
    args = parser.parse_args()

    evaluate(args.predictions, args.ground_truth)
