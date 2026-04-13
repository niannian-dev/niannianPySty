from init_spark import init_spark, stop_spark, get_spark_context, spark_parallelize


sc = init_spark("Practice9")

# 准备数据
list = [('java',5),('python',4),('php',3),('nodejs',7),('c++',6),('C#',3),('golang',2)]

rdd = spark_parallelize(sc, list)

# (V) -> U
def func(x : tuple) -> int:
    return x[1]

rdd_new = rdd.sortBy(func, ascending=False, numPartitions=1)  # 对每个键对应的值进行sortBy操作，将结果返回

print(get_spark_context(rdd_new))

stop_spark(sc)


