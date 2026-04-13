from init_spark import init_spark, stop_spark, get_spark_context, spark_parallelize


sc = init_spark("Practice13")

# 准备数据
list = [1,2,3,4,5,6,7,8,9,10]

tuple_list = [(1,2),(3,4),(5,6),(7,8),(9,10)]

dic_list = {'1':1,'2':3,'3':4,'4':5,'5':6,'6':7,'7':8,'9':10}

rdd = spark_parallelize(sc, list)

rdd_tuple = spark_parallelize(sc, tuple_list)

rdd_dic = spark_parallelize(sc, dic_list)

# 安装hadoop后，才能使用hdfs文件系统
rdd.saveAsTextFile('/output/list')

rdd_tuple.saveAsTextFile('/output/tuple')

rdd_dic.saveAsTextFile('/output/dic')

stop_spark(sc)