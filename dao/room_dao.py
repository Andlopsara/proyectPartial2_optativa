import mysql.connector
from db_connection import get_conn, close_conn
from room import Room
from typing import List, Optional

class RoomDAO:

    def create(self, room: Room) -> Optional[int]:
        conn = None
        cursor = None
        try:
            conn = get_conn()
            cursor = conn.cursor()
            query = "INSERT INTO ROOMS (room_number, room_type, status, cost_per_night, description) VALUES (%s, %s, %s, %s, %s)"
            values = (room.getRoomNumber(), room.getType(), room.getStatus(), room.getCost(), room.getDescription())
            
            cursor.execute(query, values)
            conn.commit()
            
            room_id = cursor.lastrowid
            room.setId(room_id)
            print(f"INFO: Habitacion creada en la BD con ID: {room_id}.")
            return room.getId()
        except mysql.connector.Error as err:
            print(f"ERROR: No se pudo crear la habitacion {room.getId()}: {err}")
            if conn:
                conn.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                close_conn(conn)

    def get_all(self) -> List[Room]:
        conn = None
        cursor = None
        rooms = []
        try:
            conn = get_conn()
            cursor = conn.cursor()
            query = "SELECT room_id, room_number, room_type, status, cost_per_night, description FROM ROOMS"
            cursor.execute(query)
            records = cursor.fetchall()
            for record in records:
                (room_id, room_number, room_type, status, cost, description) = record
                rooms.append(Room(room_id, room_number, room_type, status, cost, description))
            print(f"INFO: Se cargaron {len(rooms)} habitaciones desde la BD.")
        except mysql.connector.Error as err:
            print(f"ERROR: No se pudieron obtener las habitaciones de la BD: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                close_conn(conn)
        return rooms