# app_module.py
from flask import *
from Py365Lib import FileSystem as fs, WebPage, MySQL, Text, Common
import utilities as util


# flask フォルダ
IMG_FOLDER = "./static/img/"
CSS_FOLDER = "./static/css/"

# static/img フォルダのファイル一覧 
def show_img_folder() :
  files = fs.listFiles(IMG_FOLDER)
  piclist = "<ul>"
  for f in files :
    fname = fs.getFileName(f.decode())
    piclist += "<li><img src=\"{0}\" /> {1}</li>".format(f.decode(), fname)
  piclist += "</ul>"
  return render_template("show_img_folder.html", piclist=piclist)

# static/css/default.css ファイルの内容 
def show_default_css() :
  content = util.showSource(CSS_FOLDER + "default.css", "vs")
  return content

# VW_MANGA などの内容一覧を返す。view はビューの名前 (VW_MANGA, VW_HCG, VW_PIXIV) とする。
def api_pictures_view(view) :
  mysql = MySQL.MySQL()
  rows = mysql.query("SELECT * FROM {0} ORDER BY id".format(view))
  return rows

# 年齢と誕生年の計算
def api_quick_age(convert, year) :
  mysql = MySQL.MySQL()
  if convert == "age" :
    # 年齢から誕生年
    rows = mysql.query("SELECT year, gengo FROM QuickAge WHERE age = {0}".format(year))
    if len(rows) == 0 :
      result = "エラー: 年齢が不正"
    else :
      row = rows[0]
      result = str(row[0]) + "," + row[1]
  elif convert == "born" :
    # 誕生年から年齢
    if Text.isdigit(year) :
      # age は西暦
      rows = mysql.query("SELECT age FROM QuickAge WHERE year={0}".format(year))
      if len(rows) == 0 :
        result = "エラー: 西暦が不正"
      else :
        result = rows[0]
    else :
      # year は和暦
      if year.startswith('T') :
        year = "大正" + Text.substring(year, 1) + "年";
      elif year.startswith('S') :
        if Text.substring(year, 1) == '1' :
          year = "昭和元年";
        else :
          year = "昭和" + Text.substring(year, 1) + "年";
      elif year.startswith('H') :
        if Text.substring(year, 1) == '1' :
          year = "平成元年";
        else :
          year = "平成" + Text.substring(year, 1) + "年";
      elif year.startswith('R') :
        if Text.substring(year, 1) == '1' :
          year = "令和元年"
        else :
          year = "令和" + Text.substring(year, 1) + "年";
      else :
        result = "エラー: 和暦文字が不正"
        return result
      print(year)
      rows = mysql.query("SELECT age FROM QuickAge WHERE gengo='{0}'".format(year))
      if len(rows) == 0 :
        result = "エラー: 和暦が不正"
      else :
        result = rows[0]     
  else :
    # エラー
    result = "エラー: 不正な変換"
  return result


# Videos テーブルをクエリーする。
def api_videos() :
  mysql = MySQL.MySQL()
  sql = "SELECT * FROM Videos"
  rows = mysql.query(sql)
  return rows

# Video テーブルのタイトル変更
def api_video_modify(data) :
  result = "Error"
  mysql = MySQL.MySQL()
  if "id" in data.keys() :
    print("api newstring = " + str(data['newstring']))
    sql = "CALL VideoSetTitle({0}, '{1}')".format(data['id'], data['newstring'])
    mysql.execute(sql)
    result = "OK"
  elif "oldstring" in data.keys() :
    sql = "CALL VideoModifyTitle('{0}', '{1}')".format(data['oldstring'], data['newstring'])
    mysql.execute(sql)
    result = "OK"
  else :
    pass
  return result
  
# BINDATA テーブルから指定された id の画像を取り出して応答として返す。
def api_bindata_extract(id) :
  mysql = MySQL.MySQL()
  sql = f"SELECT datatype, hex(data) as hex FROM BINDATA WHERE id={id}"
  rows = mysql.query(sql)
  row = rows[0]
  datatype = row[0]
  data = row[1]
  if datatype == ".jpg" :
    mime = b"image/jpeg"
  elif datatype == ".png" :
    mime = b"image/png"
  elif datatype == ".gif" :
    mime = b"image/gif"
  else :
    return None
  imgbinary = hex2bin(data)
  response = make_response(imgbinary)
  response.headers.set('Content-Type', mime)
  return response
    
# ヘキサ文字列をバイナリに変換する。
def hex2bin(data) :
  i = 0
  n = len(data)
  buff = list()
  for c in data :
    if  i % 2 == 1 :
      b = 16 * util.nibble(c0) + util.nibble(c)
      buff.append(b)
    else :
      c0 = c
    i += 1
  return bytes(buff)

# 指定したフォルダ内の画像ファイルを縮小する。
def api_image_resize(folder, size) :
  files = fs.listFiles(folder, asstr=True)
  count = 0
  try :
    for f in files :
      ext = Text.tolower(fs.getExtension(f))
      if ext in [".jpg", ".jpeg", ".png", ".gif"] :
        util.resizeImage(f, size)
        count += 1
  except Exception as e:
    print(str(e))
  return count

# 指定したフォルダ内の画像ファイルを BINDATA テーブルに挿入する。
def api_bindata_insert(folder) :
  files = fs.listFiles(folder, asstr=True)
  count = 0
  try :
    for f in files :
      ext = Text.tolower(fs.getExtension(f))
      if ext in [".jpg", ".jpeg", ".png", ".gif"] :
        util.insertBinaries(f)
        count += 1
  except Exception as e :
    print(str(e))
  return count
