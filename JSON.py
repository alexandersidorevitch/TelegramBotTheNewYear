import json


def read_from_json(file_name: str) -> dict:
    with open(file_name, 'r') as file:
        return json.load(file)


def write_to_json(file_name: str, data: dict) -> None:
    with open(file_name, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
