from datetime import datetime

from pydantic import BaseModel


class Credential(BaseModel):
    title: str
    username: str
    password: str
    url: str = ""
    notes: str = ""
    is_deleted: bool = False
    created_at: int = int(datetime.timestamp(datetime.now()))
    updated_at: int = int(datetime.timestamp(datetime.now()))


class UpdateCredential(BaseModel):
    title: str
    username: str
    password: str
    url: str = ""
    notes: str = ""
    is_deleted: bool = False
    updated_at: int = int(datetime.timestamp(datetime.now()))


class CredentialResponse(BaseModel):
    id: str
    title: str
    username: str
    password: str
    url: str = ""
    notes: str = ""
