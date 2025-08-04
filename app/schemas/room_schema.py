from pydantic import BaseModel
from typing import List,Optional

class RoomCreate(BaseModel):
    name:str
    headquarters:str
    capacity:str
    resources:List[str]

class RoomResponse(BaseModel):
    id:int
    name:str
    headquarters:str
    capacity:str
    resources:List[str]

    class config():
        orm_mode:True


class RoomUpdate(BaseModel):  
    name:Optional[str]=None
    headquarters:Optional[str]=None
    capacity:Optional[str]=None
    resources:Optional[List[str]]=None
