# dao/reservation_dao.py

import mysql.connector
from db_connection import get_conn, close_conn
from customer import Customer
from room import Room
from reservation import Reservation
from typing import Optional, List

class ReservationDAO:
    """DAO para la entidad RESERVATIONS."""

    def create(self, res: Reservation, total_cost: float) -> Optional[int]:
        """
        Inserta una nueva reserva en la base de datos.
        El pago se asocia después.
        """
        conn = None
        cursor = None
        query = """
            INSERT INTO RESERVATIONS 
            (customer_id, room_id, check_in_date, check_out_date, status, total_cost) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            res.getCustomer().getId(),
            res.getRoom().getId(),
            res.getCheckIn(),
            res.getCheckOut(),
            'Confirmed',  # Se confirma al pasar a la ventana de pago
            total_cost
        )

        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            
            res_id = cursor.lastrowid
            res.setId(res_id) # Actualizamos el ID en el objeto
            
            print(f"INFO: Reserva #{res_id} creada en la BD.")
            return res_id

        except mysql.connector.Error as err:
            print(f"ERROR: No se pudo crear la reserva en la BD: {err}")
            if conn:
                conn.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                close_conn(conn)

    def get_all(self) -> List[Reservation]:
        """
        Obtiene todas las reservas de la base de datos, reconstruyendo los objetos
        Customer y Room asociados.
        """
        conn = None
        cursor = None
        reservations = []
        query = """
            SELECT 
                r.reservation_id, r.check_in_date, r.check_out_date, r.status, r.total_cost,
                c.customer_id, c.first_name, c.second_name, c.last_name, c.second_last_name, c.phone, c.email, c.state, c.curp, c.password_hash,
                rm.room_id, rm.room_number, rm.room_type, rm.status, rm.cost_per_night, rm.description
            FROM RESERVATIONS r
            JOIN CUSTOMERS c ON r.customer_id = c.customer_id
            JOIN ROOMS rm ON r.room_id = rm.room_id
        """
        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute(query)
            records = cursor.fetchall()

            for record in records:
                # Reconstruir el objeto Customer
                customer = Customer(record[5], record[6], record[7], record[8], record[9], record[10], record[11], record[12], record[13], record[14])
                
                # Reconstruir el objeto Room
                room = Room(record[15], record[16], record[17], record[18], record[19], record[20])

                # Reconstruir el objeto Reservation
                reservation = Reservation(record[0], str(record[1]), str(record[2]), customer, room)
                reservations.append(reservation)

            print(f"INFO: Se cargaron {len(reservations)} reservas desde la BD.")
        except mysql.connector.Error as err:
            print(f"ERROR: No se pudieron obtener las reservas de la BD: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                close_conn(conn)
        return reservations

    def delete(self, reservation_id: int) -> bool:
        """
        Elimina una reserva de la base de datos por su ID.
        """
        conn = None
        cursor = None
        query = "DELETE FROM RESERVATIONS WHERE reservation_id = %s"
        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute(query, (reservation_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                print(f"INFO: Reserva #{reservation_id} eliminada de la BD.")
                return True
            return False
        except mysql.connector.Error as err:
            print(f"ERROR: No se pudo eliminar la reserva #{reservation_id}: {err}")
            if conn:
                conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                close_conn(conn)

    def link_payment(self, reservation_id: int, payment_id: int) -> bool:
        """
        Asocia un ID de pago a una reserva existente.
        """
        conn = None
        cursor = None
        query = "UPDATE RESERVATIONS SET payment_id = %s WHERE reservation_id = %s"
        values = (payment_id, reservation_id)

        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount > 0:
                print(f"INFO: Pago #{payment_id} asociado a la Reserva #{reservation_id}.")
                return True
            else:
                print(f"WARN: No se encontró la Reserva #{reservation_id} para asociar el pago.")
                return False

        except mysql.connector.Error as err:
            print(f"ERROR: No se pudo asociar el pago a la reserva: {err}")
            if conn:
                conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                close_conn(conn)