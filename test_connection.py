import os
import psycopg2
from urllib.parse import urlparse

# Obtener la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.environ['DATABASE_URL']
result = urlparse(DATABASE_URL)
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
port = result.port

# Conectar a la base de datos
try:
    conn = psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host=hostname,
        port=port
    )
    cursor = conn.cursor()
    print("Conexión exitosa a la base de datos")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
