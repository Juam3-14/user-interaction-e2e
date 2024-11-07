import json
from pathlib import Path
from typing import List
from models.events_module.event import Event

class EventsManager:
    def __init__(self):
        self.events_file_path = Path("resources/events_log.json")
        
    def save_events_to_file(self, events: List[Event]):
        
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