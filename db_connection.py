# db_connection.py
import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
from mysql_env import HOST, PORT, DATABASE, USER, PASSWORD, POOL_SIZE

class DBConnection:
    def __init__(self):
        try:
            self.dbconfig = {
                "host": HOST,
                "port": int(PORT),
                "database": DATABASE,
                "user": USER,
                "password": PASSWORD,
                "pool_size": POOL_SIZE
            }
            # Crea un pool de conexiones para reutilizar las conexiones
            self.pool = MySQLConnectionPool(pool_name="hotel_pool", **self.dbconfig)
            print("Pool de conexiones a MySQL creado exitosamente.")
            
        except mysql.connector.Error as err:
            print(f"Error al conectar con MySQL: {err}")
            raise
        except (ValueError, TypeError) as err:
            print(f"Error en configuración de conexión: {err}")
            raise

    def get_connection(self):
        # Obtiene una conexión del pool
        return self.pool.get_connection()

    def close_connection(self, connection):
        # Devuelve la conexión al pool
        connection.close()

# Para prueba inicial:
if __name__ == '__main__':
    try:
        db = DBConnection()
        conn = db.get_connection()
        print(f"Conexión exitosa. ID de conexión: {conn.connection_id}")
        db.close_connection(conn)
    except (ValueError, TypeError, mysql.connector.Error) as e:
        print(f"Fallo la prueba de conexión: {e}")