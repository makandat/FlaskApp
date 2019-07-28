#!/usr/bin/python3
#   http://flask.pocoo.org/
from flask import Flask, render_template
import mysql.connector as MySQL

# Flask 構築
app = Flask(__name__)

# ルート
@app.route('/', methods=["GET", "POST"])
def index_get() :
  # MySQL に接続
  conf = {"user":"user", "password":"ust62kjy", "host":"localhost", "database":"user"}
  client = MySQL.connect(**conf)
  cursor = client.cursor()
  cursor.execute("SELECT id, userid, password, priv, info, registered, expired FROM user.Users")
  return render_template('index7.html', cursor=cursor)


# アプリ実行開始
app.run(host='0.0.0.0')
