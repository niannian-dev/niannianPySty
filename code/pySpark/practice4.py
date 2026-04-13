from init_spark import init_spark, stop_spark, get_spark_context, spark_parallelize


sc = init_spark("Practice4")

# 准备数据
list = [1,2,3,4,5,6,7,8,9,10]

# 通过map方法将全部数据都乘10
rdd = spark_parallelize(sc, list)

# 定义一个函数，用于将输入的整数乘以10
def func(x : int) -> int:
    if (x % 2 == 0):
        return x*2
    else:
        return x*3
    
def func2(x : int) -> int:
    return x + 5

# (T) -> (U)    T: 输入数据的类型，U: 输出数据的类型
# 链式调用map方法，先调用func函数，再调用func2函数
rdd_new = rdd.map(func).map(func2)

print(get_spark_context(rdd_new))
print("-"*10)
print(get_spark_context(rdd))

stop_spark(sc)


