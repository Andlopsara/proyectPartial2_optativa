# dao/service_dao.py

import mysql.connector
from db_connection import get_conn, close_conn
from service import Service # Importa la clase Service
from typing import Optional, List

class ServiceDAO:
    """DAO para la entidad Service."""

    # C - CREATE: Agrega un nuevo servicio al hotel
    def create(self, svc: Service) -> Optional[int]:
        conn = get_conn()
        cursor = conn.cursor()
        
        # Mapeamos service.getType() a la columna 'name' de la BD
        query = """
            INSERT INTO SERVICES 
            (name, cost, description) 
            VALUES (%s, %s, %s)
        """
        values = (
            svc.getType(), svc.getCost(), svc.getDescription()
        )
        
        try:
            cursor.execute(query, values)
            conn.commit()
            svc_id = cursor.lastrowid
            svc.setId(svc_id)
            return svc_id
        except mysql.connector.Error as err:
            print(f"Error CREATE Service: {err}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            close_conn(conn)

    # R - READ: Obtiene un servicio por ID
    def get_by_id(self, service_id: int) -> Optional[Service]:
        conn = get_conn()
        cursor = conn.cursor()
        
        query = "SELECT service_id, name, cost, description FROM SERVICES WHERE service_id = %s"
        
        try:
            cursor.execute(query, (service_id,))
            record = cursor.fetchone()
            
            if record:
                # Mapeo: service_id, name (type), cost, description
                (id, type_name, cost, description) = record
                # Notar que 'name' de la BD se convierte en 'type' del objeto Service
                return Service(id, type_name, cost, description)
            return None
        except mysql.connector.Error as err:
            print(f"Error READ Service: {err}")
            return None
        finally:
            cursor.close()
            close_conn(conn)

    # R - READ ALL: Obtiene todos los servicios
    def get_all(self) -> List[Service]:
        conn = get_conn()
        cursor = conn.cursor()
        
        query = "SELECT service_id, name, cost, description FROM SERVICES"
        services = []
        
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            
            for id, type_name, cost, description in records:
                services.append(Service(id, type_name, cost, description))
            return services
        except mysql.connector.Error as err:
            print(f"Error READ ALL Services: {err}")
            return []
        finally:
            cursor.close()
            close_conn(conn)

    # D - DELETE: Elimina un servicio
    def delete(self, service_id: int) -> bool:
        conn = get_conn()
        cursor = conn.cursor()
        query = "DELETE FROM SERVICES WHERE service_id = %s"
        
        try:
            cursor.execute(query, (service_id,))
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            # Si el servicio está referenciado en otra tabla (RESERVATION_SERVICES), fallará por Foreign Key.
            print(f"Error DELETE Service: {err}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            close_conn(conn)