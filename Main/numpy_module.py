# numpy_module.py
from Py365Lib import Common, FileSystem as fs, Text
import numpy as np
import numpy.linalg as LA


# 配列の基本
def array_basic(dt) :
  if dt == None :
    return ""
  if dt == "int32" :
    arr = np.asarray([[1,2,3],[1,2,3],[1,2,3]], dtype=np.int32)
  elif dt == "int64" :
    arr = np.asarray([[1000000000,2,3],[1,2,3],[1,200000000000,3]], dtype=np.int64)
  elif dt == "float32" :
    arr = np.asarray([[1.1,1.2,1.3],[2.1,2.2,2.3],[3.1,3.2,3.3]], dtype=np.float32)
  elif dt == "float64" :
    arr = np.asarray([[1000000000,2,3],[1,2,3],[1,200000000000,3]], dtype=np.float64)
  else :
    arr = ""
  return str(arr)

# 配列の計算
def array_operation(array_a, array_b, calc) :
  a = np.asarray(Common.from_json(array_a))
  b = np.asarray(Common.from_json(array_b))
  if calc == "add" :
    return str(a + b)
  elif calc == "sub" :
    return str(a - b)
  elif calc == "mul" :
    return str(a * b)
  elif calc == "div" :
    return str(a / b)
  else :
    return str(a.dot(b))

# 関数の計算
def numpy_function(kind, xdata) :
  try :
    x = np.array(xdata)
    if kind == "parabola" :
      return np.power(x, 2).tolist()
    elif kind == "sqrt" :
      return np.sqrt(x).tolist()
    elif kind == "cos" :
      return np.cos(np.deg2rad(x)).tolist()
    elif kind == "sin" :
      return np.sin(np.deg2rad(x)).tolist()
    elif kind == "exp" :
      return np.exp(x).tolist()
    elif kind == "log" :
      return np.log(x).tolist()
    else :
      return xdata
  except :
    return xdata

# 連立一次方程式
def array_simultaneous(coefficients) :
  c = np.array(coefficients)
  ny = c.shape[0]
  nx = c.shape[1]
  a = c[:, 0:nx-1]
  b = c[:, ny]
  y = np.linalg.solve(a, b)
  return y.tolist()
  
# 行列式
def array_determinant(coefficients) :
  a = np.array(coefficients)
  det = LA.det(a)
  return det
  
# 逆行列
def array_inverse(coefficients) :
  a = np.array(coefficients)
  inv = LA.inv(a)
  return inv.tolist()

  
