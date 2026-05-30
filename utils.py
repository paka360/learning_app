import json 
import os


def load_json(file_path):
    """Function which loads data into the app"""

    if not os.path.exists(file_path):
        return[]
    
    with open(file_path, "r") as f:
        return json.load(f)
    

def save_json(file_path, data):
    """Function which saves data from the app"""

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


