# 流程控制语句

for i in range(1,30):
    if i % 2 == 0:
        print(i,"个是偶数")

print("-"*30)

# 求100-999指之间的水仙花数
for i in range(100,1000):

    unit = i % 10
    decade  = i // 10 % 10
    hundred = i // 100

    if unit**3 + decade**3 + hundred**3 == i:
        print(i,"个是水仙花数")
