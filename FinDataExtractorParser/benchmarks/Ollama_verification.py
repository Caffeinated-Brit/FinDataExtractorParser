# doing this for now due to merge conflicts and not enough time to integrate everything before our client meeting

import difflib
import json
from concurrent.futures import ThreadPoolExecutor
from exceptiongroup import catch

from AI import Ollama
from configs import configLoader, ai_methods

# This runs the llm chosen multiple times to check that the output is consistent
def verify_similar_outputs(reruns, threshold, prompt):
    outputs = Ollama.run_parallel_requests_with_schema(reruns, prompt)
    print("Checking similarity ratio of the following outputs.\n")

    num_outputs = len(outputs)
    total_similarity = [0.0] * num_outputs
    comparison_counts = [0] * num_outputs

    # Compare each output against all others
    for i in range(num_outputs):
        norm_i = normalize_json_string(outputs[i][0])
        for j in range(num_outputs):
            if i == j:
                continue
            norm_j = normalize_json_string(outputs[j][0])
            similarity = difflib.SequenceMatcher(None, norm_i, norm_j).ratio()
            print(f"Similarity between {i} and {j}: {similarity:.2f}")

            total_similarity[i] += similarity
            comparison_counts[i] += 1

    average_similarity = [
        total / count if count > 0 else 0.0
        for total, count in zip(total_similarity, comparison_counts)
    ]

    print()
    for i, avg in enumerate(average_similarity):
        print(f"Average similarity for output {i}: {avg:.2f}")

    highest_similarity = max(average_similarity)

    # Pick the first output with the highest average similarity
    best_index = average_similarity.index(highest_similarity)

    if average_similarity[best_index] > threshold:
        print(f"\nReturning output {best_index} (avg similarity: {average_similarity[best_index]:.2f})")
        return outputs[best_index]

    print("\nNo sufficiently similar outputs found, defaulting to first.")
    return outputs[0]

def normalize_json_string(text):
    try:
        if text.startswith("```json"):
            lines = text.strip().splitlines()
            text = "\n".join(lines[1:-1])

        parsed = json.loads(text)
        return json.dumps(parsed, sort_keys=True)
    except Exception as e:
        print("⚠️ Could not normalize output:", e)
        return text

def ollama_verification(prompt):
    config = configLoader.load_config()
    selected_ai = config["ai"]
    selected_reruns = config["reruns"]
    threshold = config["threshold"]

    # if selected_ai in ai_methods:
        # Past this point elapsed_time and generated_tokens are not used they are only for benchmarking
    structured_data, elapsed_time, generated_tokens = verify_similar_outputs(selected_reruns, threshold, prompt)
    # else:
        # raise ValueError(f"Unknown AI method: {selected_ai}")

    return structured_data, elapsed_time, generated_tokens

if __name__ == "__main__":
    print(ollama_verification("give me 3 space facts"))