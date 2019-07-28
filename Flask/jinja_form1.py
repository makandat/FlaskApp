#
# 実行方法
#   FLASK_APP=jinja_form1.py flask run
#
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if 'check1' in request.form.keys() :
          return render_template('jinja_form1.html', data=request.form['text1'] + request.form['check1'])
        else :
          return render_template('jinja_form1.html', data=request.form['text1'])
    else :
        return render_template('jinja_form1.html', data="")

