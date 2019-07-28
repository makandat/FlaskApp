#
#  実行方法
#    FLASK_APP=jinja_test.py flask run
#
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index() :
  x1 = 12345
  htm = "<span style='color:red;font-weight=bold;'>SAFE filter</span>"
  value = 'NULL'
  items = ['A', 'B', 'C']
  return render_template('jinja_test.html', x1=x1, htm=htm, value=value, items=items)

