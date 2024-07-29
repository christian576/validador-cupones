from flask import Flask, render_template, request
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "default_secret_key")

@app.route('/')
def index():
    return "Hello, world!"

if __name__ == '__main__':
    app.run()
