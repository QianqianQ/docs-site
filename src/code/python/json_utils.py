import json


def read_json(file_path: str):
    """Read a JSON file and return its contents as a Python dict.

    Example:
    print(read_json("data.json"))
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def write_json(file_path: str, data):
    """Write a Python dict to a JSON file.

    Example:
    data = {"name": "John", "age": 30}
    write_json("data.json", data)
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
