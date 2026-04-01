#eval函数
#去掉字符串中的引号，按照python语法解析

#eval()经常和input()配合使用

s = '3 + 3.14'
x = eval(s)
print(x,type(x))
#等同于
print(3 + 3.14,type(3 + 3.14))


