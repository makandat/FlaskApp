#
# 実行方法
#   FLASK_ENV=development
#   FLASK_APP=app.py
#   flask run
#

from flask import *
from Py365Lib import Text, FileSystem as fs
import app_module

MENU = 'MenuItems.csv'

app = Flask(__name__)

# ルート /
@app.route('/')
def index() :
  title = "Python Flask App"
  app.config.from_pyfile('config.ini')
  app.logger.info(app.config['HOST'])
  app.logger.info(app.config['UID'])
  app.logger.info(app.config['DB'])
  menuitems = getMenuItems()
  return render_template('index.html', title=title, menuitems=menuitems)

# ファイルからメニュー項目を読み込む。
def getMenuItems() :
  menuitems = ""
  menuflag = False
  menufirst = True
  rows = fs.readCsv(MENU, False)
  for row in rows :
    #app.logger.info(row[0] + "," + row[1])
    if Text.isdigit(row[0]) :
      # サブタイトル
      if row[0] != "1" :
        menuitems += "\n</ul>"
      menuitems += "\n<h2>" + row[0] + ". " + row[1] + "</h2>\n<ul>\n"
    else :
      # メニュー項目
      url = row[0]
      text = row[1]
      link = f'<a href="{url}">' + text + "</a>"
      menuitems += "<li>" + link + "</li>\n"
  menuitems += "</ul>\n"
  return menuitems

# static/img フォルダの画像一覧
@app.route("/img")
def show_img_folder() :
  return app_module.show_img_folder()

# static/css/default.css の内容を表示
@app.route("/css")
def show_default_css() :
  return app_module.show_default_css()

# 値をそのまま返す。
@app.route("/api/echo/<value>", methods=['POST', 'GET'])
def api_echo(value) :
  app.logger.info("/api/echo/{0}".format(value))
  return jsonify(value)

# 実行開始
#if __name__ == "__main__" :
#  app.debug = True
#  app.run()

