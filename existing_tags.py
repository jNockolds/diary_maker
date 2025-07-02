import json
import os
from bisect import insort

DATA_FOLDER = "diary_data"
FILENAME = "existing_tags.json"
FILEPATH = os.path.join(DATA_FOLDER, FILENAME)

def load() -> list[str]:
    """Loads existing tags from the existing_tags.json file.
    Returns:
        list[str]: A list of existing tags, or an empty list if the file does not exist.
    """
    os.makedirs(DATA_FOLDER, exist_ok=True) # Ensure the folder exists; if not, create it
    try:
        with open(FILEPATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def add(tags: list[str]) -> None:
    """Adds tags to the existing_tags.json file."""
    existing_tags = load()

    for tag in tags:
        tag = tag.lower()
        if tag not in existing_tags:
            insort(existing_tags, tag)
    
    with open(FILEPATH, "w", encoding="utf-8") as file:
        json.dump(existing_tags, file, indent=4)

def remove(tag: str) -> None:
    """Removes a tag from the existing_tags.json file."""
    existing_tags = load()
    
    tag = tag.lower()
    if tag in existing_tags:
        existing_tags.remove(tag)
    
    with open(FILEPATH, "w", encoding="utf-8") as file:
        json.dump(existing_tags, file, indent=4)

def clear() -> None:
    """Clears all existing tags from the existing_tags.json file."""
    with open(FILEPATH, "w", encoding="utf-8") as file:
        json.dump([], file, indent=4)