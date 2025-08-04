from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from app.utils.security import create_access_token
from app.auth.reservation_model import Reservation
from app.schemas.reservation_schema import ReservationCreate

def create_reservation(session: Session, reservation_data:ReservationCreate):

    # Valida que la hora del inicio sea menor que la del final
    if reservation_data.start_time >= reservation_data.end_time:
        raise HTTPException(
            status_code=400,
            detail="La hora de inicio debe ser menor que la hora del final."
        )
    
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

