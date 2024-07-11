from flask import Flask, request, render_template, redirect, url_for, flash
import psycopg2
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para usar flash messages

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

if __name__ == '__main__':
    app.run(debug=True)
