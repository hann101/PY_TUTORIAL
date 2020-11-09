from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def home():
    return render_template('index_0.html')


@app.route('/memo', methods=['POST'])
def post_save():
    # 1. 클라이언트로부터 데이터를 받기
    title_receive = request.form['title_give']  # 클라이언트로부터 url을 받는 부분
    content_receive = request.form['content_give']  # 클라이언트로부터 comment를 받는 부분
    alonememo = {'title': title_receive, 'content': content_receive}
    db.alonememos.insert(alonememo)

    # 3. mongoDB에 데이터를 넣기
    # db.articles.insert_one(article)

    return jsonify({'result': 'success', 'msg': 'post연결완료'})


@app.route('/memo', methods=['GET'])
def read_Memos():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기 (Read)
    result = list(db.alonememos.find({}, {'_id': 0}))
    # 2. articles라는 키 값으로 article 정보 보내주기
    return jsonify({'result': 'success', 'alonememos': result})


@app.route('/api/list', methods=['GET'])
def show_memos():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기 (Read)
    result = list(db.alonememos.find({}, {'_id': 0}))
    # 2. articles라는 키 값으로 article 정보 보내주기
    return jsonify({'result': 'success', 'alonememos': result})

@app.route('/api/like', methods=['GET'])
def show_stars():
    # 1. db에서 mystar 목록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬합니다.
    # 참고) find({},{'_id':False}), sort()를 활용하면 굿!
    # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.
		return jsonify({'result': 'success','msg':'list 연결되었습니다!'})

@app.route('/api/delete', methods=['POST'])
def delete_Memo():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    title_receive = request.form['title_give']
    # 2. mystar 목록에서 delete_one으로 name이 name_receive와 일치하는 star를 제거합니다.
    # 3. 성공하면 success 메시지를 반환합니다.
    db.alonememos.delete_one({'title': title_receive})
    return jsonify({'result': 'success'})




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
