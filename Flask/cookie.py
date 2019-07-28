#
# 実行方法
#   FLASK_APP=cookie.py flask run
#
from flask import Flask, request, render_template, make_response

app = Flask(__name__)

@app.route('/')
def index() :
  if 'count' in request.cookies.keys() :
    count = int(request.cookies['count'])
    count += 1
  else :
    count = 0
  resp = make_response(render_template('jinja_cookie.html', count=str(count)))
  resp.set_cookie('count', str(count))
  return resp

