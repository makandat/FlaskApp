# utitlities.py
from flask import *
from Py365Lib import FileSystem as fs, Common, Text, MySQL, WebPage
from xml.sax.saxutils import escape
from pprint import pprint

# 複数行文字列を表示する。
def show_text(filePath, title="") :
  if title == "" :
    title = "show_text"
  buf = """<!doctype html>
<html>
<head>
 <meta charset="utf-8" />
 <title>"""
  buf += title
  buf += """</title>
</head>
<body>
<h1 style='text-align:center;'>"""
  buf += title
  buf += """</h1>
<br />
<pre style='margin-left:5%;'>
  """
  buf += escape(fs.readAllText(filePath))
  buf += """</pre>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
</body>
</html>
  """
  return buf

# 引用符で文字列を囲む。
def quote(s, q='"') :
  return q + str(s) + q

# None だったら "" に変換する。
def none2sp(s) :
  return ("" if s == None else s)

# None だったら null に変換する。
def none2null(s) :
  return ("null" if s == None else s)

# ニブルに変換する。
def nibble(c) :
  n = ord(c)
  if n >= 0x3a :
    n -= 0x41
    n += 10
  else :
    n -= 0x30
  return n




# バイナリーファイル filePath をテーブル BINDATA に挿入する。
def insertBinaries(filePath) :
  INSERT = "INSERT INTO BINDATA(`title`, `original`, `datatype`, `data`, `info`, `size`) VALUES('{0}', '{1}', '{2}', {3}, '', {4})"
  ext = fs.getExtension(filePath)
  size = fs.getFileSize(filePath)
  fileName = fs.getFileName(filePath)
  filePath = filePath.replace("\\", "/")
  filePath = filePath.replace("'", "''")
  hexa = bin2hex(filePath)
  sql = Text.format(INSERT, fileName, filePath, ext, hexa, size)
  client = MySQL.MySQL()
  client.execute(sql)
  return

# バイナリーファイルをヘキサに変換する。
def bin2hex(filePath) :
  buff = "0x"
  b = fs.readBinary(filePath)
  buff += b.hex()
  return buff


# 画像ファイルのサイズを変更する。
def resizeImage(filePath, size) :
  cmd = ["mogrify", "-resize", size, filePath]
  Common.exec(cmd)
  return

# プログラム・ソースを表示する。
def showSource(filePath, style="default") :
  text = fs.readAllText(filePath)
  source = WebPage.WebPage.escape(text)
  title = fs.getFileName(filePath)
  return render_template("showSource.html", source=source, title=title, style=style)

