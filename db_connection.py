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
            self.pool = MySQLConnectionPool(pool_name="hotel_pool", **self.dbconfig)
            print("Pool de conexiones a MySQL creado exitosamente.")
            
        except mysql.connector.Error as err:
            print(f"Error al conectar con MySQL: {err}")
            raise
        except (ValueError, TypeError) as err:
            print(f"Error en configuracion de conexion: {err}")
            raise

    def get_connection(self):
        return self.pool.get_connection()

    def close_connection(self, connection):
        connection.close()

try:
    _db_connection_instance = DBConnection()

    def get_conn():
        return _db_connection_instance.get_connection()

    def close_conn(connection):
        _db_connection_instance.close_connection(connection)

except (mysql.connector.Error, ValueError, TypeError) as e:
    print(f"CRITICAL: No se pudo inicializar el pool de conexiones a la BD: {e}")
    raise

if __name__ == '__main__':
    conn_test = get_conn()
    print(f"Conexion de prueba exitosa. ID: {conn_test.connection_id}")
    close_conn(conn_test)