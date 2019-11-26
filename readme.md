### 如何编写web框架


WEB服务器也叫网页服务器（Web server),主要功能：

```text
Web应用框架（也叫“服务器端框架”）用于进行Web开发的一套软件架构，它是使用某种后端编程语言编写的，目标是使编写、维护和扩展web应用更加容易。提供的功能主要有
    1：提供http服务
    2：快速开发业务能力
web框架一般都提供工具和库来实现简单、常见的开发任务, 包括 路由处理, 数据库交互, 会话支持和用户验证, 格式化输出 (e.g. HTML, JSON, XML), 提高安全性应对网络攻击等.
```


框架功能列表：
```text
1.处理HTTP请求响应
2.将请求路由到相关的handle中
3.简化获取数据和响应数据
4.抽象和简化数据库接口
5.渲染数据
6.网络安全与数据加密
```

<img src="https://raw.githubusercontent.com/shzy2012/static/master/web_framework_http_process.png" width="800" height="500">

example 
```python
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
```