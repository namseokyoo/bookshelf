from flask import Flask, session, render_template, make_response
from uuid import uuid4
from datetime import datetime, timedelta
from flask.sessions import SessionInterface, SessionMixin
from werkzeug.datastructures import CallbackDict

from pymongo import MongoClient


class MongoSession(CallbackDict, SessionMixin):
    def __init__(self, initial=None, sid=None):
        CallbackDict.__init__(self, initial)
        self.sid = sid
        self.modified = False


class MongoSessinoInterface(SessionInterface):
    def __init__(self, host='localhost', port=27017,\
                db='', collection='sessions'):
        client = MongoClient(host, port)
        self.store = client[db][collection]

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if sid:
            stored_session = self.store.find_one({'sid': sid})
            if stored_session:
                if stored_session.get('expiration') > datetime.utcnow():
                    return MongoSession(initial=stored_session['data'],
                                        sid=stored_session['sid'])
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
                            'data': session,
                            'expiration': expiration
                        }, True)
        response.set_cookie(app.session_cookie_name,
                            session.sid,
                            expires=self.get_expiration_time(app, session),
                            httponly=True, domain=domain)

app = Flask(__name__)
app.session_interface = MongoSessinoInterface(db='session')
app.config.update(
    SESSION_COOKIE_NAME='flask_session'
)

@app.route('/')
def welcome():
    res = make_response(render_template('index.html'))
    res.set_cookie(app.session_cookie_name, session.sid)
    return res
    # return "Welcome to myproject"


@app.route('/session_in')
def session_signin():
    print(session.sid)
    title='title'
    session[title] ={title:title}
    return 'Login'


@app.route('/session_out')
def session_signout():
    session.clear()
    return "Signout"


if __name__ == "__main__":
    app.run("localhost", 4000, debug=True)