from flask import Flask, jsonify
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('main.html')

@app.route('/list')
def list():
    return render_template('list.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'  # SQLite 데이터베이스 URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # SQLAlchemy의 수정 추적 비활성화
db = SQLAlchemy(app)
usercookies = 0

# 데이터베이스 모델 정의
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=True, nullable=False)
    
# 데이터베이스 모델 정의
class UserSession(db.Model):
    name = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, primary_key = True)

# 데이터베이스 생성
@app.before_first_request
def create_tables():
    db.create_all()
    
# 데이터 추가 엔드포인트
@app.route('/add_user/<name>/<email>', methods=['POST'])
def add_user(name, email):
    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'return': True})

# 로그인 엔드포인트
@app.route('/login/<name>/<password>', methods=['GET'])
def login(name, password):
    users = User.query.all()
    for user in users:
        if user.name == name:
            if user.password == password:
                db.session.add(UserSession(usercookies, user.id))
                usercookies += 1
                return jsonify({'return': True, 'session': usercookies - 1})
            else:
                return  jsonify({'return': False, 'reason': 'Wrong password'})
    return jsonify({'return': False, 'reason': 'No name'})


if __name__ == '__main__':
    app.run(debug=True)


#a.com/users