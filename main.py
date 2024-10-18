from flask import Flask, jsonify, session, request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.secret_key = '0000'  # 안전한 비밀 키를 설정합니다.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'  # SQLite 데이터베이스 URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # SQLAlchemy의 수정 추적 비활성화
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/gatong')
def gatong():
    return render_template('ing.html')

@app.route('/list')
def list():
    return render_template('list.html')

if __name__ == '__main__':
    app.run()

# 데이터베이스 모델
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=True, nullable=False)


# 데이터베이스 생성
def create_tables():
    db.create_all()
    
# signup
@app.route('/add_user/<name>/<password>', methods=['POST'])
def add_user(name, password):
    new_user = User()
    new_user.name = name
    new_user.password = password
    return jsonify({'return': True, 'exist': False}), 200

# login
@app.route('/login/<name>/<password>', methods=['GET'])
def login(name, password):
    users = User.query.all()
    for user in users:
        if user.name == name:
            if user.password == password:
                session['username'] = user.name
                return jsonify({'return': True}), 200
            else:
                return  jsonify({'return': False, 'reason': 'Wrong password'}), 404
    return jsonify({'return': False, 'reason': 'No name'}), 404

if __name__ == '__main__':
    app.run(debug=True)
    
# intialize
app.before_request(create_tables)