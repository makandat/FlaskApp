#!/usr/bin/python3
#   http://flask.pocoo.org/
from flask import Flask, render_template, request, redirect, url_for, session

# Flask 構築
app = Flask(__name__)
# session のキー暗号化のために使用する。
app.secret_key = 'o9H-b5i/+09KeF%j'

# GET のとき
@app.route('/', methods=["GET"])
def index_get() :
  session['count'] = 0
  return render_template('index3.html', message="", count=0)

# POST のとき
@app.route('/', methods=["POST"])
def index_post() :
  if not 'count' in session :
    return redirect(url_for('index3'))
  count = int(session['count']) + 1
  session['count'] = count
  return render_template('index3.html', message="カウントを増加させました。", count=count)


# アプリ実行開始
app.run(host='0.0.0.0')
