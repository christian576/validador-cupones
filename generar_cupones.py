import qrcode
import uuid
import sqlite3
import os

# Crear carpeta para almacenar QR codes si no existe
if not os.path.exists('static/qrs'):
    os.makedirs('static/qrs')

# Conectar a la base de datos
conn = sqlite3.connect('vouchers.db')
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS vouchers (
        code TEXT PRIMARY KEY,
        used INTEGER DEFAULT 0
    )
''')

# Función para generar un código único y un QR
def generar_qr():
    code = str(uuid.uuid4())
    qr = qrcode.make(code)
    qr.save(f'static/qrs/{code}.png')
    cursor.execute('INSERT INTO vouchers (code) VALUES (?)', (code,))
    conn.commit()
    return code

# Generar N códigos y QR
N = 10  # Por ejemplo, generar 10 códigos
for _ in range(N):
    generar_qr()

print(f"{N} códigos QR generados y guardados en la base de datos.")
