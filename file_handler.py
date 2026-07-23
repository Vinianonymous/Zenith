from json import load, dump

def read(self, filepath: str):
    try:
        with open(filepath, "r") as file:
            return load(file)
    except FileNotFoundError:
        print("File Not found.")


def write(self, filepath: str, data):
    with open(filepath, "w") as file:
        dump(data, file)

def load_tasks():
    try:
        with open("engager.json", "r") as f:
            return load(f)
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open("engager.json", "w") as f:
        dump(tasks, f)
