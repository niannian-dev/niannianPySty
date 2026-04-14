# 正则表达式
import re

s = 'hello python'

try:
 # # match 方法从字符串的开头开始匹配,如果匹配失败,则返回 None
    result = re.match(r'hello', s)
    print(result)
    print(result.group())
    print(result.span())
except:
    print('匹配失败')

# try:
#  # # match 方法从字符串的开头开始匹配,如果匹配失败,则返回 None
#     result = re.match(r'ello', s)
#     print(result)
#     print(result.group())
#     print(result.span())
# except:
#     print('匹配失败')

print('-'*30)
str = 'Python 到 AI 应用开发学习路线 , Python 是一种高级编程语言, 学会 Python 可以让你快速上手 AI 应用开发'
result = re.search(r'Python', str)
print(result)
print(result.group())
print(result.span())

print('-'*30)
str = 'Python 到 AI 应用开发学习路线 , Python 是一种高级编程语言, 学会 Python 可以让你快速上手 AI 应用开发'
result = re.findall(r'Python', str)
print(result)