from init_spark import init_spark, stop_spark, get_spark_context, spark_parallelize


sc = init_spark("Practice7")

# 准备数据
list = [1,2,3,4,5,6,7,8,9,10]

rdd = spark_parallelize(sc, list)

# 定义一个函数，用于筛选出偶数
def func(a) -> bool:
    return a % 2 == 0

# (V) -> bool
rdd_new = rdd.filter(func)  # 对每个键对应的值进行filter操作，将结果返回

print(get_spark_context(rdd_new))

stop_spark(sc)


