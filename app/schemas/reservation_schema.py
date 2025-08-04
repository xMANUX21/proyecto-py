from pydantic import BaseModel
from typing import List,Optional
from sqlmodel import Field, SQLModel
from datetime import date, time
from app.auth.reservation_model import State


class ReservationCreate(BaseModel):
    user_id: int
    room_id: int
    dates: date
    start_time: time
    end_time: time
    state: State = Field(default=State.pendiente)


class ReservationResponse(BaseModel):
    id: int
    user_id: int
    room_id: int
    dates: date
    start_time: time
    end_time: time
    state: State

    class Config:
        orm_mode = True


class ReservationUpdate(BaseModel):  
    user_id: Optional[int] = None
    room_id: Optional[int] = None
    dates: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    state: Optional[State] = None
