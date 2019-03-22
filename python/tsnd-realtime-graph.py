#coding: utf-8
import matplotlib.pyplot as plt
import os
import sys
import serial
import time
import struct
import binascii
import ctypes
import numpy as np
import time
import threading
import concurrent.futures
# import math
# from matplotlib import pyplot as plt
from Quaternion import Quat

# from matplotlib import pyplot as plt
class TSND151:
  def __init__(self): # 初期化： インスタンス作成時に自動的に呼ばれる
    self.ser = serial.Serial(port='/dev/tty.TSND151-AP09181039-Blue', timeout=0.07, baudrate=115200)
    # 5ms   20    1

    self.str = 0
    self.quartW = 0
    self.quartX = 0
    self.quartY = 0
    self.quartZ = 0
    self.quat = [1,1,1,1]
    self.rpy = [0,0,0]
    print(self.ser)
    # self.count = 0

  def sendQuat(self):
    self.ser.read(1000)
    # クォータニオン計測設定
    header = (0x9A).to_bytes(1, 'little')
    self.ser.write(header)
    cmd = (0x55).to_bytes(1, 'little')
    self.ser.write(cmd)
    data = (0x14).to_bytes(1, 'little')
    # data = (0x0A).to_bytes(1, 'little')
    self.ser.write(data)
    # data1 = (0x32).to_bytes(1, 'little')
    data1 = (0x01).to_bytes(1, 'little')
    self.ser.write(data1)
    data2 = (0x00).to_bytes(1, 'little')
    self.ser.write(data2)
    # パリティチェック
    check = 0x9A ^ 0x55
    # サンプリング周波数
    check = check ^ 0x14
    # 平均送信回数
    check = check ^ 0x01
    # 平均記録回数
    check = check ^ 0x00
    check = (check).to_bytes(1, 'little')

    self.ser.write(check)
    # list = [header, cmd, data, data1, data2, check]
    self.str = self.ser.read(1)
    print(self.str)
    print('CmdRes:' + repr(self.str))

  def startMesure(self):
    self.ser.read(1000)
    header = (0x9A).to_bytes(1, 'little')
    self.ser.write(header)
    cmd    = (0x13).to_bytes(1, 'little')
    self.ser.write(cmd)
    smode   = (0x00).to_bytes(1, 'little')
    self.ser.write(smode)
    syear  = (0x00).to_bytes(1, 'little')
    self.ser.write(syear)
    smonth = (0x01).to_bytes(1, 'little')
    self.ser.write(smonth)
    sday   = (0x01).to_bytes(1, 'little')
    self.ser.write(sday)
    shour  = (0x00).to_bytes(1, 'little')
    self.ser.write(shour)
    smin   = (0x00).to_bytes(1, 'little')
    self.ser.write(smin)
    ssec   = (0x00).to_bytes(1, 'little')
    self.ser.write(ssec)
    emode  = (0x00).to_bytes(1, 'little')
    self.ser.write(emode)
    eyear  = (0x00).to_bytes(1, 'little')
    self.ser.write(eyear)
    emonth = (0x01).to_bytes(1, 'little')
    self.ser.write(emonth)
    eday   = (0x01).to_bytes(1, 'little')
    self.ser.write(eday)
    ehour  = (0x00).to_bytes(1, 'little')
    self.ser.write(ehour)
    emin   = (0x00).to_bytes(1, 'little')
    self.ser.write(emin)
    esec   = (0x00).to_bytes(1, 'little')
    self.ser.write(esec)
    check = 0x9A ^ 0x13
    check = check ^ 0x00
    check = check ^ 0x00
    check = check ^ 0x01
    check = check ^ 0x01
    check = check ^ 0x00
    check = check ^ 0x00
    check = check ^ 0x00
    check = check ^ 0x00
    check = check ^ 0x00
    check = check ^ 0x01
    check = check ^ 0x01
    check = check ^ 0x00
    check = check ^ 0x00
    check = check ^ 0x00
    check = (check).to_bytes(1, 'little')
    self.ser.write(check)
    # コマンドレスポンス
    self.str = self.ser.read(1)
    # print('CmdRes:' + repr(str))
    # レスポンスを16進数に変換
    strFix = self.str.hex()
    print(strFix)
    # print(str)
    print("start")
    return strFix

  def setGraph():
    time1 = 1
    t = np.arange(-50, 0, 1)
    plt.ion()
    plt.figure()
    y = np.zeros(50)
    plt.ion()
    plt.figure()
    li, = plt.plot(t, y, 'r',label='yaw')
    #########roll & pitch#########
    r = np.zeros(50)
    li2, = plt.plot(t, r, 'k',label='roll')
    p = np.zeros(50)
    li3, = plt.plot(t, p, color = "royalblue",label='pitch')
  #################################
    plt.ylim(-100, 100)
    plt.yticks([-90,-75,-60,-45,-30,-15,0,15,30,45,60,75,90])
    plt.xlabel("time[s]")
    plt.ylabel("rpy(degrees)")
    plt.grid(color='gray')
    plt.legend(loc='best')
    plt.draw()

  def readData(self, strFix):
    # while strFix != 0x9A:
    while True:
      str = self.ser.read(1)
      # strHex = str.hex()
      # print('ReadRes:' + strHex)
      # print(str)
      if len(str) == 0:
        res = 0
      else:
        strHex = str.hex()
        res = int(strHex, 16)

        if res == 154:
          str = self.ser.read(1)
          strHex =str.hex()
          # print('書き込み' + strHex)
          # if strHex
          res = int(strHex, 16)
          if res == 138:
            if len(str) == 0:
              str = self.ser.read(1)
            else:
              responce = []
              quatLoop = int(str.hex(), 16)
              while quatLoop != 154:
                #header
                responce.append(str)
                #time
                str = self.ser.read(4)
                responce.append(str)
                #クォータニオン
                str = self.ser.read(2)
                responce.append(str)
                str = self.ser.read(2)
                responce.append(str)
                str = self.ser.read(2)
                responce.append(str)
                str = self.ser.read(2)
                responce.append(str)
                #加速度
                str = self.ser.read(3)
                responce.append(str)
                str = self.ser.read(3)
                responce.append(str)
                str = self.ser.read(3)
                responce.append(str)
                #角速度
                str = self.ser.read(3)
                responce.append(str)
                str = self.ser.read(3)
                responce.append(str)
                str = self.ser.read(3)
                responce.append(str)
                str = self.ser.read(1)
                responce.append(str)
                str = self.ser.read(1)
                # print(str)
                # print(len(str))
                if len(str) == 0:
                  quatLoop = 0
                else:
                  quatLoop = int(str.hex(), 16)

              if len(responce) == 13:
                self.quartW = int.from_bytes(responce[2],byteorder='little',signed = True)
                self.quartX = int.from_bytes(responce[3],byteorder='little',signed = True)
                self.quartY = int.from_bytes(responce[4],byteorder='little',signed = True)
                self.quartZ = int.from_bytes(responce[5],byteorder='little',signed = True)
                print(self.quartW, self.quartX, self.quartY, self.quartZ)

  def convertQuat(self):
    # while True:
      print("aaaaaaaa")
      a = np.sqrt(self.quartW**2 + self.quartX**2 + self.quartY**2 + self.quartZ**2)
      #aで割ってあげたwxyzをクォータニオン関数に渡す
      data = [self.quartY/a, self.quartX/a, self.quartZ/a, self.quartW/a]
      q = Quat(data)
      #roll, pitch, yawの順で配列に入れてあげる
      self.rpy = [q.dec,-q.roll,q.ra]
      #それぞれ±180度を超える値を取るときは±360度してあげて180度を超えないようにする
      for i in range(3):
          if self.rpy[i-1] > 180:
            self.rpy[i-1] -= 360
          elif self.rpy[i-1] <  -180:
            self.rpy[i-1] += 360

      #結果表示
      print(self.rpy)
      time.sleep(1)
      # roll = rpy[0]

  def updateGraph(self):

    t = np.append(t, time1)
    t = np.delete(t, 0)
    y = np.append(y, yaw)
    y = np.delete(y, 0)
    li.set_xdata(t)
    li.set_ydata(y)
#########roll & pitch add graph##########
    roll = rpy[0]
    pitch = rpy[1]
    yaw = rpy[2]
    r = np.append(r, roll)
    r = np.delete(r, 0)
    li2.set_xdata(t)
    li2.set_ydata(r)
    p = np.append(p, pitch)
    p = np.delete(p, 0)
    li3.set_xdata(t)
    li3.set_ydata(p)
########################################

    tMax = time1
    tMin = time1 - 50
    plt.xlim(tMin,tMax)
    plt.draw()
    plt.pause(0.0001)
    time1 = time1 + 1

if __name__ == '__main__':
  # ser = serial.Serial(port='/dev/tty.TSND151-AP03160848-Blue', timeout=0.5, baudrate=115200)
  tsnd = TSND151()
  tsnd.sendQuat()
  strFix = tsnd.startMesure()
  tsnd.readData(strFix)
  # thread_1 = threading.Thread(target=tsnd.readData(strFix))
  # thread_2 = threading.Thread(target=tsnd.convertQuat())
  # while True:
  #   executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
  #   executor.submit(tsnd.readData(strFix))
  #   executor.submit(tsnd.convertQuat())

  # ser.close();
