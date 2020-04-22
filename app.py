import os
import requests
import json
from flask import Flask, render_template, request, jsonify

from dotenv import load_dotenv
from bs4 import BeautifulSoup
from pymongo import MongoClient

from review import req_review
from bookinfo import req_info
from searchvideo import search_video


load_dotenv()
KAKAO_API_KEY = os.getenv('KAKAO_API_KEY')

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('index.html')


@app.route('/reviews', methods=['POST'])
def review():
    bookurl = request.form['bookurl']
    result = req_review(bookurl)
    return jsonify({'result': 'success', 'review': result})


@app.route('/bookinfo', methods=['POST'])
def bookinfo():
    infourl = request.form['bookurl']
    result = req_info(infourl)
    print(result)
    return jsonify({'result': 'success', 'info': result})    


@app.route('/review')
def review_page():
    book_url=request.query_string
    return render_template('review.html', bookurl=book_url.decode('ascii'))


@app.route('/searchvideo')
def video():
    options = '피프티 피플'
    result = search_video(options)
    return jsonify({'result': 'success', 'searchvideo': result})


@app.route('/info', methods=['POST'])
def info():
    searchbook = request.form['searchbook']
    search_key = request.form['search_key']
    if search_key == 'title':
        url = "https://dapi.kakao.com/v3/search/book?target=title"
    elif search_key == 'authors':
        url = "https://dapi.kakao.com/v3/search/book?target=person"
    elif search_key == 'ISBN':
        url = "https://dapi.kakao.com/v3/search/book?target=isbn"

    headers = {'Authorization': KAKAO_API_KEY}
    queryString = {'query': searchbook}
    data = requests.get(url, headers=headers, params=queryString)

    soup = BeautifulSoup(data.text, 'html.parser')
    books = json.loads(soup.text)
    info = books['documents']
    # book={'title':title,'authors':authors,'contents':contents,'thumbnail':thumbnail}
    # db.books.insert_one(book)
    return jsonify({'result': 'success', 'info': info})


if __name__ == '__main__':
    app.run('localhost', 5005, debug=True)
