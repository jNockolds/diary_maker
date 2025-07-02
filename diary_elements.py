import json
import os
from datetime import datetime
import existing_tags as etm

DATA_FOLDER = "diary_data"

class DiaryEntry:
    """A class representing a diary entry with content and tags."""
    def __init__(self, content: str, tags: list[str],  datetime_created: str | None = None):
        """Initializes a DiaryEntry with content, tags, and an optional datetime.
        If datetime_created is not provided, it defaults to the current date and time.
        Args:
            content (str): The content of the diary entry.
            tags (list[str]): A list of tags associated with the entry.
            datetime_created (str | None): Optional; if provided, it should be a string representing the date and time. Formatted as "Wednesday, 2 July 2025, 03:30:03 PM".
        """
        if datetime_created is None:
            self.datetime_created = datetime.now().strftime("%A, %#d %B %Y, %I:%M:%S %p") 
        else: 
            self.datetime_created = datetime_created
        self.content = content
        self.tags = tags
        etm.add(tags)

    def to_dict(self):
        """Converts the DiaryEntry instance to a dictionary.
        Returns:
            dict: A dictionary representation of the DiaryEntry instance.
        """
        return {
            self.datetime_created: {
                "content": self.content,
                "tags": self.tags
            }
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Creates a DiaryEntry instance from a dictionary.
        Args:
            data (dict): A dictionary containing the entry's content, tags, and datetime.
        Returns:
            DiaryEntry: An instance of DiaryEntry.
        """
        datetime_created = list(data.keys())[0]
        content = data[datetime_created]["content"]
        tags = data[datetime_created]["tags"]
        return cls(content, tags, datetime_created)
    
    def __repr__(self):
        return f"DiaryEntry(datetime_created={self.datetime_created}, content={self.content}, tags={self.tags})"
    
    def __str__(self):
        tags_str = ', '.join(self.tags) if self.tags else 'none'
        return (
            f"📅 {self.datetime_created}\n"
            f"🏷️ Tags: {tags_str}\n"
            f"{self.content}"
        )

class Diary:
    """A class representing a diary with a method to add entries."""
    def __init__(self, name: str, filepath: str | None = None):
        self.name = name

        if filepath is None:
            filename = f"{name.lower().replace(' ', '_')}_diary.json"
            filepath = os.path.join(DATA_FOLDER, filename)
        self.filepath = filepath


    def add_entry(self, entry: DiaryEntry) -> None:
        """Adds an entry to the diary's file with the given content and tags.
        If the file exists, it appends the new entry to the existing entries.
        If the file does't exist, it creates a new file with the default structure and appends the entry.
        Args:
            entry (DiaryEntry): The diary entry to be added.
        """
        os.makedirs(DATA_FOLDER, exist_ok=True) # Ensure the folder exists; if not, create it
        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        
        data.append(entry.to_dict())
        
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    
    def get_entries(self) -> list[DiaryEntry]:
        """Retrieves all entries from the diary's file.
        Returns:
            list[DiaryEntry]: A list of DiaryEntry instances.
        """
        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
            return [DiaryEntry.from_dict(entry) for entry in data]
        except FileNotFoundError:
            return []
    
    def __str__(self):
        entries = self.get_entries()
        if not entries:
            return f"Diary '{self.name}' is empty."

        buffer = "-------------------------"
        output = buffer + "\n"
        output += f"Diary name: {self.name}\n"
        output += f"Filepath: {self.filepath}\n"
        output += buffer

        
        for entry in entries:
            output += "\n" + str(entry)
            output += "\n" + buffer
        
        return output