from init_spark import init_spark, stop_spark, get_spark_context, spark_parallelize


sc = init_spark("Practice6")

# 准备数据
list = [('男',99),('女',88),('男',77),('女',66),('男',55),('女',44),('男',33),('女',22)]

rdd = spark_parallelize(sc, list)

# 定义一个函数，用于将输入的整数乘以10
def func(a , b) -> int:
    return a + b

# (V,V) -> V
rdd_new = rdd.reduceByKey(func)  # 对每个键对应的值进行reduce操作，将结果返回

print(get_spark_context(rdd_new))

stop_spark(sc)


