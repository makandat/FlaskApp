#
#  実行方法
#    FLASK_APP=redirect.py flask run
#
from flask import Flask, request, redirect, abort, url_for, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index() :
  if request.method == 'POST' :
    if request.form['radio'] == 'r' :
      return redirect(url_for('here'))
    else :
      return abort(401)
  else :
    return render_template('jinja_redirect.html')

@app.route('/here')
def here() :
  return "Jumped here\n"

