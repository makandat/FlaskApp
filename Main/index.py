#!/usr/bin/env python3
from flask import *
from Py365Lib import Text, FileSystem as fs, Common
import app_module, numpy_module, pillow_module
from pprint import pprint

MENU = 'MenuItems.csv'
ALARMICON = "/static/img/alarm.svg"
PYTHONICON = "/static/img/Flask256.jpg"

app = Flask(__name__)

# ルート /
@app.route('/')
def index() :
  title = "Python Flask App"
  #Common.init_logger("/home/user/log/FlaskMain.log")
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

# VW_MANGA, VW_HCG, VW_PIXIV の内容を返す。
@app.route("/api/pictures/<view>")
def api_pictures_view(view) :
  app.logger.info("/api/pictures/{0}".format(view))
  return jsonify(app_module.api_pictures_view(view))

# 年齢と誕生年の取得
@app.route("/api/quick_age")
def api_quick_age() :
  convert = request.args.get("convert")
  year = request.args.get("year")
  app.logger.info(convert)
  app.logger.info(year)
  return jsonify(app_module.api_quick_age(convert, year))

# Videos テーブルの表示ページ
@app.route("/videos")
def videos() :
  return render_template("videos.html")
  
# Videos テーブルの表示 API
@app.route("/api/videos")
def api_videos() :
  app.logger.info("/api/videos")
  return jsonify(app_module.api_videos())

# Videos テーブルのタイトル修正 (文字列指定)
@app.route("/videos/modify/substr")
def videos_modify_substr():
  return render_template("videos_modify.html", title="Videos テーブルのタイトル修正 (文字列指定)", v_substr="block", v_id="none")

# Videos テーブルのタイトル修正 (id 指定)
@app.route("/videos/modify/id")
def videos_modify_id():
  return render_template("videos_modify.html", title="Videos テーブルのタイトル修正 (id 指定)", v_substr="none", v_id="block")

# Videos テーブルのタイトル修正 API
@app.route("/api/videos/modify/<xtype>")
def api_videos_modify(xtype) :
  data = {}
  result = "Error"
  if xtype == "substr" :
    data["oldstring"] = request.args.get("oldstring")
    data["newstring"] = request.args.get("newstring")
    result = app_module.api_video_modify(data)
  elif xtype == "id":
    data["id"] = request.args.get("id")
    data["newstring"] = request.args.get("newstring")
    result = app_module.api_video_modify(data)
  else :
    pass
  return jsonify(result=result)

# BINDATA テーブルから指定した id の画像を取り出して返す。
@app.route("/api/bindata/extract/<id>")
def api_bindata_extract(id) :
  return app_module.api_bindata_extract(id)

# 指定フォルダ内の画像ファイルのサイズを縮小する。
@app.route("/api/image_resize")
def api_image_resize() :
  folder = request.args.get("folder")
  size = request.args.get("size")
  return jsonify(count=app_module.api_image_resize(folder, size))

# 指定フォルダ内の画像ファイルを BINDATA テーブルに挿入する。
@app.route("/api/bindata/insert")
def api_bindata_insert() :
  folder = request.args.get("folder")
  return jsonify(count=app_module.api_bindata_insert(folder))

# パスを指定したファイルを返す。
@app.route("/api/send_file")
def api_send_file() :
  path = request.args.get("path")
  if not fs.exists(path) :
    return send_file(ALARMICON)
  filename = fs.getFileName(path)
  return send_file(path, as_attachment=True, attachment_filename=filename)


# NumPy 配列の基本
@app.route("/numpy/array", methods=["POST", "GET"])
def numpy_array() :
  if request.method == "POST" :
    dtype = request.form["dtype"]
  else :
    dtype = None
  return render_template("numpy_array.html", content=numpy_module.array_basic(dtype))

# NumPy 配列の計算
@app.route("/numpy/array/operation", methods=["POST", "GET"])
def numpy_array_operation() :
  if request.method == "POST" :
    array_a = request.form["array_a"]
    array_b = request.form["array_b"]
    calc = request.form["calc"]
    return render_template("numpy_array_operation.html", result=numpy_module.array_operation(array_a, array_b, calc), array_a=array_a, array_b=array_b, kind=calc)
  else :
    return render_template("numpy_array_operation.html", result="", array_a="", array_b="", kind="")

# NumPy 連立一次方程式
@app.route("/numpy/array/simultaneous", methods=["GET", "POST"])
def numpy_simultaneous() :
  if request.method == "POST" :
    coef = request.form["coefficients"]
    coefficients = Common.from_json(coef)
    return render_template("numpy_array_simultaneous.html", result=numpy_module.array_simultaneous(coefficients), coef=coef)
  else :
    return render_template("numpy_array_simultaneous.html", result="", coef="")

