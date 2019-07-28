#!/usr/bin/python3
#   http://flask.pocoo.org/
from flask import Flask, render_template, request, redirect, url_for

# Flask 構築
app = Flask(__name__)

# GET のとき
@app.route('/', methods=["GET"])
def index_get() :
  return render_template('index2.html', title='flask テスト', message="")

# POST のとき
@app.route('/', methods=["POST"])
def index_post() :
  result = ""
  try :
    # text1
    result += ("text1=" + request.form['text1'])
  except :
    result += "No_text1"
  try :
    # check1
    result += (" check1=" + request.form['check1'])
  except :
    result += " No_check1"
  try :
    # radio1
    result += (" radio1=" + request.form['radio1'])
  except :
    result += " No_radio1"
  try :
    # select1
    result += (" select1=" + request.form['select1'])
  except :
    result += " No_select1"
  # message として result を返す。
  return render_template('index2.html', title='flask テスト', message=result)

# アプリ実行開始
app.run(host='0.0.0.0')
