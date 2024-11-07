from pydantic import BaseModel, Field
from typing import Optional

class ElementAttributes(BaseModel):
    class_: Optional[str] = Field(default=None, alias="class")
    href: Optional[str] = None