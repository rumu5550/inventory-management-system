import json
import os

class JsonStore:
    """Handles persistence of data using JSON files."""
    def __init__(self, filename):
        self.filename = f"data/{filename}.json"
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        if not os.path.exists(self.filename):
            self.save([])

    def save(self, data):
        """Saves a list of dictionaries to the JSON file."""
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load(self):
        """Loads a list of dictionaries from the JSON file."""
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            return []
