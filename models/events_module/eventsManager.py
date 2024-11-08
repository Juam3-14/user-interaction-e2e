import json
from pathlib import Path
from typing import List
from pydantic import TypeAdapter
from models.events_module.event import Event

class EventsManager:
    def __init__(self):
        self.events_file_path = Path("resources/events_log.json")
        
    def save_events_to_file(self, events: List[Event]):
        """
        This function saves a list of event objects to a file in JSON format.
        
        :param events: The `save_events_to_file` method takes a list of `Event` objects as input. It
        then serializes each `Event` object into a dictionary using the `model_dump` method with
        `by_alias=True`. These dictionaries are stored in the `events_data` list
        :type events: List[Event]
        """
        events_data = [event.model_dump(by_alias=True) for event in events]
        
        if self.events_file_path.exists():
            with open(self.events_file_path, "r+") as file:
                existing_data = json.load(file)
                existing_data.extend(events_data)
                file.seek(0)
                json.dump(existing_data, file, indent=4)
        else:
            with open(self.events_file_path, "w") as file:
                json.dump(events_data, file, indent=4)
                
    def get_events_from_file(self):
        """
        The function reads events from a file and yields each event.
        """
        if self.events_file_path.exists():
            with open(self.events_file_path, "r") as file:
                events = TypeAdapter(List[Event]).validate_python(json.load(file))
            for event in events:
                yield event