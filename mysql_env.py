from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv("DB_HOST", "localhost")
PORT = int(os.getenv("DB_PORT", "3306"))
DATABASE = os.getenv("DB_NAME", "hotel_le_villa")
USER = os.getenv("DB_USER", "root")
PASSWORD = os.getenv("DB_PASSWORD", "")
POOL_SIZE = int(os.getenv("POOL_SIZE", "5"))

if not HOST or not DATABASE or not USER:
    raise ValueError("Variables de entorno criticas no configuradas: DB_HOST, DB_NAME, DB_USER son obligatorias.")