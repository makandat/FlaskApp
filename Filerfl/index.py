#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from Py365Lib import FileSystem as fs, Text, DateTime, Common
from pprint import pprint

app = Flask(__name__)

# ルート
@app.route('/')
def index() :
  home_folder = '"' + fs.getHomeDirectory() + '"'
  orderby = request.args.get("orderby")
  hiddenfile = request.args.get("hiddenfile")
  textview = request.args.get("textview")
  favarray = fs.readAllText("fav_folders.csv")
  return render_template('index.html', version='1.0', home=home_folder, fav_folder=favarray)


# ファイル一覧表示
@app.route("/list_files")
def list_files() :
  folder = request.args.get("folder")
  orderby = request.args.get("orderby")
  hiddenfile = request.args.get("hiddenfile")
  # ディレクトリ一覧
  items1 = []
  folders = fs.listDirectories(folder, asstr=True)
  for f in folders :
    fn = fs.getFileName(f)
    if hiddenfile == 1 :  # 隠しファイルを表示する。
      items1.append(getFileInfo(f))  # すべてのフォルダ
    else :
      if not fn.startswith("."): # 隠しファイル(フォルダ)は表示しない。
        items1.append(getFileInfo(f))
    if orderby == "size" or orderby == "rsize":
      items1 = sortby("name", items1)
    else :
      if len(items1) > 0 :
        items1 = sortby(orderby, items1)
  # ファイル一覧
  files = fs.listFiles(folder, asstr=True)
  items2 = []
  for f in files :
    fn = fs.getFileName(f)
    if hiddenfile == 1 :  # 隠しファイルを表示する。
      items2.append(getFileInfo(f))  # すべてのファイル
    else :
      if not fn.startswith("."): # 隠しファイルは表示しない。
        items2.append(getFileInfo(f))
    if len(items2) > 0 :
      items2 = sortby(orderby, items2)
  # ディレクトリ一覧とファイル一覧を１つのリストにする。
  items = []
  for i in items1 :
    items.append(i)
  for i in items2 :
    items.append(i)
  return jsonify(items)


# ソート
def sortby(orderby, items) :
  if orderby == "name" :
    new_items = sorted(items, key=lambda x: x[6])
  elif orderby == "date" :
    new_items = sorted(items, key=lambda x: x[5])
  elif orderby == "size" :
    new_items = sorted(items, key=lambda x: x[4])
  elif orderby == "rname" :
    new_items = sorted(items, key=lambda x: x[6])
    new_items.reverse()
  elif orderby == "rdate" :
    new_items = sorted(items, key=lambda x: x[5])
    new_items.reverse()
  elif orderby == "rsize" :
    new_items = sorted(items, key=lambda x: x[4])
    new_items.reverse()
  else :
    new_items = []
  return new_items


# テキストファイル表示ページ
@app.route("/text_view")
def text_view() :
  path = request.args.get("path")
  print(path)
  return render_template("text_view.html", textfile=path)

# テキストファイルの内容を返す。
@app.route("/text_content")
def text_content() :
  path = request.args.get("path")
  s = fs.readAllText(path)
  return s

# 画像表示ページ
@app.route("/image_view")
def image_view() :
  path = request.args.get("path")
  print(path)
  return render_template("image_view.html", imagefile=path)

# 画像ファイル(一般ファイルのダウンロードも可能)を返す。
@app.route("/get_image")
def get_image() :
  path = request.args.get("path")
  filename = fs.getFileName(path)
  return send_file(path, as_attachment=True, attachment_filename=filename)

# 検索
@app.route("/find")
def find() :
  folder = request.args.get("folder")
  findstr = request.args.get("findstr")
  files = fs.listDirectories(folder, asstr=True) + fs.listFiles(folder, asstr=True)
  items = []
  for f in files :
    if Text.contain(findstr, f) :
      items.append(getFileInfo(f))
    else :
      pass
  return jsonify(items)

# 操作ページ
@app.route("/command")
def command():
  return render_template("command.html")

# コマンド実行
@app.route("/run_command")
def run_command() :
  c = request.args.get("command")
  cmds = Text.re_split("\s+", c)
  return Common.shell(cmds)

# ファイル操作
@app.route("/file_op")
def file_op() :
  op = request.args.get("operation")
  src = request.args.get("sources")
  dest = request.args.get("destination")

# オプションページ
@app.route("/options")
def options() :
  return render_template("options.html")



# ファイル情報を得る。
def getFileInfo(f) :
  if Common.is_windows() :
    mode = ""
    owner = ""
    group = ""
  else :
    mode = "o{0:o}".format(fs.getAttr(f))
    owner = fs.getOwner(f)
    group = fs.getGroup(f)
  dir_or_link = ""
  if fs.isDirectory(f):
    dir_or_link = "D"
  if fs.isLink(f):
    dir_or_link += "L"
  size = fs.getFileSize(f)
  last = fs.getLastWrite(f)
  filename = fs.getFileName(f)
  item = [mode, dir_or_link, owner, group, size, last, filename]
  return item


# 開始
#  FLASK_APP=index.py flask run
