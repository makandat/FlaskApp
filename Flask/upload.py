#
# 実行方法
#   FLASK_APP=upload.py flask run
#
from flask import Flask,request, render_template

UPLOAD_DIR = '/home/user/temp/'

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index() :
  if request.method == 'POST' :
    f = request.files['file1']
    f.save(UPLOAD_DIR + f.filename)
    return render_template('jinja_upload.html', message='Uploaded ' + UPLOAD_DIR + f.filename)
  else :
    return render_template('jinja_upload.html', message="")


