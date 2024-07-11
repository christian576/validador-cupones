from flask import Flask, request, jsonify, render_template
import os
import psycopg2
from urllib.parse import urlparse

app = Flask(__name__)

# Conectar a la base de datos PostgreSQL
DATABASE_URL = os.environ['DATABASE_URL']
result = urlparse(DATABASE_URL)
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
port = result.port
conn = psycopg2.connect(
    database=database,
    user=username,
    password=password,
    host=hostname,
    port=port
)
cursor = conn.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validar', methods=['POST'])
def validar():
    code = request.form['code']
    cursor.execute('SELECT used FROM vouchers WHERE code = %s', (code,))
    result = cursor.fetchone()
    if result is None:
        return jsonify({'status': 'error', 'message': 'Código no válido'})
    elif result[0] == 1:
        return jsonify({'status': 'error', 'message': 'Código ya utilizado'})
    else:
        cursor.execute('UPDATE vouchers SET used = 1 WHERE code = %s', (code,))
        conn.commit()
        return jsonify({'status': 'success', 'message': 'Código válido y ahora marcado como utilizado'})

if __name__ == '__main__':
    app.run(debug=True)
