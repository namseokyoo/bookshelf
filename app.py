from flask import Flask, render_template, jsonify
from dotenv import load_dotenv

from review import req_review

app = Flask(__name__)

@app.route('/')
def welcome():
   return render_template('index.html')


@app.route('/review')
def review():
    url='https://search.daum.net/search?w=bookpage&bookId=532462&q=%ED%94%BC%ED%94%84%ED%8B%B0+%ED%94%BC%ED%94%8C'
    result = req_review(url)
    return jsonify({'result':result})



if __name__=='__main__' :
    app.run('localhost', 5000, debug=True)

    