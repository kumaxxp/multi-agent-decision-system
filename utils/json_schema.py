import json, jsonschema, pathlib

def validate_json_schema(payload: str, schema_path: str) -> dict:
    data = json.loads(payload)
    schema = json.loads(pathlib.Path(schema_path).read_text(encoding="utf-8"))
    jsonschema.validate(data, schema)
    return data
