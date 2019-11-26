# -*- coding: utf-8 -*-
"""
    ws.view
"""

# HTML模板渲染引擎
class Template:
    def __init__(self,HTML):
        self.html=HTML
    
    # 渲染
    def render(self,data):
        return self.html.format_map(data)