from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('main.html')

@app.route('/list')
def list():
    return render_template('list.html')

if __name__ == '__main__':
    app.run()