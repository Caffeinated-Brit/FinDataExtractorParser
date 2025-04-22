from general_schema_basic import FinancialData
import json

data = FinancialData.model_json_schema()

output_file_path = "small_schema.json"
with open(output_file_path, "w") as file:
    json.dump(data, file, indent=4)
    print("Created schema output json test at: " + output_file_path)

print(data)