# 実行方法
#   [Linux] FLASK_APP=route0.py flask run
#   [Windows] SET FLASK_APP=route0.py
#             flask run
#   [URL] http://localhost:5000

from flask import Flask
app = Flask(__name__)

@app.route('/')
def index() :
  return "Index Page"

@app.route('/hello')
def hello() :
  return "Hello World!"
