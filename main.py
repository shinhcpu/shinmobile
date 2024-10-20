from flask import Flask, jsonify, session, request, flash
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.secret_key = '0000'  # 안전한 비밀 키를 설정합니다.
# SQLite 데이터베이스 URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
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
    return render_template('gatong.html')


@app.route('/list')
def list():
    return render_template('list.html')


@app.route('/login')
def login():
    return render_template('login.html')


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
    users = User.query.all()
    for user in users:
        if name == user.name:
            return jsonify({'return': False, 'exist': True}), 200

    new_user = User()
    new_user.name = name
    new_user.password = password
    db.session.add(new_user)
    return jsonify({'return': True, 'exist': False}), 200

# login


@app.route('/try_login/<name>/<password>', methods=['GET'])
def login_get(name, password):
    users = User.query.all()
    for user in users:
        if user.name == name:
            if user.password == password:
                session['username'] = user.name
                return jsonify({'return': True}), 200
            else:
                return jsonify({'return': False, 'reason': 'WrongPassword'}), 200
    return jsonify({'return': False, 'reason': 'NoSuchName'}), 200


if __name__ == '__main__':
    # intialize
    app.before_request(create_tables)
    app.run(debug=True)
