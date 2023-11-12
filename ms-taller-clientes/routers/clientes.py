from fastapi import APIRouter, HTTPException
from contextlib import contextmanager
import sqlite3
from models.customer import Customer

@contextmanager
def db_connection():
    conn = sqlite3.connect('../microservicios.db')
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        conn.commit()
        conn.close()

router = APIRouter(
    prefix="/taller/web/cliente"
)

@router.get("/")
async def get_customers():
    with db_connection() as cursor:
        cursor.execute("SELECT * FROM customer_data",)
        customer_data = cursor.fetchall()
    return customer_data

@router.post("/")
async def register_customer(new_customer: Customer):
    with db_connection() as cursor:
        cursor.execute("SELECT * FROM customer_data WHERE email=? OR username=?", (new_customer.email, new_customer.user_name,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            return {"mensaje": "Usuario ya registrado"}
        else:
            cursor.execute('INSERT INTO customer_data (username, email) VALUES (?, ?)', (new_customer.user_name, new_customer.email,))
            return {"mensaje": "Usuario creado exitosamente."}

@router.delete("/{customer_id}")
async def delete_customer(customer_id:int):
    with db_connection() as cursor:
        cursor.execute("SELECT * FROM customer_data WHERE customer_id=?",(customer_id,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.execute("DELETE FROM customer_data WHERE customer_id=?",(customer_id,))
            return {"mensaje": f"Usuario con ID {customer_id} eliminado correctamente."}
        else:
            raise HTTPException(status_code=404, detail=f"Usuario con ID {customer_id} no encontrado.")

@router.put("/{customer_id}")
async def update_customer(customer_id:int,updated_data:Customer):
    with db_connection() as cursor:
        # Verifica si el usuario existe antes de intentar actualizarlo
        cursor.execute("SELECT * FROM customer_data WHERE customer_id=?", (customer_id,))
        existing_user = cursor.fetchone()

        if existing_user:
            # Si el usuario existe, procede a actualizar sus datos
            update_query = "UPDATE customer_data SET username=?, email=? WHERE customer_id=?"

            # Ejecuta la consulta de actualización
            cursor.execute(update_query, (updated_data.user_name, updated_data.email, customer_id))

            return {"mensaje": f"Usuario con ID {customer_id} actualizado correctamente."}
        else:
            # Si el usuario no existe, devuelve un error
            raise HTTPException(status_code=404, detail=f"Usuario con ID {customer_id} no encontrado.")

@router.post("/set_fiado_status/{customer_id}")
async def set_fiado_status(customer_id:int,fiado_status:bool):
    with db_connection() as cursor:
        # Verifica si el cliente existe antes de intentar actualizar su estado de fiado
        cursor.execute("SELECT * FROM customer_data WHERE customer_id=?", (customer_id,))
        existing_user = cursor.fetchone()

        if existing_user:
            # Si el cliente existe, procede a actualizar el estado de fiado
            cursor.execute("UPDATE customer_data SET estado_fiado=? WHERE customer_id=?", (fiado_status, customer_id))

            return {"mensaje": f"Estado de fiado del cliente con ID {customer_id} actualizado correctamente."}
        else:
            # Si el cliente no existe, devuelve un error
            raise HTTPException(status_code=404, detail=f"Cliente con ID {customer_id} no encontrado.")


# VALIDAR USERNAME
# @router.post("/validate_username")
# async def validate_username(username: str):
#     with db_connection() as cursor:
#         # Verifica si el nombre de usuario ya existe en la base de datos
#         cursor.execute("SELECT * FROM customer_data WHERE username=?", (username,))
#         existing_user = cursor.fetchone()

#         if existing_user:
#             # Si el nombre de usuario ya existe, devuelve un mensaje indicando que no está disponible
#             raise HTTPException(status_code=400, detail="El nombre de usuario no está disponible.")
#         else:
#             # Si el nombre de usuario no existe, devuelve un mensaje indicando que está disponible
#             return {"mensaje": "El nombre de usuario está disponible."}
