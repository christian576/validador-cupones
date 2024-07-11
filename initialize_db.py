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
conn = psycopg2.connect(
    database=database,
    user=username,
    password=password,
    host=hostname,
    port=port
)
cursor = conn.cursor()

# Crear la tabla de vouchers
cursor.execute('''
    CREATE TABLE IF NOT EXISTS vouchers (
        code TEXT PRIMARY KEY,
        used INTEGER DEFAULT 0
    );
''')
conn.commit()
cursor.close()
conn.close()

print("Tabla 'vouchers' creada exitosamente.")
