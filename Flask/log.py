#
#  実行方法
#    FLASK_APP=log.py flask run
#
from flask import Flask, request, session
import logging

LOGFILE = "LOGFILE.log"

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(LOGFILE)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
app.logger.addHandler(fh)

@app.route('/')
def index() :
  app.logger.info('session start')
  session['count'] = '0'
  return "Enter URL /log "

@app.route('/log')
def log() :
  count = int(session['count'])
  count += 1
  session['count'] = str(count)
  app.logger.info("log count = " + str(count))
  return "/log " + str(count)
