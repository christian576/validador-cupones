from flask import Flask
import os
import psycopg2

app = Flask(__name__)

# Configuración de la clave secreta
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Configuración de la base de datos
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

@app.route('/')
def index():
    return "¡Hola, mundo!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)