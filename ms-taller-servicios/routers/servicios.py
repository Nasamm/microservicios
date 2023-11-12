from contextlib import contextmanager
import sqlite3
from fastapi import APIRouter, HTTPException
from datetime import datetime
from models.service import Service

router = APIRouter(prefix="/taller/web/servicios")


@contextmanager
def db_connection():
    conn = sqlite3.connect("../microservicios.db")
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        conn.commit()
        conn.close()


@router.post("/cita")
async def book_service(customer_id: int, service_id: int, date: str, time: str):
    try:
        # Convierte la fecha y la hora a objetos datetime
        datetime_obj = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")

        with db_connection() as cursor:
            # Verifica si el cliente y el servicio existen antes de realizar la reserva
            cursor.execute(
                "SELECT * FROM customer_data WHERE customer_id=?", (customer_id,)
            )
            existing_customer = cursor.fetchone()

            cursor.execute(
                "SELECT * FROM services_data WHERE service_id=?", (service_id,)
            )
            existing_service = cursor.fetchone()

            if existing_customer and existing_service:
                # Si el cliente y el servicio existen, procede a realizar la reserva
                cursor.execute(
                    "INSERT INTO reservation_list (customer_id, service_id, date) VALUES (?, ?, ?)",
                    (customer_id, service_id, datetime_obj),
                )

                return {"mensaje": "Reserva realizada exitosamente."}
            else:
                # Si el cliente o el servicio no existen, devuelve un error
                raise HTTPException(
                    status_code=404, detail="Cliente o servicio no encontrado."
                )
    except ValueError:
        # Si hay un error al convertir la fecha o la hora, devuelve un error
        raise HTTPException(
            status_code=400, detail="Formato de fecha o hora incorrecto."
        )


@router.get("/citados")
async def get_reservations():
    with db_connection() as cursor:
        # Obtiene la lista de reservas desde la base de datos
        cursor.execute("SELECT * FROM reservation_list")
        reservations = cursor.fetchall()

        if reservations:
            # Si hay reservas, devuelve la lista
            return {"reservations": reservations}
        else:
            # Si no hay reservas, devuelve un mensaje indicando que la lista está vacía
            raise HTTPException(status_code=404, detail="No hay reservas registradas.")


@router.post("/")
async def register_service(service: Service):
    with db_connection() as cursor:
        # Verifica si el servicio ya existe en la base de datos
        cursor.execute(
            "SELECT * FROM services_data WHERE service_name=?", (service.service_name,)
        )
        existing_service = cursor.fetchone()

        if existing_service:
            # Si el servicio ya existe, devuelve un error
            raise HTTPException(
                status_code=400, detail="El servicio ya está registrado."
            )
        else:
            # Si el servicio no existe, procede a registrarlo
            cursor.execute(
                "INSERT INTO services_data (service_name, description, price) VALUES (?, ?, ?)",
                (service.service_name, service.description, service.price),
            )

            return {"mensaje": "Servicio registrado exitosamente."}


@router.get("/")
async def get_services():
    with db_connection() as cursor:
        # Obtiene la lista de servicios desde la base de datos
        cursor.execute("SELECT * FROM services_data")
        services = cursor.fetchall()

        if services:
            # Si hay servicios registrados, devuelve la lista
            return {"services": services}
        else:
            # Si no hay servicios registrados, devuelve un mensaje indicando que la lista está vacía
            raise HTTPException(status_code=404, detail="No hay servicios registrados.")


@router.put("/{service_id}")
async def update_service(service_id:int,updated_service: Service):
    with db_connection() as cursor:
        # Verifica si el servicio existe antes de intentar actualizarlo
        cursor.execute("SELECT * FROM services_data WHERE service_id=?", (service_id,))
        existing_service = cursor.fetchone()

        if existing_service:
            # Si el servicio existe, procede a actualizar sus datos
            cursor.execute(
                "UPDATE services_data SET service_name=?, description=?, price=? WHERE service_id=?",
                (updated_service.service_name, updated_service.description, updated_service.price, service_id)
            )

            return {"mensaje": f"Servicio con ID {service_id} actualizado correctamente."}
        else:
            # Si el servicio no existe, devuelve un error
            raise HTTPException(status_code=404, detail=f"Servicio con ID {service_id} no encontrado.")


@router.delete("/{service_id}")
async def delete_service(service_id:int):
    with db_connection() as cursor:
        # Verifica si el servicio existe antes de intentar eliminarlo
        cursor.execute("SELECT * FROM services_data WHERE service_id=?", (service_id,))
        existing_service = cursor.fetchone()

        if existing_service:
            # Si el servicio existe, procede a eliminarlo
            cursor.execute("DELETE FROM services_data WHERE service_id=?", (service_id,))

            return {"mensaje": f"Servicio con ID {service_id} eliminado correctamente."}
        else:
            # Si el servicio no existe, devuelve un error
            raise HTTPException(status_code=404, detail=f"Servicio con ID {service_id} no encontrado.")


@router.post("/validar_pago")
async def validate_payment(reservation_id: int, payment_status: bool):
    with db_connection() as cursor:
        # Verifica si la reserva existe antes de intentar validar el pago
        cursor.execute("SELECT * FROM reservation_list WHERE id=?", (reservation_id,))
        existing_reservation = cursor.fetchone()

        if existing_reservation:
            # Si la reserva existe, procede a actualizar su estado de pago
            cursor.execute(
                "UPDATE reservation_list SET payment_status=? WHERE id=?",
                (payment_status, reservation_id)
            )

            return {"mensaje": f"Validación de pago para la reserva con ID {reservation_id} exitosa."}
        else:
            # Si la reserva no existe, devuelve un error
            raise HTTPException(status_code=404, detail=f"Reserva con ID {reservation_id} no encontrada.")
