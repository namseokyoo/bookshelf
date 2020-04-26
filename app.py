
import os
import requests
import json
from flask import Flask, render_template, request, jsonify, session, make_response
from uuid import uuid4
from datetime import datetime, timedelta
from flask.sessions import SessionInterface, SessionMixin
from werkzeug.datastructures import CallbackDict

from dotenv import load_dotenv
from bs4 import BeautifulSoup
from pymongo import MongoClient

from review import req_review
from bookinfo import req_info
from searchvideo import search_video


load_dotenv()
KAKAO_API_KEY = os.getenv('KAKAO_API_KEY')
HOST = os.getenv('HOST', '0.0.0.0')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

# >>> client = MongoClient('example.com',
# …                      username='user',
# …                      password='password',
# …                      authSource='the_database',
# …                      authMechanism='SCRAM-SHA-1')

client = MongoClient(HOST,
                    27017,
                    username=USERNAME,
                    password=PASSWORD,
                    authMechanism='SCRAM-SHA-1')
db = client.session

app = Flask(__name__)


class MongoSession(CallbackDict, SessionMixin):
    def __init__(self, initial=None, sid=None):
        CallbackDict.__init__(self, initial)
        self.sid = sid
        self.modified = False


class MongoSessinoInterface(SessionInterface):
    def __init__(self, host='localhost', port=27017,\
                db='', collection='sessions'):
        # client = MongoClient(host, port) 
        self.store = client[db][collection]

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if sid:
            stored_session = self.store.find_one({'sid': sid})
            if stored_session:
                if stored_session.get('expiration') > datetime.utcnow():
                    return MongoSession(initial=stored_session.get('books',None),
                                        sid=stored_session.get('sid', None))
        sid = str(uuid4())
        return MongoSession(sid=sid)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if session is None:
            response.delete_cookie(app.session_cookie_name, domain=domain)
            return
        if  self.get_expiration_time(app, session):
            expiration = self.get_expiration_time(app, session)
        else:
            expiration = datetime.utcnow() +  timedelta(hours=1)

        self.store.update({'sid': session.sid}, {
                            'sid': session.sid,
                            'books': session,
                            'expiration': expiration
                        }, True)
        response.set_cookie(app.session_cookie_name,
                            session.sid,
                            expires=self.get_expiration_time(app, session),
                            httponly=True, domain=domain)


app.session_interface = MongoSessinoInterface(db='session')
app.config.update(
    SESSION_COOKIE_NAME='flask_session'
)


@app.route('/')
def welcome():
    res = make_response(render_template('index.html'))
    # res.set_cookie(app.session_cookie_name, session.sid)
    return res
    


@app.route('/session_in', methods=['GET','POST'])
def session_signin():
    title = request.args.get('title')
    url = request.args.get('url')
    rating= request.args.get('rating')
    sid = session.sid
    print(session.sid)
    session[title]= {'title':title, 'url':url, 'rating':rating}
    #print(session)
    event = list(db.sessions.find({'sid':sid},{'_id':0}))
    return jsonify({'result':'success', 'event':event})


@app.route('/session_out')
def session_signout():
    session.clear()
    return "Signout"


@app.route('/reviews', methods=['POST'])
def review():
    bookurl = request.form['bookurl']
    result = req_review(bookurl)
    return jsonify({'result': 'success', 'review': result})


@app.route('/bookinfo', methods=['POST'])
def bookinfo():
    infourl = request.form['bookurl']
    result = req_info(infourl)
    #print(result)
    return jsonify({'result': 'success', 'info': result})    


@app.route('/review')
def review_page():
    book_url=request.query_string
    return render_template('review.html', bookurl=book_url.decode('ascii'))


@app.route('/searchvideo', methods=['POST'])
def video():
    options = request.form['booktitle']
    result = search_video(options)
    return jsonify({'result': 'success', 'searchvideo': result})

@app.route('/bookshelf')
def bookshelf():
   return render_template('fullcalendar.html')

@app.route('/bookshelflist')
def addShelf():
    sid = session.sid
    event = list(db.sessions.find({'sid':sid},{'_id':0}))
    #print(event)
    return jsonify({'result':'success','event':event})

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
    port = os.getenv('PORT', 5005)
    app.run('0.0.0.0', port,  debug=True)
