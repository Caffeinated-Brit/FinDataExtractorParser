#This will run the selected ai multiple times and output the most similar to the others
import difflib
import json
import sys

from AI import Vllm, OllamaVerification
from configs.ai_methods import ai_methods

def verify_similar_outputs(reruns, threshold, prompt, selected_ai, schema):
    #TODO: Make sure this works with vllm and make it work with schemas
    if "vllm" in selected_ai:
        if schema is not None:
            print(type(schema))
            outputs = Vllm.run_parallel_requests_with_schema(reruns, prompt, schema)
        else:
            outputs = Vllm.run_parallel_requests(reruns, prompt)
    elif "Ollama" in selected_ai:
        if schema is not None:
            print(type(schema))
            print("verification schema:" + schema)
            outputs = OllamaVerification.run_parallel_requests_with_schema(reruns, prompt, schema)
        else:
            outputs = OllamaVerification.run_parallel_requests(reruns, prompt)
    else:
        print(f"AI chosen \"{selected_ai}\" not eligible for verification, exiting.")
        sys.exit(1)

    print("Checking similarity ratio of the following outputs.\n")

    num_outputs = len(outputs)
    total_similarity = [0.0] * num_outputs
    comparison_counts = [0] * num_outputs

    # Compare each output against all others
    for i in range(num_outputs):
        norm_i = normalize_json_string(outputs[i])
        for j in range(num_outputs):
            if i == j:
                continue
            norm_j = normalize_json_string(outputs[j])
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

