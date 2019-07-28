# 実行方法
#   [Linux] FLASK_APP=ajax_image.py flask run
#   [Windows] SET FLASK_APP=ajax_image.py
#             flask run
#   [URL] http://localhost:5000/?path=/home/user/Pictures/picture1.jpg

from flask import Flask, send_file, request

app = Flask(__name__)

@app.route('/')
def index() :
  path = request.args.get('path', '', type=str)
  return send_file(path, 'image/jpeg')

