import mysql.connector
from db_connection import get_conn, close_conn
from service import Service
from typing import Optional, List

class ServiceDAO:

    def create(self, svc: Service) -> Optional[int]:
        conn = None
        cursor = None
        
        query = """
            INSERT INTO SERVICES 
            (name, cost, description) 
            VALUES (%s, %s, %s)
        """
        values = (
            svc.getType(), svc.getCost(), svc.getDescription()
        )
        
        conn = None
        try:
            conn = get_conn()
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                conn.commit()
                svc_id = cursor.lastrowid
                svc.setId(svc_id)
                return svc_id
        except mysql.connector.Error as err:
            print(f"Error CREATE Service: {err}")
            if conn:
                conn.rollback()
            return None
        finally:
            if conn:
                close_conn(conn)

    def get_by_id(self, service_id: int) -> Optional[Service]:
        conn = get_conn()
        cursor = conn.cursor()
        
        query = "SELECT service_id, name, cost, description FROM SERVICES WHERE service_id = %s"
        
        try:
            cursor.execute(query, (service_id,))
            record = cursor.fetchone()
            
            if record:
                (id, type_name, cost, description) = record
                return Service(id, type_name, cost, description)
            return None
        except mysql.connector.Error as err:
            print(f"Error READ Service: {err}")
            return None
        finally:
            cursor.close()
            close_conn(conn)

    def get_all(self) -> List[Service]:
        conn = None
        cursor = None
        services = []
        query = "SELECT service_id, name, cost, description FROM SERVICES"
        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute(query)
            records = cursor.fetchall()
            for id, type_name, cost, description in records:
                services.append(Service(id, type_name, cost, description))
            print(f"INFO: Se cargaron {len(services)} servicios desde la BD.")
        except mysql.connector.Error as err:
            print(f"Error READ ALL Services: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                close_conn(conn)
        return services

    def delete(self, service_id: int) -> bool:
        conn = get_conn()
        cursor = conn.cursor()
        query = "DELETE FROM SERVICES WHERE service_id = %s"
        
        try:
            cursor.execute(query, (service_id,))
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Error DELETE Service: {err}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            close_conn(conn)