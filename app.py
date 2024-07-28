from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xd9\x00\x02I\x19\x1a\xe6(\xb8\xa5\x0c\x9c\xec\xa8\x9c)\x04\xca\xb8\xee\x10\x10\xc1\xff'

@app.route('/')
def home():
    return 'Hola, Mundo!'

if __name__ == '__main__':
    app.run(debug=True)
