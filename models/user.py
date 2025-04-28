from pydantic import BaseModel

class User(BaseModel):
    uid: str
    name: str
    email: str
    password: str




    ##### email null le rha signup k badd
