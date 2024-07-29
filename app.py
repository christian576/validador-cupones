from flask import Flask

app = Flask(__name__)
import os
port = int(os.environ.get("PORT", 8000))
# Usa 'port' en lugar de 8000 al iniciar tu servidor

@app.route('/')
def index():
    return "Hello, world!"

@app.route('/test')
def test():
    return "This is a test endpoint"

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8000)
