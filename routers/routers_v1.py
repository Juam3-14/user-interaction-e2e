from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List

from models.events_module.event import Event
from models.events_module.eventsManager import EventsManager
from models.stories_module.storiesManager import StoriesManager

router = APIRouter(prefix="/api/v1")
    
class EventsRequest(BaseModel):
    events: List[Event]

@router.post("/events")
async def method(request: Request, eventsRequest: EventsRequest):
    eventsManager = EventsManager()
    eventsManager.save_events_to_file(events=eventsRequest.events)
    return {"status": "success", "event_count": len(eventsRequest.events)}

@router.get("/stories")
async def method(request: Request):
    storiesManager = StoriesManager()
    user_stories = storiesManager.group_events_into_user_stories()
    return {"status": "success", "stories_count": len(user_stories)}

@router.get("/tests")
async def method(request: Request):
    return {"value": "returned value"}
