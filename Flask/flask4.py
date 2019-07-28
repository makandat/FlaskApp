#!/usr/bin/python3
#   http://flask.pocoo.org/
from flask import Flask, render_template, request, redirect, url_for, session

# アップロード先
SAVEDIR = "/home/user/data"

# Flask 構築
app = Flask(__name__)
# session のキー暗号化のために使用する。
app.secret_key = 'o9H-b5i/+09KeF%j'

# GET のとき
@app.route('/', methods=["GET"])
def index_get() :
  return render_template('index4.html', message="")

# POST のとき
@app.route('/', methods=["POST"])
def index_post() :
  try :
    file1 = request.files['file1']
    saveFileName = SAVEDIR + "/" + file1.filename
    file1.save(saveFileName)
    message="ファイルがアップロードされました。" + saveFileName
  except :
    message="エラーが発生。"
  return render_template('index4.html', message=message)


# アプリ実行開始
app.run(host='0.0.0.0')
