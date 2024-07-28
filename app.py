from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
from generar_cupones import generar_cupones

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

def get_db_connection():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
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
        if username == os.environ['USERNAME'] and password == os.environ['PASSWORD']:
            session['logged_in'] = True
            return redirect(url_for('generar'))
        else:
            flash('Credenciales incorrectas')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/generar', methods=['GET', 'POST'])
def generar():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        generar_cupones()
        flash('Cupones generados con éxito!')
        return redirect(url_for('generar'))
    return render_template('generar.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