# NumPy 行列式
@app.route("/numpy/array/determinant", methods=["GET", "POST"])
def numpy_determinant() :
  if request.method == "POST" :
    coef = request.form["coefficients"]
    coefficients = Common.from_json(coef)
    return render_template("numpy_array_determinant.html", result=numpy_module.array_determinant(coefficients), coef=coef)
  else :
    return render_template("numpy_array_determinant.html", result="", coef="")

# NumPy 逆行列
@app.route("/numpy/array/inverse", methods=["GET", "POST"])
def numpy_inverse() :
  if request.method == "POST" :
    coef = request.form["coefficients"]
    coefficients = Common.from_json(coef)
    return render_template("numpy_array_inverse.html", result=numpy_module.array_inverse(coefficients), coef=coef)
  else :
    return render_template("numpy_array_inverse.html", result="", coef="")



    
# Pillow 画像情報
@app.route("/pillow/info", methods=["POST", "GET"])
def pillow_info() :
  if request.method == "POST" :
    path = request.form["path"]
    return render_template("get_image_info.html", result=pillow_module.get_image_info(path), path=path)
  else :
    defaulticon = fs.getCurrentDirectory() + PYTHONICON
    return render_template("get_image_info.html", result="", path=defaulticon)

# Pillow 画像処理 Resize
@app.route("/pillow/resize", methods=["POST", "GET"])
def pillow_resize() :
  if request.method == "POST" :
    path = request.form["path"]
    percent = int(request.form["percent"])
    return render_template("pillow_resize.html", result=pillow_module.resize_image(path, percent), path=path, percent=percent)
  else :
    defaulticon = fs.getCurrentDirectory() + PYTHONICON
    return render_template("pillow_resize.html", result=defaulticon, path=defaulticon, percent="")

# Pillow 画像処理 Rotate
@app.route("/pillow/rotate", methods=["POST", "GET"])
def pillow_rotate() :
  if request.method == "POST" :
    path = request.form["path"]
    angle = int(request.form["angle"])
    return render_template("pillow_rotate.html", result=pillow_module.rotate_image(path, angle), path=path, angle=angle)
  else :
    defaulticon = fs.getCurrentDirectory() + PYTHONICON
    return render_template("pillow_rotate.html", result=defaulticon, path=defaulticon, angle="")


# Pillow 画像処理 Convert
@app.route("/pillow/convert", methods=["POST", "GET"])
def pillow_convert() :
  if request.method == "POST" :
    path = request.form["path"]
    mode = request.form["mode"]
    if mode == "LA" and fs.getExtension(path) == ".jpg" :
      return "Error: JPEG は LA を使用できません。"
    return render_template("pillow_convert.html", result=pillow_module.convert_image(path, mode), path=path, mode=mode)
  else :
    defaulticon = fs.getCurrentDirectory() + PYTHONICON
    return render_template("pillow_convert.html", result=defaulticon, path=defaulticon, mode="")

# Pillow 画像処理 Miller
@app.route("/pillow/mirror", methods=["POST", "GET"])
def pillow_mirror() :
  if request.method == "POST" :
    path = request.form["path"]
    mode = request.form["mode"]
    return render_template("pillow_mirror.html", result=pillow_module.mirror_image(path, mode), path=path, mode=mode)
  else :
    defaulticon = fs.getCurrentDirectory() + PYTHONICON
    return render_template("pillow_mirror.html", result=defaulticon, path=defaulticon, mode="")

# Pillow 画像処理 Crop
@app.route("/pillow/crop", methods=["POST", "GET"])
def pillow_crop() :
  if request.method == "POST" :
    left_top = request.form["left_top"]
    right_bottom = request.form["right_bottom"]
    path = request.form["path"]
    return render_template("pillow_crop.html", result=pillow_module.crop_image(path, left_top, right_bottom), path=path, left_top=left_top, right_bottom=right_bottom)
  else :
    defaulticon = fs.getCurrentDirectory() + PYTHONICON
    return render_template("pillow_crop.html", result=defaulticon, path=defaulticon, left_top="", right_bottom="")



# Chart.js 基本 (棒グラフ)
@app.route("/chart/basic/bar")
def chart_basic_bar() :
  return render_template("chart_basic_bar.html")

# Chart.js 基本 (折れ線グラフ)
@app.route("/chart/basic/line")
def chart_basic_line() :
  return render_template("chart_basic_line.html")

# Chart.js 関数のグラフ
@app.route("/chart/function")
def chart_function() :
  return render_template("chart_numpy_function.html")

# Chart.js 用の API
@app.route("/api/numpy/function")
def api_numpy_function() :
  kind = request.args.get("kind")
  xdata = Common.from_json("[" + request.args.get("xdata") + "]")
  result = numpy_module.numpy_function(kind, xdata)
  return jsonify(result)


# 実行開始
if __name__ == "__main__" :
  app.debug = True
  app.run()

