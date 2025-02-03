import json
import re

def fix_truncated_json(ai_output):
    # Attempts to parse JSON output from AI, auto-fixing truncated or extra text issues.
    ai_output = extract_json(ai_output)  # Extract just the JSON part
    if not ai_output:
        print("No valid JSON detected in AI output.")
        return None

    try:
        return json.loads(ai_output)
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}\nAttempting auto-fix...")

        # Attempt to auto-fix by finding the last valid closing bracket
        last_curly = ai_output.rfind("}")
        last_square = ai_output.rfind("]")

        last_valid = max(last_curly, last_square)
        if last_valid == -1:
            print("No valid JSON structure found.")
            return None

        fixed_json = ai_output[:last_valid+1]  # Trim to the last valid bracket

        try:
            return json.loads(fixed_json)
        except json.JSONDecodeError:
            print("Still invalid JSON after truncation.")
            return None

def extract_json(ai_output):
    # Extracts only the JSON portion from a mixed AI output containing explanations and JSON.
    json_match = re.search(r'(\[.*\]|\{.*\})', ai_output, re.DOTALL)
    if json_match:
        return json_match.group(1)
    return None