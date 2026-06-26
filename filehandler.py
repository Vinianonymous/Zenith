import json


class fileHandler:
    def read(self, filepath: str):
        try:
            with open(filepath, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            with open(filepath, "w") as file:
                json.dump([], file)
            return []

    def write(self, filepath: str, data):
        with open(filepath, "w") as file:
            json.dump(data, file)
