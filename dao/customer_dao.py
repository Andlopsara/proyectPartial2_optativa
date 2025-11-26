import mysql.connector
from db_connection import get_conn, close_conn
from customer import Customer
from typing import Optional

class CustomerDAO:
    def create(self, cust: Customer) -> Optional[int]:
        conn = None
        cursor = None
        try:
            conn = get_conn()
            cursor = conn.cursor()

            query = """
                INSERT INTO CUSTOMERS 
                (first_name, second_name, last_name, second_last_name, phone, email, state, curp, password_hash) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                cust.getName(), cust.getSecondName(), cust.getLastName(),
                cust.getSecondLastName(), cust.getPhone(), cust.getEmail(),
                cust.getState(), cust.getCurp(), cust.getPassword()
            )

            cursor.execute(query, values)
            conn.commit()
            
            cust_id = cursor.lastrowid
            cust.setId(cust_id)
            
            print(f"INFO: Cliente '{cust.getName()}' insertado en la BD con ID: {cust_id}")
            return cust_id

        except mysql.connector.Error as err:
            print(f"ERROR: No se pudo crear el cliente en la BD: {err}")
            if conn:
                conn.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                close_conn(conn)

    def get_all(self) -> list[Customer]:
        conn = None
        cursor = None
        customers = []
        try:
            conn = get_conn()
            cursor = conn.cursor()
            query = "SELECT customer_id, first_name, second_name, last_name, second_last_name, phone, email, state, curp, password_hash FROM CUSTOMERS"
            cursor.execute(query)
            records = cursor.fetchall()
            for record in records:
                (cust_id, name, sName, lName, sLName, phone, email, state, curp, password) = record
                customers.append(
                    Customer(cust_id, name, sName, lName, sLName, phone, email, state, curp, password)
                )
            print(f"INFO: Se cargaron {len(customers)} clientes desde la BD.")
        except mysql.connector.Error as err:
            print(f"ERROR: No se pudieron obtener los clientes de la BD: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                close_conn(conn)
        return customers