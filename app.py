from flask import Flask
import os

app = Flask(__name__)

# Configuración de la aplicación a partir de variables de entorno
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

# Opcional: otras configuraciones si las necesitas
app.config['USERNAME'] = os.environ.get('USERNAME')
app.config['PASSWORD'] = os.environ.get('PASSWORD')

@app.route('/')
def home():
    return "Hello, Flask is up and running!"

if __name__ == '__main__':
    app.run()

