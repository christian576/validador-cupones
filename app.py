from flask import Flask, render_template, request
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

@app.route('/')
def home():
    return "Hello, Flask on Railway!"

@app.route('/test')
def test():
    return "This is a test endpoint."

if __name__ == "__main__":
    app.run()
