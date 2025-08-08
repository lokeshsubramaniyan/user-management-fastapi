from pydantic import BaseModel
from datetime import datetime

class Credential(BaseModel):
    title: str
    username: str
    password: str
    url: str = None
    notes: str = None
    is_deleted: bool = False
    created_at: int = int(datetime.timestamp(datetime.now()))
    updated_at: int = int(datetime.timestamp(datetime.now()))

class UpdateCredential(BaseModel):
    title: str
    username: str
    password: str
    url: str = None
    notes: str = None
    is_deleted: bool = False
    updated_at: int = int(datetime.timestamp(datetime.now()))

