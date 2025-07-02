import json
import os
from bisect import insort

DATA_FOLDER = "diary_data"
FILENAME = "existing_diaries.json"
FILEPATH = os.path.join(DATA_FOLDER, FILENAME)

def load() -> list[str]:
    """Loads existing diaries from the existing_diaries.json file.
    Returns:
        list[str]: A list of existing diaries, or an empty list if the file does not exist.
    """
    os.makedirs(DATA_FOLDER, exist_ok=True) # Ensure the folder exists; if not, create it
    try:
        with open(FILEPATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def add(diary: str) -> None:
    """Adds a diary to the existing_diaries.json file."""
    existing_diaries = load()

    if diary not in existing_diaries:
        insort(existing_diaries, diary)
    
    with open(FILEPATH, "w", encoding="utf-8") as file:
        json.dump(existing_diaries, file, indent=4)

def remove(diary: str) -> None:
    """Removes a diary from the existing_diaries.json file."""
    existing_diaries = load()
    
    if diary in existing_diaries:
        existing_diaries.remove(diary)
    
    with open(FILEPATH, "w", encoding="utf-8") as file:
        json.dump(existing_diaries, file, indent=4)

def clear() -> None:
    """Clears all existing diaries from the existing_diaries.json file."""
    with open(FILEPATH, "w", encoding="utf-8") as file:
        json.dump([], file, indent=4)

def contains(diary: str) -> bool:
    """Checks if a diary exists in the existing_diaries.json file.
    Args:
        diary (str): The name of the diary to check.
    Returns:
        bool: True if the diary exists, False otherwise.
    """
    existing_diaries = load()
    return diary in existing_diaries

def print_formatted() -> str:
    """Loads existing diaries and formats them as a string.
    Returns:
        str: A formatted string of existing diaries.
    """
    existing_diaries = load()
    if not existing_diaries:
        return "No existing diaries found."
    
    return "\n".join(f"- {diary}" for diary in existing_diaries)