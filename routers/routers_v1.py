from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List

from models.events_module.event import Event
from models.events_module.eventsManager import EventsManager
from models.stories_module.storiesManager import StoriesManager
from models.tests_module.testCaseManager import TestCaseManager

router = APIRouter(prefix="/api/v1")
    
class EventsRequest(BaseModel):
    events: List[Event]

@router.post("/events")
async def process_events(request: Request, eventsRequest: EventsRequest):
    eventsManager = EventsManager()
    eventsManager.save_events_to_file(events=eventsRequest.events)
    return {"status": "success", "event_count": len(eventsRequest.events)}

@router.get("/stories")
async def generate_user_stories(request: Request):
    storiesManager = StoriesManager()
    eventsManager = EventsManager()
    
    for event in eventsManager.get_events_from_file():
        storiesManager.process_event(event) # => Process every event indepndently one by one
        
    storiesManager.save_user_stories_to_file() 
    user_stories = storiesManager.get_user_stories()
    return {"status": "success", "stories_count": len(user_stories)}

@router.get("/tests")
async def generate_test_cases(request: Request):
    storiesManager = StoriesManager()
    testCaseManager = TestCaseManager()

    userStories = storiesManager.get_stories_from_file()
    
    counter = 0
    
    for story in userStories:
                counter -= -1
                test_code = testCaseManager.create_test_case_code(story)
                testCaseManager.save_test_case(story, test_code)
                
    return {"status": "success", "stories_count": counter}
