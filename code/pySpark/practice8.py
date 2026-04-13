from init_spark import init_spark, stop_spark, get_spark_context, spark_parallelize


sc = init_spark("Practice8")

# 准备数据
list = [1,3,5,6,7,8,9,10,3,5,8,11,3,7,9,6,4,3,2,4,5,6,6,7,8,5,3,2,1]

rdd = spark_parallelize(sc, list)

rdd_new = rdd.distinct()  # 对每个键对应的值进行distinct操作，将结果返回

print(get_spark_context(rdd_new))

stop_spark(sc)


