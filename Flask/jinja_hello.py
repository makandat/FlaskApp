#
# 実行方法 (Linux)
#   FLASK_APP=jinja_hello.py flask run
from flask import Flask, render_template

app = Flask(__name__)
 
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('jinja_hello.html', name=name)

