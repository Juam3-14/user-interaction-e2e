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
    try:
        eventsManager = EventsManager()
        eventsManager.save_events_to_file(events=eventsRequest.events)
        return {"status": "success", "event_count": len(eventsRequest.events)}
    except Exception as e:
        return {"status": "error", "detail": e}

@router.get("/stories")
async def generate_user_stories(request: Request, session_id: str = None):
    storiesManager = StoriesManager()
    eventsManager = EventsManager()
    try:
        for event in eventsManager.get_events_from_file():
            storiesManager.process_event(event) # => Process every event indepndently one by one            
        storiesManager.save_user_stories_to_file() 
        user_stories = storiesManager.get_stories_from_file(session_id=session_id)
        return {"status": "success", "stories_count": len(user_stories)}
    except Exception as e:
            return {"status": "error", "detail": e}

@router.get("/tests")
async def generate_test_cases(request: Request, story_id: str = None):
    storiesManager = StoriesManager()
    testCaseManager = TestCaseManager()
    try:
        userStories = storiesManager.get_stories_from_file()
        counter = 0
        for story in userStories:
                    # TODO: Improve the filter logic. Function create_test_case should be responsible of deciding to create the user_story only for the id provided if so.
                    if not story_id:
                        counter -= -1
                        test_code = testCaseManager.create_test_case_code(story)
                        testCaseManager.save_test_case(story, test_code)
                    elif story_id == story.id:
                        counter -= -1
                        test_code = testCaseManager.create_test_case_code(story)
                        testCaseManager.save_test_case(story, test_code)
                    else: 
                        pass
        return {"status": "success", "stories_count": counter}
    except Exception as e:
            return {"status": "error", "detail": e}