import configparser
import numpy as np
import json
from collections import defaultdict
from difflib import SequenceMatcher
import time

from FinDataExtractorParser.parse import fullParse

TEST_AMOUNT = 3
FILE_PATH = "C:/Users/lukas/Desktop/Capstone/FinDataExtractorParser/FinDataExtractorParser/examplePDFs/fromCameron/2021_2_Statement_removed.pdf"


def compare_json_outputs(json_outputs):
    """
    Compare a list of JSON outputs and measure consistency for each field.

    Args:
        json_outputs (list of dict): List of extracted JSON outputs.

    Returns:
        dict: Consistency scores for each field.
        float: Overall consistency score.
    """
    num_runs = len(json_outputs)
    field_values = defaultdict(list)

    # Extract all fields dynamically
    for output in json_outputs:
        def flatten_json(d, parent_key=''):
            """Recursively flatten nested JSON fields."""
            items = {}
            for k, v in d.items():
                new_key = f"{parent_key}.{k}" if parent_key else k
                if isinstance(v, dict):
                    items.update(flatten_json(v, new_key))
                elif isinstance(v, list):
                    for i, item in enumerate(v):
                        if isinstance(item, dict):
                            items.update(flatten_json(item, f"{new_key}[{i}]"))
                        else:
                            items[f"{new_key}[{i}]"] = item
                else:
                    items[new_key] = v
            return items

        flat_output = flatten_json(output)
        for key, value in flat_output.items():
            field_values[key].append(value)

    # Calculate consistency metrics
    consistency_scores = {}

    for field, values in field_values.items():
        # Numeric consistency (Variance-based)
        if all(isinstance(v, (int, float)) for v in values):
            if len(values) < 2:
                # Not enough data for comparison
                consistency_scores[field] = 1.0
            else:
                variance = np.var(values)
                consistency_scores[field] = 1 - (variance / (np.mean(values) + 1e-6))  # Normalize variance

        # Text consistency (Levenshtein similarity)
        elif all(isinstance(v, str) for v in values):
            if len(values) < 2:
                # Not enough data for comparison
                consistency_scores[field] = 1.0
            else:
                similarity_scores = [
                    SequenceMatcher(None, values[i], values[i + 1]).ratio()
                    for i in range(len(values) - 1)
                ]
                avg_similarity = np.mean(similarity_scores)
                consistency_scores[field] = avg_similarity

        # Other data types (booleans, None, mixed types) - Count exact matches
        else:
            if len(values) < 2:
                # Not enough data for comparison
                consistency_scores[field] = 1.0
            else:
                exact_match_ratio = sum(values.count(values[0]) for v in values) / num_runs
                consistency_scores[field] = exact_match_ratio

    # Compute overall consistency score
    overall_consistency = np.mean(list(consistency_scores.values()))

    return consistency_scores, overall_consistency

start_time = time.time()
# Initialize json_outputs
json_outputs = []

# Populate json_outputs by running parsing multiple times
for i in range(TEST_AMOUNT):
    json_outputs.append(fullParse(FILE_PATH))

# Call compare_json_outputs to determine consistency
field_scores, overall_score = compare_json_outputs(json_outputs)

# Print results
# print(f"Field Consistency Scores:\n{json.dumps(field_scores, indent=2)}")
# print(f"Overall Consistency Score: {overall_score:.2f}")

config = configparser.ConfigParser()
config.read("config.ini")
selected_parser = config.get("Parser", "method", fallback="pdfPlumber")
selected_ai = config.get("AI", "method", fallback="Ollama")

endTime = time.time() - start_time

output_data = {
    "Test_Data": {
        "File_Path": FILE_PATH,
        "Number_of_Runs": TEST_AMOUNT,
        "Time_Elapsed": endTime,
        "Parser_Used": selected_parser,
        "AI_Used": selected_ai,
        "Disclaimer": "This only checks the consistency of the JSON output. It does not check the accuracy of the data."
    },
    "Field_Consistency_Scores": field_scores,
    "Overall_Consistency_Score": round(overall_score, 4)
}

with open("consistencyBenchmarkOutput.json", "w") as f:
    json.dump(output_data, f, indent=2)

# Print confirmation
print("Consistency benchmark results saved to consistencyBenchmarkOutput.json")