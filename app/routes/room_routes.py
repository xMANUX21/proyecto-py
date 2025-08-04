from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session,select
from app.utils.dbConn import session_dep
from app.utils.dbConn import get_session
from app.auth.room_model import Room
from app.auth.user_model import User
from app.auth.user_controller import get_current_user
from app.schemas.room_schema import RoomCreate,RoomResponse,RoomUpdate
from app.auth.room_controller import create_room
from typing import List

router = APIRouter(tags=["rooms"])


#Optener salas
@router.get("/", response_model=List[RoomResponse])
def get_all_rooms(session: Session = Depends(get_session)):
    rooms = session.exec(select(Room)).all()
    return rooms


#Para crear salas
@router.post('/',response_model=RoomResponse)
def create_rooms(room_data:RoomCreate,session:Session=Depends(get_session),current_user:User=Depends(get_current_user)):
    if current_user.role!="admin":
        raise HTTPException(status_code=403,detail="Solo los administradores pueden crear salas")
    return create_room(session,room_data)


#Para actualizar la sala
@router.put('/{room_id}',response_model=RoomResponse)
def update_room(
    room_id:int,
    room_data:RoomUpdate,
    session:Session=Depends(get_session),
    current_user:User=Depends(get_current_user)
):
    if current_user.role!="admin":
        raise HTTPException(status_code=403,detail="Solo los administradores pueden actualizar las salas")
     
    room=session.get(Room,room_id)

    if not room:
        raise HTTPException (status_code=404 , detail="no se encontra la sala")
    
   
    for key, value in room_data.dict(exclude_unset=True).items():
        setattr(room,key,value)

    session.add(room)
    session.commit()
    session.refresh(room)

    return room


#Para borrar salas
@router.delete('/{room_id}',response_model=RoomResponse)
def delete_room(room_id:int,session:Session=Depends(get_session),current_user:User=Depends(get_current_user)):
    if current_user.role!="admin":
        raise HTTPException (status_code=403,detail="Solo los administradores pueden borrar salas")
    
    room=session.get(Room,room_id)

    if not room:
        raise HTTPException(status_code=404,detail="Sala no encontrado")
    
    session.delete(room)
    session.commit()
    
    return room