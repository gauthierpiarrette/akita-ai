import json


def load_model_config(file_path: str):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Model configuration file not found: {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the model configuration file: {file_path}")
        return {}
