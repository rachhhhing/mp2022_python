import cv2
import sys
import numpy as np
from socket import *
from threading import Thread
from datetime import datetime

class Server():
    def __init__(self, socket, addr, capture):
        self._socket = socket
        self._addr = addr
        self._cap = capture
    
    def __get_cam(self):
        while True:
            ret, frame = self._cap.read()
            yield frame

    def post_cam(self):
        for frame in self.__get_cam():
            img_encode = cv2.imencode('.jpg', frame)[1]
            data_encode = np.array(img_encode)
            data = data_encode.tobytes()
            self._socket.sendto(data, self._addr)
            reply, addr = self._socket.recvfrom(1024)
            # 收到客户端消息若为退出, 则结束线程
            if reply.decode('utf-8') == 'end':
                break
        with open('week13/ServerLog.txt', 'a', encoding='utf-8') as f:
            f.write(f'{datetime.now()} 客户端{self._addr} 退出\n')

def accpet_client():
    # tcp通讯用于获取接入的ip
    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.bind(('0.0.0.0', 9999))
    tcp_socket.listen(5)
    # udp通讯用于传输视频
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    capture = cv2.VideoCapture(0)
    capture.set(3, 160) # 故意修改小的，不然mac上容易超过udp发送数据的长度限制
    capture.set(4, 90)  # windows上好像不用这么小
    while True:
        print('新的客户端正在接入中...')
        conn, addr = tcp_socket.accept()
        client = (addr[0], int(conn.recv(1024).decode('utf-8')))
        # 记录Log日志
        with open('week13/ServerLog.txt', 'a', encoding='utf-8') as f:
            f.write(f'{datetime.now()} 客户端{client} 接入\n')
        # 开启子线程, 传输监控视频
        s = Server(udp_socket, client, capture)
        t = Thread(target=Server.post_cam, args=(s,))
        t.start()

if __name__ == "__main__":
    a = Thread(target=accpet_client)
    a.start()
    a.join()