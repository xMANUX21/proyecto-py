from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session,select
from app.utils.dbConn import session_dep
from app.utils.dbConn import get_session
from app.auth.reservation_model import Reservation
from app.auth.user_model import User
from app.auth.user_controller import get_current_user
from app.schemas.reservation_schema import ReservationCreate,ReservationResponse,ReservationUpdate
from app.auth.room_model import Room
from app.auth.revervation_controller import create_reservation
from typing import List
from datetime import date


router = APIRouter(tags=["reservations"])

router = APIRouter()


#Crear reservacion
@router.post('/',response_model=ReservationResponse)
def create_reservations(room_data:ReservationCreate,session:Session=Depends(get_session)):
    return create_reservation(session,room_data)


#Reservaciones que tiene el usuario
@router.get('/me',response_model=List[ReservationResponse])
def my_reservation(
    session:Session=Depends(get_session),
    current_user:User=Depends(get_current_user)
):

    reservations= session.query(Reservation).filter(Reservation.user_id==current_user.id).all()

    if not reservations:
        raise HTTPException (status_code=404,detail="No se encuentran reservas para este usuario")
    
    return reservations

#Reservas por sala
@router.get('/{room_id}',response_model=List[ReservationResponse])
def room_reservation(
    room_id:int,
    session:Session=Depends(get_session)
):
    reservation=session.query(Reservation).filter(Reservation.room_id==room_id).all()

    if not reservation:
        raise HTTPException(status_code=404,detail="No se encontro reserva para esta sala")
    return reservation


#Reservas por fecha
@router.get('/date/{reservation_date}',response_model=List[ReservationResponse])
def date_reservation(
    reservation_date:date,
    session:Session=Depends(get_session)
):
    reservation= session.query(Reservation).filter(Reservation.dates==reservation_date).all()

    if not reservation:
        raise HTTPException(status_code=404,detail="No se encontro reserva para esa fecha")
    
    return reservation


#Para eliminar reserva por id
@router.delete('/{id}')
def delete_reservation(id:int,session:Session=Depends(get_session),current_user:User=Depends(get_current_user)):

    reservation=session.query(Reservation).filter(Reservation.id==id).first()

    if not reservation:
        raise HTTPException(status_code=404,detail="No se encontro esta reserva")
    
    if reservation.user_id != current_user.id:
        raise HTTPException (status_code=403,detail="No coincide con el usuario de la reserva")
    
    reservation.state="cancelada"
    session.commit()

    return {"message": "Reserva cancelada correctamente"}