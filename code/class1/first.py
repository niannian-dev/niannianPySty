name = 'shan三'
age = 25
height = 1.85
is_student = True
nothing = None

print("名字:",name)
print("年龄:",age)
print("身高:",height)
print("是否是学生:",is_student)
print("空值:",nothing)



print("Hello", "World", sep="-")  # Hello-World

name = input("请输入名字：")

print("你好，", name)

welcome = f"欢迎，{name}！"  # f"格式化字符串"

print(welcome)

print("----------------")

welcome = "你好{}, 欢迎来到Python世界！".format(name)

print(welcome)

print("----------------")
welcome = "你好%s，欢迎来到Python世界！" % name

print(welcome)



