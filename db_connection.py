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

# --- Singleton Pattern: Instancia única para toda la aplicación ---
try:
    # Creamos una instancia global que será compartida
    _db_connection_instance = DBConnection()

    def get_conn():
        """Obtiene una conexión del pool global."""
        return _db_connection_instance.get_connection()

    def close_conn(connection):
        """Devuelve una conexión al pool global."""
        _db_connection_instance.close_connection(connection)

except (mysql.connector.Error, ValueError, TypeError) as e:
    print(f"CRITICAL: No se pudo inicializar el pool de conexiones a la BD: {e}")
    # Si la BD no está, las funciones no existirán y la app fallará al importar, lo cual es correcto.
    raise

# Para prueba inicial:
if __name__ == '__main__':
    conn_test = get_conn()
    print(f"Conexión de prueba exitosa. ID: {conn_test.connection_id}")
    close_conn(conn_test)