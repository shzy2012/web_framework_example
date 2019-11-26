#!/usr/bin/python
# -*- coding: utf-8 -*-

import ws.ws


# 创建ws
app = ws.WebServer()
app.EnableCORS()
# 定义路由
@app.route("/")
def hello(request):
    return "i am working"
# 开启监听
app.Listen(8001)


