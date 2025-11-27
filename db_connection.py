import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
from mysql_env import HOST, PORT, DATABASE, USER, PASSWORD, POOL_SIZE

class DBConnection:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            try:
                dbconfig = {
                    "host": HOST,
                    "port": int(PORT),
                    "database": DATABASE,
                    "user": USER,
                    "password": PASSWORD,
                    "pool_size": POOL_SIZE
                }
                pool = MySQLConnectionPool(pool_name="hotel_pool", **dbconfig)
                print("Pool de conexiones a MySQL creado exitosamente.")
                cls._instance = pool
            except mysql.connector.Error as err:
                print(f"Error al conectar con MySQL: {err}")
                raise
            except (ValueError, TypeError) as err:
                print(f"Error en configuracion de conexion: {err}")
                raise
        return cls._instance

    def get_connection(self):
        pool = self.get_instance()
        return pool.get_connection()

    def close_connection(self, connection):
        connection.close()

def get_conn():
    return DBConnection.get_instance().get_connection()

def close_conn(connection):
    connection.close()

if __name__ == '__main__':
    try:
        conn_test = get_conn()
        print(f"Conexion de prueba exitosa. ID: {conn_test.connection_id}")
        close_conn(conn_test)
    except Exception as e:
        print(f"CRITICAL: No se pudo inicializar el pool de conexiones a la BD: {e}")