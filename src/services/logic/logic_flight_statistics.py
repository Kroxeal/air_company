import json


def is_valid_json(content):
    try:
        json.loads(content)
        return True
    except json.JSONDecodeError:
        return False

