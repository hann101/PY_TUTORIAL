from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
# mongodb://test:test@localhost
# 13.209.69.252
db = client.dbjungle


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


## API 역할을 하는 부분
@app.route('/memo', methods=['POST'])
def post_save():
    # 1. 클라이언트로부터 데이터를 받기
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    # 3. mongoDB에 데이터 넣기
    memo = {'title': title_receive, 'content': content_receive}
    db.memo.insert(memo)
    return jsonify({'result': 'success'})


@app.route('/memo', methods=['GET'])
def show_post():
    posts = list(db.memo.find({}, {'_id': 0}))

    return jsonify({'result': 'success', 'showAll': posts})


@app.route('/api/delete', methods=['POST'])
def delete_star():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    title_receive = request.form['title_give']
    # 2. mystar 목록에서 delete_one으로 name이 name_receive와 일치하는 star를 제거합니다.
    db.memo.delete_one({'title': title_receive})
    # 3. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success'})


@app.route('/api/repair', methods=['GET'])
def repair_post():
    post = list(db.memo.find({}, {'_id': 0}))

    return jsonify({'result': 'success', 'repair': post})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
