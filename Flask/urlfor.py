# 実行方法
#   [Linux] FLASK_APP=urlfor.py flask run
#   [Windows] SET FLASK_APP=urlfor.py
#             flask run
#   [URL] http://localhost:5000

from flask import Flask, url_for
app = Flask(__name__)

@app.route('/')
def index() :
  return "Index Page " + url_for('index')

@app.route('/user/<userid>')
def show_userid(userid) :
  return "show_userid = " + url_for('show_userid', userid='tad')

@app.route('/age/<int:age>')
def show_age(age) :
  return "show_age = " + url_for('show_age', age=20)


