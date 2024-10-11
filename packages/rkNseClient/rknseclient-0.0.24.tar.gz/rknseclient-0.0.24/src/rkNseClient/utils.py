import re


def fix_invalid_json_getIndicesWeightage(data: str) -> str:
    # Step 1: Remove trailing commas
    data = data.replace("},]", "}]")
    # Step 2: Add missing quotes to the keys (label, file)
    data = re.sub(r'(\w+)\s*:', r'"\1":', data)
    # Step 3: Remove the last unsupported object
    data = data.split("}]},{")[0]
    data += "}]}"
    return data