from pydantic import BaseModel
from typing import Optional
from datetime import date, time



class NewProjectSch(BaseModel):
    name: str
