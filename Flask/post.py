# 実行方法
#   [Linux] FLASK_APP=post.py flask run
#   [Windows] SET FLASK_APP=post.py
#             flask run
#   [URL] http://localhost:5000

from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def index() :
  return "Index Page"

# POST の仕方
#   curl -X POST localhost:5000/login
@app.route('/login', methods=['GET', 'POST'])
def login() :
  if request.method == 'POST':
    return 'POST method'
  else :
    return "GET method"

