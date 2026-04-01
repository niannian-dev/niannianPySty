#整数类型

#进制表示
#十进制
print(18)
#二进制
print(0b10010)
#八进制
print(0o22)
#十六进制
print(0x12)

num1 = 24
num2 = 0b110000
num3 = 0o22
num4 = 0x124
print(num1)
print(num2)
print(num3)
print(num4)

#浮点数类型
x = 3.1
y = 1.2

#浮点数的运算,存在不确定位数，需要使用round函数进行四舍五入
print(x * y)
print(round(x * y,2))

#浮点数表示虚数
x = 123 + 456j
print(x)
print("虚数的模为：",abs(x))
print("虚数的实部为：",x.real)
print("虚数的虚部为：",x.imag)


#转义字符
print("hello world")
print("hello\nworld")
print("hello\tworld")
print("hello\\world")
print("hello\'world")
print("hello\"world")

#转义字符失效
print("-----------------")
print(R"hello\nworld")
print("hello\nworld")
print(r"hello\tworld")


#字符索引
strs = "hello world"
print(strs[0])
print(strs[10])

#字符串切片,左闭右开
print(strs[0:5])
print(strs[6:])
print(strs[:5])

#字符串的负索引,从后往前数
print(strs[-1])
print(strs[-6:])
print(strs[:-5])

#字符串的拼接操作
x = "hello"
y = "world"
print(x + y)
print(x * 3)
print(x * 3 + y)
print('h' in x)

#布尔类型
print(True)
print(False)

#布尔类型的转换,非零数字为True,零为False,空字符串为False,非空字符串为True
# ,空为False,非空为True,空列表为False,非空列表为True,空元组为False,非空元组为True,空字典为False,非空字典为True
print(bool(10))
print(bool(0))
print(bool(""))
print(bool("hello"))
print(bool([]))

#自定义对象的 __bool__方法和 __len__方法返回False或者0时,对象为False


self = None

def __bool__(self):
    return False
def __len__(self):
    return 0

if __bool__(self):
    print("对象为True")
else:
    print("对象为False")

if __len__(self):
    print("对象为True")
else:
    print("对象为False")


#数据类型转换显示转换使用函数
print("=====================")
print(int("123"))
print(float("123.456"))
print(str(123))
print(chr(65))
print(ord('c'))
print(hex(10))
print(oct(10))
print(bin(10))
