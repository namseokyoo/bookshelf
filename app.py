from flask import Flask, render_template,request,jsonify
from bs4 import BeautifulSoup
import requests
import json
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
KAKAO_API_KEY = os.getenv('KAKAO_API_KEY')

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.


app = Flask(__name__)

@app.route('/')
def welcome():
   return render_template('index.html')




@app.route('/info',methods=['POST'])
def info():
   searchbook = request.form['searchbook']
   search_key = request.form['search_key']
   if search_key == 'title' :
      url="https://dapi.kakao.com/v3/search/book?target=title"
   elif search_key == 'authors':
      url="https://dapi.kakao.com/v3/search/book?target=person"
   elif search_key == 'ISBN' :
      url="https://dapi.kakao.com/v3/search/book?target=isbn"
   
   headers={ 'Authorization' : KAKAO_API_KEY }
   queryString={'query':searchbook}

   data = requests.get(url,headers=headers,params=queryString)
   soup = BeautifulSoup(data.text, 'html.parser')
   books = json.loads(soup.text)

   info=books['documents']

   #book={'title':title,'authors':authors,'contents':contents,'thumbnail':thumbnail}
   #db.books.insert_one(book)
      
   return jsonify({'result':'success','info':info})

@app.route('/bookshelf')
def bookshelf():
   return render_template('fullcalendar.html')


if __name__=='__main__' :
   app.run('localhost', 5005, debug=True)





