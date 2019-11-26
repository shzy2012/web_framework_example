# -*- coding: utf-8 -*-
"""
    microframework.app
"""

__name__ = "microframework.app"
import socket
import sys
import collections
import os
import json

# 创建服务器
class WebServer:
    # 开启服务端监听
    def __init__(self,):
        self.routes={}
        self.enableCORS=False

    def Listen(self,port):
         # 1.创建 TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 2.绑定socket监听地址(ip:port)
        server_address = ('0.0.0.0', port)
        sock.bind(server_address)
        print('starting up on {} port {}'.format(*server_address))
        # 3.开启监听
        sock.listen(100)
         # 4.循环等待客户端连接
        while True:
            connection,client_address = sock.accept()
            HttpHandle(connection,client_address,self.routes,self.enableCORS)  
    # 路由处理  
    def route(self,path=None):
        def wrapper(func):
            self.routes[path]=func
            return func
        return wrapper
    
    # 跨域
    def EnableCORS(self):
        self.enableCORS=True
    
    # database 访问层
    def DB(self):
        # 打开数据库
        def open(self):
            pass
        # 连接数据库
        def connect(self):
            pass
        # 执行SQL
        def execute(self,sql):
            pass
            # 获取数据
            def fetch():
                pass

# 处理客户端
class HttpHandle:
    def __init__(self,connection,client_address,routes,enableCORS):
        # 回话
        self.conn = connection
        self.client_address = client_address
        # 路由
        self.routes = routes
        # 请求、响应
        self.request = {}
        self.response = {}
        # 存储request data
        self.request_data = b''
        # 存储response data
        self.write_queue = collections.deque()
        # 跨域
        self.enableCORS=enableCORS
        # 处理请求
        self.conn_hanler(connection)
 

     # 处理接受事件
    def conn_hanler(self,connection):
        # 打印收到的客户端请求
        self.read_hanler(connection)


    # 读取传入的请求数据
    def read_hanler(self,connection):
        # 读取客户端请求信息
        while True:
            chunk = connection.recv(1024)
            self.request_data += chunk
            if b'\r\n\r\n' in self.request_data:
                self.handle_request()
                break


    # 处理传入请求
    def handle_request(self):
        header_data = self.request_data[:self.request_data.find(b'\r\n\r\n')]
        header_text = header_data.decode('utf-8')
        header_lines = header_text.splitlines()
        request = header_lines.pop(0).split()
        op = request[0]
        url = request[1]
        dic = {'op':op,'url':url}

        for x in header_lines:
            keys = x.split()
            key = keys[0].replace(':','') #删除 "Host:"中的":"
            if key=="Host":
                values = keys[1].split(':')
                dic[key]=values[0]
                dic["Port"]=values[1]
            else:
                dic[key]=keys[1]

        self.request = dic
        print('---------receive data from client{}----------'.format(self.client_address))
        print(header_text)

        # 处理CORS
        if(self.enableCORS):
            if not (('Host' in dic) & (dic['Host'] == 'localhost')):
                self.send_error(403,'No Access-Control-Allow-Origin header is present on the requested resource')
                self.handle_write()
                return
        
        self.process_request(op,url)

    # 处理请求
    def process_request(self,op,url):

        # 解析不同的请求方法
        if op =="GET":
            if url in self.routes.keys():
                f = self.routes[url]
                data = str(f(self.request))
                self.push_text('HTTP/1.0 200 OK\r\n')
                self.push_text('Server: shzy-ws\r\n')
                self.push_text('Content-Length: %d\r\n' % len(data))
                self.push_text('Content-Type: application/json\r\n')
                self.push_text('Set-Cookie: name=ws_cookie\r\n')
                self.push_text('Set-Cookie: id=a3fWa; HttpOnly\r\n')
                self.push_text('Connection: Closed\r\n')
                self.push_text('\r\n')
                self.push_text(data)
            else:
                self.send_error(404,"url {} not found\r\n".format(url))
            
        elif op=="POST":
            pass
        elif op=="PUT":
            pass
        elif op=="HEAD":
            pass
        elif op=="DELETE":
            pass
        elif op=="OPTIONS":
            pass
        elif op=="TRACE":
            pass
        else:
            self.send_error(501,"{} method not implemented\r\n".format(self.op))
        
        self.handle_write()


    # 错误处理
    def send_error(self,code,message):
        self.push_text('HTTP/1. %s %sOK\r\n' %(code,'Not Found'))
        self.push_text('Content-Type: text/plain\r\n')
        self.push_text('Content-Length: %d\r\n' % len(message))
        self.push_text('Connection: Closed\r\n')
        self.push_text('\r\n')
        self.push_text(message)

    # 将文本数据添加到输出队列
    def push_text(self,text):
        self.push(text.encode('utf-8'))

    # 将二进制数据添加到输出队列
    def push(self,data):
        self.write_queue.append(data)
    
    # 写入响应数据
    def handle_write(self):
        # 服务端响应数据给请求的客户端
        data = b''
        while len(self.write_queue)>0:
            data += self.write_queue.popleft()
            
        print('---------send data to client------------')
        print(data)
        self.conn.sendall(data)
        #data=bytes("hello", 'utf-8')
        # 关闭连接
        self.conn.close()

# app
if __name__ == '__main__':
    pass
else:
    # 创建ws
    app = WebServer()
    app.EnableCORS()
    # 定义路由
    @app.route("/")
    def hello(request):
        return "i am working"
    # 开启监听
    app.Listen(8001)