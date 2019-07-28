#!/usr/bin/python3
#   http://flask.pocoo.org/
from flask import Flask, render_template, request, redirect, url_for, session


# Flask 構築
app = Flask(__name__)
# session のキー暗号化のために使用する。
app.secret_key = 'o9H-b5i/+09KeF%j'

# GET のとき
@app.route('/', methods=["GET", "POST"])
def index_get() :
  return render_template('index5.html', message="")

# 静的な HTML
@app.route('/<string:page_name>/')
def render_static(page_name):
  return render_template('%s.html' % page_name)

# アプリ実行開始
app.run(host='0.0.0.0')
