#!/usr/bin/python3
#   http://flask.pocoo.org/
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

@app.route('/')
def index() :
  return render_template('index1.html', title='flask テスト')

app.debug = True
app.run()  # localhost のみ
#app.run(host='0.0.0.0')  # 外部からもアクセス可能

