import json
import os
from datetime import datetime
from time import time
import existing_tags as etm

DATA_FOLDER = "diary_data"

"""NOTE: this code is timezone naive, meaning it does not account for timezones."""
class DiaryEntry:
    """A class representing a diary entry with content and tags."""
    def __init__(self, content: str, tags: list[str], productive_activities_count: int = 0, timestamp: int | None = None, datetime_format: str = "%A, %#d %B %Y, %I:%M:%S %p"):
        """Initializes a DiaryEntry with content, tags, and an optional datetime.
        If datetime_created is not provided, it defaults to the current date and time.
        Args:
            content (str): The content of the diary entry.
            tags (list[str]): A list of tags associated with the entry.
            productive_activities_count (int): The number of productive activities worked on in the entry.
            timestamp (int | None): An optional timestamp of when the entry was created. The number should be a Unix timestamp (seconds since epoch).
            datetime_format (str): The format for the datetime string.
            """
        if timestamp is None:
            self._timestamp = int(time())
        else: 
            self._timestamp = timestamp
        timestamp_datetime = datetime.fromtimestamp(self._timestamp)
        self._datetime_created = timestamp_datetime.strftime(datetime_format)
        self._content = content
        self._tags = tags
        etm.add(self._tags)
        self._productive_activities_count = productive_activities_count

    def set_productive_activities_count(self, number: int) -> None:
        """Sets the productive activities count for the diary entry.
        Args:
            number (int): The productive activities count.
        """
        self._productive_activities_count = number

    def to_dict(self) -> tuple[int, dict]:
        """Converts the DiaryEntry instance to a dictionary.
        Returns:
            dict: A dictionary representation of the DiaryEntry instance.
        """
        return (self._timestamp, {
                "datetime_created": self._datetime_created,
                "content": self._content,
                "tags": self._tags,
                "productive_activities_count": self._productive_activities_count
            })
    
    @classmethod
    def from_dict(cls, data: tuple[int, dict]):
        """Creates a DiaryEntry instance from a dictionary.
        Args:
            data (dict): A tuple containing the entry's timestamp at index 0, and content content, tags, and datetime at index 1 in the follwing format:\n
            (timestamp, {
                "datetime_created": str,  # e.g. "Monday, 1 January 2024, 12:00:00 PM"
                "content": str,
                "tags": list[str],
                "productive_activities_count": int
                }
            )
        Returns:
            DiaryEntry: An instance of DiaryEntry.
        """
        timestamp = data[0]
        content = data[1].get("content", "")
        tags = data[1].get("tags", [])
        productive_activities_count = data[1].get("productive_activities_count", 0)
        
        return cls(content, tags, productive_activities_count, timestamp)
    
    def __repr__(self):
        return f"DiaryEntry(timestamp={self._timestamp}, datetime_created={self._datetime_created}, content={self._content}, tags={self._tags}, productive_activities_count={self._productive_activities_count})"
    
    def __str__(self):
        tags_str = ', '.join(self._tags) if self._tags else 'none'
        return (
            f"📅 {self._datetime_created}\n"
            f"🏷️ Tags: {tags_str}\n"
            f"{self._content}"
        )

class Diary:
    """A class representing a diary with a method to add entries."""
    def __init__(self, name: str, filepath: str | None = None):
        self.name = name

        if filepath is None:
            filename = f"{name.lower().replace(' ', '_')}_diary.json" # e.g. "Daily" becomes "daily_diary.json"
            # affixing "diary" also prevents file clashes with non-diary .json files
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
            return [DiaryEntry.from_dict((entry[0], entry[1])) for entry in data]
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