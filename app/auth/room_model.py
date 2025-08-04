from sqlmodel import Field, SQLModel
from typing import Optional,List
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import JSON

class Room(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True,unique=True)
    headquarters: str = Field(index=True)  #("Medellin","Bogota")
    capacity: str
    resources: List[str] = Field(default_factory=list, sa_column=Column(JSON))#De esta forma sabe como almacenar una lista 

