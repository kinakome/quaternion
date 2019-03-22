#numpyとQuaternionの読み込み
import numpy as np
from Quaternion import Quat
#センサの値を代入（今後はセンサから直接値を代入できるように）
w = 6875
x = 468
y = 7031
z = 312
#クォータニオンをwxyz表記するときはw^2 + x^2 + y^2 + z^2 = 1にならないといけない
#センサから出力される値は大きすぎるのでそれぞれaで割ってあげると上記の式を満たすようなaを求める
#(w/a)^2 + (x/a)^2 + (y/a)^2 + (z/a)^2 = 1   =>     a = SQRT(w^2 + x^2 + y^2 + z^2)
a = np.sqrt(w**2 + x**2 + y**2 + z**2)
#aで割ってあげたwxyzをクォータニオン関数に渡す
data = [y/a, x/a, z/a, w/a]
q = Quat(data)
#roll, pitch, yawの順で配列に入れてあげる
rpy = [q.dec,-q.roll,q.ra]
#それぞれ±180度を超える値を取るときは±360度してあげて180度を超えないようにする
for i in range(3):
    if  rpy[i-1] > 180:
        rpy[i-1] -= 360
    elif rpy[i-1] <  -180:
        rpy[i-1] += 360
#結果表示
print(rpy)
