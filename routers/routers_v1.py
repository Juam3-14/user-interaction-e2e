from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional

from models.events_module.event import Event
from models.events_module.eventsManager import EventsManager
from models.stories_module.storiesManager import StoriesManager
from models.tests_module.testCaseManager import TestCaseManager

router = APIRouter(prefix="/api/v1")
    
class EventsRequest(BaseModel):
    events: List[Event]

@router.post("/events", summary="Process Events", response_description="The number of events processed.")
async def process_events(request: Request, eventsRequest: EventsRequest):
    """
    Process and store a list of events.
    This endpoint accepts a list of events and saves them to a file for future processing.
    Args:
        request (Request): The HTTP request object.
        eventsRequest (EventsRequest): Contains a list of event data to be processed.
    Returns:
        dict: A dictionary with a status message and the count of events processed.
    Raises:
        HTTPException: If an error occurs during processing.
    """
    try:
        eventsManager = EventsManager()
        eventsManager.save_events_to_file(events=eventsRequest.events)
        return {"status": "success", "event_count": len(eventsRequest.events)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stories", summary="Generate User Stories", response_description="List of user stories.")
async def generate_user_stories(request: Request, session_id: Optional[str] = None):
    """
    Generate and retrieve user stories from processed events.
    This endpoint processes stored events, generates user stories, saves them to a file, and optionally filters by session ID.
    Args:
        request (Request): The HTTP request object.
        session_id (Optional[str]): A session ID to filter the user stories.
    Returns:
        dict: A dictionary with a status message and the list of generated user stories.
    Raises:
        HTTPException: If an error occurs during story generation.
    """
    storiesManager = StoriesManager()
    eventsManager = EventsManager()
    try:
        for event in eventsManager.get_events_from_file():
            storiesManager.process_event(event) # => Process every event indepndently one by one            
        storiesManager.save_user_stories_to_file() 

        user_stories = storiesManager.get_stories_from_file()
        stories_array = []
        for story in user_stories:
            if not session_id:
                stories_array.append(story)
            elif story.session_id == session_id:
                stories_array.append(story)
            else:
                pass
        return {"status": "success", "stories": stories_array}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tests", summary="Generate Test Cases", response_description="Generated test cases for user stories.")
async def generate_test_cases(request: Request, story_id: Optional[str] = None):
    """
    Generate test case code for user stories and save it to a file.
    This endpoint generates test cases based on the user stories in storage.
    Optionally, it can filter by a specific story ID to generate tests only for that story.
    Args:
        request (Request): The HTTP request object.
        story_id (Optional[str]): An optional story ID to filter the user stories for test case generation.
    Returns:
        dict: A dictionary with a status message and the list of generated test cases.
    Raises:
        HTTPException: If an error occurs during test case generation.
    """
    storiesManager = StoriesManager()
    testCaseManager = TestCaseManager()
    try:
        userStories = storiesManager.get_stories_from_file()
        tests_array = []
        for story in userStories:
                # TODO: Improve the filter logic. Function create_test_case should be responsible of deciding to create the user_story only for the id provided if so.
                if not story_id:
                    test_code = testCaseManager.create_test_case_code(story)
                    testCaseManager.save_test_case(story, test_code)
                    tests_array.append(test_code)
                elif story_id == story.id:
                    test_code = testCaseManager.create_test_case_code(story)
                    testCaseManager.save_test_case(story, test_code)
                    tests_array.append(test_code)
                else: 
                    pass
        return {"status": "success", "test_cases": tests_array}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))