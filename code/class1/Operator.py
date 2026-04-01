
# 逻辑运算符

age = 12
is_student = True

if (age < 18 and is_student):
    print("你是一个学生")
else:
    print("你不是一个学生")

if (age < 18 or is_student):
    print("你是个孩子")
else:
    print("你可能不是一个孩子")

if  (not is_student):
    print("你不是一个学生")
else:
    print("你是一个学生")



list = [1,2,3,4,5]
print(list)

if(5 in list):
    print("5在列表中")
else:
    print("5不在列表中")

if(10 not in list):
    print("10不在列表中")
else:
    print("10在列表中")