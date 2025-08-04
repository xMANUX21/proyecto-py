from fastapi import Depends, HTTPException
from sqlmodel import Session, select ,or_, not_
from app.utils.security import create_access_token
from app.auth.reservation_model import Reservation
from app.schemas.reservation_schema import ReservationCreate
from datetime import datetime,timedelta

def create_reservation(session: Session, reservation_data:ReservationCreate):

    # Valida que la hora del inicio sea menor que la del final
    if reservation_data.start_time >= reservation_data.end_time:
        raise HTTPException(
            status_code=400,
            detail="La hora de inicio debe ser menor que la hora del final."
        )
    
    #Vdlidacion de 1 hora
    duration=datetime.combine(reservation_data.dates,reservation_data.end_time)- datetime.combine(reservation_data.dates,reservation_data.start_time) #Combine junta la fecha y hora
    if duration != timedelta(hours=1): # valida que sean hours , en este caso 1
        raise HTTPException(status_code=400,detail="Las reservas deben durar 1 hora")
    
    #Validacion para que no se crucen las reservas
    conflicts= session.exec( 
        select(Reservation).where(#Seleccionamos la table
            Reservation.room_id==reservation_data.room_id,
            Reservation.dates==reservation_data.dates, #Buscamos la fecha y sala que coincidan
            not_(
                or_(
                    Reservation.end_time<=reservation_data.start_time, #Si no se cumple que la hora en que finaliza la antigua reserva sea menor a la hora que inicia la otra o si la hora que inicia la antigua no es mayor a cuando finaliza la otra , se cruzan
                    Reservation.start_time>=reservation_data.end_time
                )
            )
        )
    ).all()

    if  conflicts:
        raise HTTPException (status_code=400,detail="Ya existe una reserva a esa hora")
    
    new_reservation = Reservation(
        user_id=reservation_data.user_id,
        room_id=reservation_data.room_id,
        dates=reservation_data.dates,
        start_time=reservation_data.start_time,
        end_time=reservation_data.end_time,
        state=reservation_data.state
    )

    session.add(new_reservation)
    session.commit()
    session.refresh(new_reservation)
    
    return new_reservation

