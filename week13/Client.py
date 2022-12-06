import cv2
import sys
import time
import numpy as np
from socket import *
from datetime import datetime

rsize = 400000
fourcc = cv2.VideoWriter_fourcc(*'XVID')

class Receiver:
    def __init__(self, socket, addr, savetime=15, savepath='D:/code/mp2022/week13/camera'):
        self._socket = socket
        self._addr = addr
        self._time = savetime
        self._path = savepath
    
    def __save_cam(self, frame):
        # 每一段时间储存一次视频
        if time.time() - self._start > self._time:
            self._start = time.time()
            path = self._path + (datetime.now().strftime('%H-%M-%S')) + '.avi'
            self._out = cv2.VideoWriter(path, fourcc, 10.0, (160,120))
        self._out.write(frame)

    def receive_cam(self):
        self._socket.bind(self._addr)
        self._start = time.time()
        path = self._path + (datetime.now().strftime('%H-%M-%S')) + '.avi'
        self._out = cv2.VideoWriter(path, fourcc, 10.0, (160,120))
        # fourcc 指定编码器; fps 要保存的视频的帧率
        while True:
            data, addr = self._socket.recvfrom(rsize)
            nparr = np.frombuffer(data, np.uint8)
            img_decode = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            cv2.imshow('receive', img_decode)
            self.__save_cam(img_decode)		# 储存每一帧
            c = cv2.waitKey(50)
            udp_socket.sendto('continue'.encode('utf-8'), addr)
            if c == 27:         			# 按了esc后可以退出
                cv2.destroyAllWindows()
                udp_socket.sendto('end'.encode('utf-8'), addr)
                break

if __name__ == "__main__":
    # 和服务器连接, 将自己ip和port发过去
    # sys.argv[1], sys.argv[2] 是服务器的ip和port
    # sys.argv[3] 是客户端用于接收视频的端口号
    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.connect((sys.argv[1], int(sys.argv[2])))
    tcp_socket.send((sys.argv[3]).encode('utf-8'))
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    r = Receiver(udp_socket, ('0.0.0.0', int(sys.argv[3])))
    r.receive_cam()