import json


def read_from_json(file_name: str) -> dict:
    with open(file_name, 'r', encoding='ISO-8859-1') as file:
        return json.load(file)


def write_to_json(file_name: str, data: dict) -> None:
    with open(file_name, 'w', encoding='ISO-8859-1') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
