# pillow_module.py
from PIL import Image, ImageFilter, ImageOps
from Py365Lib import FileSystem as fs, Common, Text, DateTime
import math

if Common.is_windows() :
  TMP = "C:/temp/"
else :
  TMP = "/tmp/"

# 画像情報
def get_image_info(path) :
  if not fs.exists(path) :
    return path + " does not exists."
  im = Image.open(path)
  res = "format:{0} size:{1} mode:{2}".format(im.format, im.size, im.mode)
  return res

# 画像処理(Resize)
def resize_image(path, percent=50) :
  if percent <= 0 and percent > 100 :
    return "Error: percent must be 0 < p <= 100."
  im = Image.open(path)
  width = im.size[0]
  height = im.size[1]
  rate = percent / 100.0
  new_width = math.floor(width * rate)
  new_height = math.floor(height * rate)
  newim = im.resize((new_width, new_height))
  time = DateTime.DateTime()
  fileName = TMP + str(time.timestamp) + "_" + fs.getFileName(path)
  newim.save(fileName)
  return fileName
  
# 画像処理(Rotate)
def rotate_image(path, angle=0) :
  if angle < -180 and angle > 180 :
    return "Error: angle must be -180 <= p <= 180."
  im = Image.open(path)
  newim = im.rotate(angle)
  time = DateTime.DateTime()
  fileName = TMP + str(time.timestamp) + "_" + fs.getFileName(path)
  newim.save(fileName)
  return fileName

# 画像処理(Convert)
def convert_image(path, mode) :
  im = Image.open(path)
  newim = im.convert(mode)
  time = DateTime.DateTime()
  fileName = TMP + str(time.timestamp) + "_" + fs.getFileName(path)
  newim.save(fileName)
  return fileName

# 画像処理(Mirror)
def mirror_image(path, mode) :
  im = Image.open(path)
  if mode == "mirror" :
    newim = ImageOps.mirror(im)
  elif mode == "flip" :
    newim = ImageOps.flip(im)
  else :
    return "Fatal error"
  time = DateTime.DateTime()
  fileName = TMP + str(time.timestamp) + "_" + fs.getFileName(path)
  newim.save(fileName)
  return fileName

# 画像処理(Crop)
def crop_image(path, left_top, right_bottom) :
  p = left_top.split(",")
  q = right_bottom.split(",")
  xy = (int(p[0]), int(p[1]), int(q[0]), int(q[1]))
  im = Image.open(path)
  newim = im.crop(xy)
  time = DateTime.DateTime()
  fileName = TMP + str(time.timestamp) + "_" + fs.getFileName(path)
  newim.save(fileName)
  return fileName
  