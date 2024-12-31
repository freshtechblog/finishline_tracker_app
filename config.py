import json

def load_config(file_path='config.json'):
    """Load the configuration using a json file

    Args:
        file_path (str, optional): Filepath for the json. Defaults to 'config.json'.

    Returns:
        _type_: returns the json object loaded
    """
    with open(file_path, 'r') as config_file:
        return json.load(config_file)


config = load_config()
