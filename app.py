from flask import Flask, render_template, request, jsonify, flash, session
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.bko1xj3.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

# create a session object
app.secret_key = 'secret_key'

# 메인 홈페이지 출력
@app.route('/')
def home():
    return render_template('login.html')

# 검색 페이지 출력
@app.route('/list')
def login_finish():
    return render_template('list.html')

@app.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        username = request.form["username_give"]
        password = request.form["password_give"]
        print(username, password)
        user_info = db.join.find_one({'id': username, 'pw': password}, {'_id': False})
        print(user_info)
        # 아이디 혹은 비번이 맞지 않을 때
        if user_info == None:
            return jsonify({"msg": '존재하지않는 회원입니다.'})
        # 아이디 비번 모두 맞을 때
        elif user_info['id'] == username:
            if user_info['pw'] == password:
                session['user_id'] = username
                return jsonify({"msg": "로그인이 되었습니다."})

# 로그인 상태 체크
@app.route('/check', methods = ["GET"])
def check():
    user_id = session.get('user_id')
    if user_id:
            data = {
                "id": user_id
            }
            return jsonify({"result": data["id"]})
    else:
            return jsonify({"msg": "로그인이 필요합니다."})

# 로그아웃 기능
@app.route('/logout', methods = ["POST"])
def logout():
    session.pop('user_id', None)
    msg = "로그아웃 성공"
    return msg
    
@app.route("/join", methods=["POST", "GET"])
def join_post():
    
    if request.method == "GET":
        return render_template("join.html")

    else:
        name_receive = request.form['name_give']
        id_receive = request.form['id_give']
        pw_receive = request.form['pw_give']
        pw2_receive = request.form['pw2_give']
        nickname_receive = request.form['nickname_give']

        existing_user = db.join.find_one({'id': id_receive})
        existing_nickname = db.join.find_one({'nickname': nickname_receive})

        if existing_user:
            return jsonify({'msg': '중복된 아이디 입니다'})
        elif existing_nickname:
            return jsonify({'msg': '중복된 닉네임 입니다'})


        doc = {
            'name': name_receive, 
            'id' : id_receive,
            'pw' : pw_receive,
            'pw2' : pw2_receive,
            'nickname' : nickname_receive   
        }
        db.join.insert_one(doc)
        return jsonify({'msg': '회원가입이 되었습니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)