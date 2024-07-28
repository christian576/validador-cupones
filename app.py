from flask import Flask, request, render_template, redirect, url_for, flash, session
import psycopg2
import os
from generar_cupones import generar_cupones  # Asegúrate de que este import esté correcto

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey')  # Configura tu clave secreta en las variables de entorno

DATABASE_URL = os.environ['DATABASE_URL']

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    voucher_code = request.form['voucher_code']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM vouchers WHERE code = %s", (voucher_code,))
    voucher = cur.fetchone()
    cur.close()
    conn.close()

    if voucher:
        flash('Voucher válido. ¡Disfruta tu cena!')
    else:
        flash('Voucher no válido. Por favor, intenta nuevamente.')

    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == os.environ.get('USERNAME', 'admin') and password == os.environ.get('PASSWORD', 'password'):
            session['logged_in'] = True
            return redirect(url_for('generar'))
        else:
            flash('Credenciales incorrectas')
    return render_template('login.html')

@app.route('/generar', methods=['GET', 'POST'])
def generar():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        cantidad = int(request.form['cantidad'])
        generar_cupones(cantidad)  # Asegúrate de que esta función esté definida correctamente en generar_cupones.py
        flash('Cupones generados con éxito!')
        return redirect(url_for('generar'))
    return render_template('generar.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

