from init_spark import init_spark, stop_spark, get_spark_context, spark_parallelize


sc = init_spark("Practice11")

# 准备数据
list = [1,2,3,4,5,6,7,8,9,10]

rdd = spark_parallelize(sc, list)

# (V,V) -> V
def func(x,y):
    return x+y

list = rdd.reduce(func)

print(list)

stop_spark(sc)