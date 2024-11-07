from pydantic import BaseModel, Field
from typing import List, Optional
from models.events_module.elementAttributes import ElementAttributes
from datetime import datetime

class EventProperties(BaseModel):
    distinct_id: str # ID único del usuario
    session_id: str # ID de la sesión
    journey_id: str # ID del journey
    current_url: str = Field(alias="$current_url") # URL actual
    host: str = Field(alias="$host") # Hostname
    pathname: str = Field(alias="$pathname") # Path de la URL
    browser: str = Field(alias="$browser") # Navegador usado
    device: str = Field(alias="$device") # Tipo de dispositivo
    screen_height: Optional[int] = Field(default=0, alias="$screen_height") # Alto de la pantalla
    screen_width: Optional[int] = Field(default=0, alias="$screen_width") # Ancho de la pantalla
    eventType: str # Tipo de evento (ej: "click")
    elementType: str # Tipo de elemento HTML
    elementText: str # Texto del elemento
    elementAttributes: Optional[ElementAttributes] # Atributos del elemento => Class defined above
    timestamp: str # ISO timestamp
    x: int # Posición X del evento
    y: int # Posición Y del evento
    mouseButton: int # Botón del mouse usado
    ctrlKey: bool # Si Ctrl estaba presionado
    shiftKey: bool # Si Shift estaba presionado
    altKey: bool # Si Alt estaba presionado
    metaKey: bool # Si Meta estaba presionado
