from socket import *
import time
import traceback

s = socket(AF_INET, SOCK_DGRAM)
# 设置套接字
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
# 选择一个接收地址
s.bind(('0.0.0.0', 5127))
while True:
    try:
        msg, addr = s.recvfrom(1024)
        print('接收消息==客户端地址:{},消息内容:{}'.format(addr, msg.decode('utf-8')))
    except:
        print("接收消息异常:{}".format(traceback.format_exc()))
s.close()

