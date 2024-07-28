from flask import Flask, jsonify
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/test')
def test():
    return jsonify({"message": "This is a test endpoint"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
