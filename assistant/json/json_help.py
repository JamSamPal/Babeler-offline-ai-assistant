import json

def save_memory(path:str, memory_list:list[str]):
    with open(path, "w") as f:
        json.dump(memory_list, f, indent=2)

def load_config(path:str):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_config_value(key:str, value:str, path:str):
    try:
        with open(path, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {}

    config[key] = value
    with open(path, "w") as f:
        json.dump(config, f, indent=2)