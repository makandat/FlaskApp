# 実行方法
#   [Linux] FLASK_APP=route1.py flask run
#   [Windows] SET FLASK_APP=route1.py
#             flask run
#   [URL] http://localhost:5000

from flask import Flask
app = Flask(__name__)

@app.route('/')
def index() :
  return "Index Page"

@app.route('/user/<userid>')
def show_userid(userid) :
  return "user id = " + userid

@app.route('/age/<int:age>')
def show_age(age) :
  return "age = " + str(age)

