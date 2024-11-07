import json
from datetime import datetime, timedelta
from pathlib import Path

class StoriesManager:
    
    
    def __init__(self):
        self.events_file_path = Path("resources/events_log.json")
        self.max_interval_for_event_group = timedelta(minutes=5)
        self.user_stories_file_path = Path("resources/user_stories.json")
        
        if self.events_file_path.exists():
            with open(self.events_file_path, "r") as file:
                self.events = json.load(file)
        else: 
            self.events = None

    def parse_timestamp(self, timestamp):
        return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    
    
    
    def group_events_into_user_stories(self):
        user_stories = []
        current_story = {
            "id": "",
            "title": "",
            "startTimestamp": "",
            "endTimestamp": "",
            "initialState": {},
            "actions": [],
            "networkRequests": [],
            "finalState": {}
        }
        last_event_time = None
        if self.events:
            for event in self.events:
                event_time = self.parse_timestamp(event["timestamp"])
                
                if not last_event_time or (event_time - last_event_time > self.max_interval_for_event_group):
                    if current_story["actions"]:
                        current_story["endTimestamp"] = last_event_time.isoformat()
                        user_stories.append(current_story)
                        
                current_story = {
                    "id": f"us-{len(user_stories) + 1}",
                    "title": "User Story Title", # => Modify depending on event's nature
                    "startTimestamp": event_time.isoformat(),
                    "endTimestamp": "",
                    "initialState": {"url": event.get("url")},
                    "actions": [],
                    "networkRequests": [],
                    "finalState": {}
                }
                
                if event["properties"]["eventType"] in ["input", "click", "navigation"]:
                    current_story["actions"].append(
                        {
                            "type": event["properties"]["eventType"],
                            "target": event["properties"]["distinct_id"],
                            "path": event["properties"]["$pathname"]
                        }
                    )
                elif event["properties"]["eventType"] == "network":
                    current_story["networkRequests"].append(
                        {
                            "url": event["properties"]["eventType"],
                            "method": event["properties"]["distinct_id"],
                            "status": event["properties"]["$pathname"],
                        }
                    )
                    
                current_story["finalState"]["url"] = event["properties"]["$current_url"]
                current_story["finalState"]["displayName"] = event["properties"]["elementText"] 
                last_event_time = event_time
                
            if current_story["actions"]:
                current_story["endTimestamp"] = last_event_time.isoformat()
                user_stories.append(current_story)
                
            with open(self.user_stories_file_path, "w") as outfile:
                json.dump(user_stories, outfile, indent=2)
                
        return user_stories