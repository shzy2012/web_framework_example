#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import sys

# 1.创建 TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2.绑定socket监听地址(ip:port)
server_address = ('0.0.0.0', 5000)
sock.bind(server_address)
print('starting up on {} port {}'.format(*server_address))

# 3.开启监听
sock.listen(100)

# http 响应模板
response_template = '''
HTTP/1.0 200 OK
Date: Mon, 27 Jul 2009 12:28:53 GMT
Server: http-123/1.2.0 (myserver)
Last-Modified: Wed, 22 Jul 2019 19:00:00 GMT
Content-Length: {}
Content-Type: text/html
Connection: Closed

{}'''

# http body模板
body = '''<html>
    <head>
        <title>http server example</title>
    </head>
    <body>
        <h1>The HTTP Server is working!</h1>
    </body>
</html>'''


# 4.循环等待客户端连接
while True:
    # a.等待一个客户端连接
    connection, client_address = sock.accept()
    
    # 打印收到的客户端请求信息
    print('-------------------------------------------|')
    print('---------receive data from client----------|')
    print('-------------------------------------------|')

    # b.读取客户端请求信息
    
    print(client_address)
    data = connection.recv(1024)
    for param in str(data,'utf-8').split("\r\n"):
        print(param)
     
    # c.执行业务处理函数 httpHanler
    # 1.跨域逻辑

    # 打印服务端响应的信息
    print('-------------------------------------------|')
    print('------sending data back to the client------|')
    print('-------------------------------------------|')
    response = response_template.format(len(body),body)

    # d.服务端响应数据给请求的客户端
    connection.sendall(bytes(response, 'utf-8'))

    # e.关闭连接
    connection.close()
    print(response,"\r\n")
