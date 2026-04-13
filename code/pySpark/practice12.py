from init_spark import init_spark, stop_spark, get_spark_context, spark_parallelize


sc = init_spark("Practice12")

# 准备数据
list = [1,2,3,4,5,6,7,8,9,10]

rdd = spark_parallelize(sc, list)

list = rdd.take(3)

print(list)

stop_spark(sc)