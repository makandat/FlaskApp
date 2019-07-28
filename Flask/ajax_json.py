# 実行方法
#   [Linux] FLASK_APP=ajax_json.py flask run
#   [Windows] SET FLASK_APP=ajax_json.py
#             flask run
#   [URL] http://localhost:5000
#   [TEST] curl http://localhost:5000/add_numbers?a=15&b=80

from flask import Flask, render_template, jsonify, request
import logging

app = Flask(__name__)

@app.route('/')
def index() :
  return render_template("ajax_json.html")

@app.route('/add_numbers')
def add_numbers() :
  a = request.args.get('a', 0, type=int)
  b = request.args.get('b', 0, type=int)
  app.logger.info(str(a) + "+" + str(b))
  return jsonify(result=a + b)
