#!/usr/bin/python3
#   http://flask.pocoo.org/
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

# Flask 構築
app = Flask(__name__)
# session のキー暗号化のために使用する。
app.secret_key = 'o9H-b5i/+09KeF%j'

# ルート
@app.route('/', methods=["GET", "POST"])
def index_get() :
  return render_template('index6.html')

# JSON を返す。
@app.route('/add')
def add() :
  a = request.args.get('a', 0, type=int)
  b = request.args.get('b', 0, type=int)
  return jsonify(result=a + b)

# アプリ実行開始
app.run(host='0.0.0.0')
