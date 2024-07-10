from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Conectar a la base de datos
conn = sqlite3.connect('vouchers.db', check_same_thread=False)
cursor = conn.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validar', methods=['POST'])
def validar():
    code = request.form['code']
    cursor.execute('SELECT used FROM vouchers WHERE code = ?', (code,))
    result = cursor.fetchone()
    if result is None:
        return jsonify({'status': 'error', 'message': 'Código no válido'})
    elif result[0] == 1:
        return jsonify({'status': 'error', 'message': 'Código ya utilizado'})
    else:
        cursor.execute('UPDATE vouchers SET used = 1 WHERE code = ?', (code,))
        conn.commit()
        return jsonify({'status': 'success', 'message': 'Código válido y ahora marcado como utilizado'})

if __name__ == '__main__':
    app.run(debug=True)
