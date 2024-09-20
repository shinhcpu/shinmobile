from flask import Flask, jsonify
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('main.html')

if __name__ == '__main__':
    app.run()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'  # SQLite 데이터베이스 URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # SQLAlchemy의 수정 추적 비활성화
db = SQLAlchemy(app)

# 데이터베이스 모델 정의
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

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

# HTTP GET 요청을 처리하는 엔드포인트
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()  # 모든 사용자 데이터 조회
    users_list = []
    for user in users:
        users_list.append({
            'id': user.id,
            'name': user.name,
            'email': user.email
        })
    return jsonify(users_list)  # JSON으로 응답

if __name__ == '__main__':
    app.run(debug=True)


#a.com/users