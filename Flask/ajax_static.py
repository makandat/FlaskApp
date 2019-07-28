# 実行方法
#   [Linux] FLASK_APP=ajax_static.py flask run
#   [Windows] SET FLASK_APP=ajax_static.py
#             flask run
#   [URL] http://localhost:5000/?file=Python.gif

from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index() :
  file = request.args.get('file', '', type=str)
  return app.send_static_file(file)

