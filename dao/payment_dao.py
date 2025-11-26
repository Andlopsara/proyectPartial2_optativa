# dao/payment_dao.py

import mysql.connector
from db_connection import get_conn, close_conn
from payment import Payment
from typing import Optional

class PaymentDAO:
    """DAO para la entidad PAYMENTS."""

    def create(self, payment: Payment) -> Optional[int]:
        """
        Inserta un nuevo pago en la base de datos.
        """
        conn = None
        cursor = None
        
        query = """
            INSERT INTO PAYMENTS 
            (amount, payment_method, payment_date) 
            VALUES (%s, %s, %s)
        """
        values = (
            payment.getAmount(),
            payment.getPaymentMethod(),
            payment.getDate()
        )

        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            
            payment_id = cursor.lastrowid
            payment.setId(payment_id)
            
            print(f"INFO: Pago #{payment_id} por ${payment.getAmount()} guardado en la BD.")
            return payment_id

        except mysql.connector.Error as err:
            print(f"ERROR: No se pudo guardar el pago en la BD: {err}")
            if conn:
                conn.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                close_conn(conn)