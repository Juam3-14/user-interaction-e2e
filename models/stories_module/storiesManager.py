import json
import uuid

from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
from typing import List

from models.events_module.event import Event
from models.stories_module.userStory import UserStory

class StoriesManager:
    
    def __init__(self):
        self.user_stories_file_path = Path("resources/user_stories.json")
        self.stories_by_session = defaultdict(list)
        
    def process_event(self, event: Event):
        session_id = event.properties.session_id
        timestamp = datetime.fromisoformat(event.timestamp)
        if not self.stories_by_session[session_id] or self.is_new_story(event, self.stories_by_session[session_id][-1]):
            new_story = UserStory(
                id=str(uuid.uuid4()),
                session_id=session_id,
                startTimestamp=timestamp,
                endTimestamp=timestamp
            )
            self.stories_by_session[session_id].append(new_story)
        current_story: UserStory = self.stories_by_session[session_id][-1]
        current_story.add_event(event)

    def is_new_story(self, event: Event, last_story: UserStory) -> bool:
            # Lógica para decidir si este evento comienza una nueva historia
            # Ejemplo: agrupa en US fijándose en URL o tiempo desde el último evento (2 minutos)
            max_time_gap = timedelta(minutes=2)
            return (
                datetime.fromisoformat(event.timestamp) - last_story.endTimestamp > max_time_gap
                or event.properties.current_url != last_story.actions[-1].current_url
            )
    
    def get_user_stories(self) -> List[UserStory]:
        return [story for stories in self.stories_by_session.values() for story in stories]
    
    def save_user_stories_to_file(self):
        user_stories = [story.dict() for stories in self.stories_by_session.values() for story in stories]
        with open(self.user_stories_file_path, "w") as file:
            json.dump(user_stories, file, indent=4, default=str)