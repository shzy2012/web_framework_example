#!/usr/bin/python
# -*- coding: utf-8 -*-

from ws.ws import WebServer
from ws.view import Template

# 创建ws
app = WebServer()
app.EnableCORS()
# 定义路由
@app.route("/")
def hello(request):
    return "i am working"

@app.route("/index.html")
def index(request):
    HTML = '''
    <div>
        <p>welcome, {name}</p>
    </div>
    '''
    
    dic = {'name':'ws'}
    return Template(HTML).render(dic)
# 开启监听
app.Listen(8000)


