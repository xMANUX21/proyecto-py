from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from app.utils.security import create_access_token
from app.auth.room_model import Room
from app.schemas.room_schema import RoomCreate,RoomResponse

def create_room(session: Session, room_data:RoomCreate):
    new_room = Room(
        name=room_data.name,
        headquarters=room_data.headquarters,
        capacity=room_data.capacity,
        resources=room_data.resources
    )
    session.add(new_room)
    session.commit()
    session.refresh(new_room)
    return new_room

