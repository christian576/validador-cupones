from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask on Railway!"

@app.route('/test')
def test():
    return "This is a test endpoint."

if __name__ == "__main__":
    app.run()
