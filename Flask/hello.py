# 実行方法
#   [Linux] FLASK_APP=hello.py flask run
#   [Windows] SET FLASK_APP=hello.py
#             flask run
#   [URL] http://localhost:5000

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello() :
  return "Hello World!"

