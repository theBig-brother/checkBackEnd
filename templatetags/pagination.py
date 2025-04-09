# 在你的应用目录下创建一个 templatetags 文件夹，然后在其中创建一个 `pagination.py` 文件

from django import template

register = template.Library()

@register.filter
def to(value):
    return range(1, value + 1)
