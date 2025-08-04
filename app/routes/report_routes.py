from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func
from sqlalchemy import extract
from app.utils.dbConn import get_session
from app.auth.reservation_model import Reservation
from app.auth.room_model import Room
from app.auth.user_model import User
from app.auth.user_controller import get_current_user
from datetime import datetime,date

router = APIRouter(tags=["reports"])


#Que sala se ha reservado mas veces
@router.get("/most-reserved-room")
def get_most_reserved_room(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede ver esto")

    statement = (
        select(Room.name, func.count(Reservation.id).label("total")) #Seleccion el nombre de cada sala y la cantidad de reservas
        .join(Reservation, Reservation.room_id == Room.id)#Junta room con reservas y busca cuales coinciden 
        .group_by(Room.name)#Las agrupa por el nombre de la sala
        .order_by(func.count(Reservation.id).desc())#Lo ordena de forma descendente la cantidad de reservas
        .limit(1)#Muestra solo 1
    )

    result = session.exec(statement).first() #Devuelve el primero y unico

    if result:
        return {"room_name": result[0], "total_reservations": result[1]}
    
    return {"message": "No hay reservas registradas"}


#Cuantas horas ha reservado un usuario este mes
@router.get("/{user_id}")
def horas_reservadas_usuario(user_id: int, session: Session = Depends(get_session)):
    ahora = datetime.now()
    mes_actual = ahora.month
    anio_actual = ahora.year

    # Query corregida con extract()
    query = select(Reservation).where(
        Reservation.user_id == user_id,
        extract('month', Reservation.dates) == mes_actual,
        extract('year', Reservation.dates) == anio_actual
    )
    reservas = session.exec(query).all()

    total_horas = 0
    for r in reservas:
        # Combina con la fecha de hoy para obtener datetime completo
        inicio = datetime.combine(date.today(), r.start_time)
        fin = datetime.combine(date.today(), r.end_time)
        total_horas += (fin - inicio).seconds / 3600

    return {"user_id": user_id, "horas_reservadas": round(total_horas, 2)}