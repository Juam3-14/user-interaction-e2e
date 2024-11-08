from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from models.events_module.event import Event

class US_Step(BaseModel):
    event: str
    timestamp: str
    distinct_id: str
    session_id: str
    current_url: Optional[str] = None
    journey_id: Optional[str] = None
    eventType: Optional[str] = None
    elementType: Optional[str] = None
    elementText: Optional[str] = None
    eventClass: Optional[str] = None
    href: Optional[str] = None
    
    @classmethod
    def from_event(cls, event: 'Event'):
        return cls(
            event=event.event,
            timestamp=event.timestamp,
            distinct_id=event.properties.distinct_id,
            session_id=event.properties.session_id,
            current_url=event.properties.current_url if hasattr(event.properties, 'current_url') else None,
            journey_id=event.properties.journey_id if hasattr(event.properties, 'journey_id') else None,
            eventType=event.properties.eventType if hasattr(event.properties, 'eventType') else None,
            elementType=event.properties.elementType if hasattr(event.properties, 'elementType') else None,
            elementText=event.properties.elementText if hasattr(event.properties, 'elementText') else None,
            eventClass=event.properties.elementAttributes.class_ if event.properties.elementAttributes else None,
            href=event.properties.elementAttributes.href if event.properties.elementAttributes else None
        )



class UserStory(BaseModel):
    id: str
    session_id: str
    startTimestamp: datetime
    endTimestamp: Optional[datetime]
    actions: List[US_Step] = []
    
    def add_event(self, event: Event):
        self.actions.append(US_Step.from_event(event))
        self.endTimestamp = datetime.fromisoformat(event.timestamp)
    
    @property    
    def title(self) -> str:
        return f"User story for session {self.session_id}"
    
    
