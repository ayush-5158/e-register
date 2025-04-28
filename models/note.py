from pydantic import BaseModel

class Note(BaseModel):
    uid: str
    activity: str
    date: str

class NoteUpdate(BaseModel):
    activity: str
    date: str

class ResponseModel(BaseModel):
    success: bool
    message: str

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


class Announcement(BaseModel):
    title: str
    content: str
    created_at: str
