import json

def read_config(config_filename: str):
    with open(config_filename, 'r') as f:
        return json.load(f)