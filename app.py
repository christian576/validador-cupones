import os
from flask import Flask, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# Conexión a la base de datos
DATABASE_URL = os.environ.get('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

@app.route('/')
def index():
    return 'Hello, world!'

@app.route('/test')
def test():
    return jsonify({"message": "API is working"}), 200

if __name__ == '__main__':
    app.run(debug=True)

