#
#  実行方法
#    FLASK_APP=session.py flask run
#
from flask import Flask, request, session, render_template

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/', methods=['GET', 'POST'])
def index() :
  if request.method == 'POST' :
    new_value = request.form['value']
    if 'value' in session :
      old_value = session['value']
      session['value'] = new_value
    else :
      old_value = "undef"
      session['value'] = old_value
    return render_template('jinja_session.html', value="{0} => {1}".format(old_value, new_value))
  else :
    return render_template('jinja_session.html', value="")

