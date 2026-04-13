from init_spark import init_spark, stop_spark, get_spark_context, spark_parallelize


sc = init_spark("Practice10")

# 准备数据
list = [('java',5),('python',4),('php',3),('nodejs',7),('c++',6),('C#',3),('golang',2)]

rdd = spark_parallelize(sc, list)

list = rdd.collect()

print(list)

stop_spark(sc)


