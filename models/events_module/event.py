from pydantic import BaseModel
from models.events_module.eventProperties import EventProperties
from datetime import datetime

class Event(BaseModel):
    event: str # Tipo de evento (ej: "$click")
    properties: EventProperties # Propiedades del evento => Class defined above
    timestamp: str # ISO timestamp del evento