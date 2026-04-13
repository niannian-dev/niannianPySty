# 将输入转换为spark RDD对象

from pyspark import SparkContext
from pyspark import SparkConf

conf = SparkConf().setMaster("local[*]").setAppName("Practice2")
sc = SparkContext(conf=conf)

list = [1,2,3,4,5,6,7,8,9,10]
rdd1 = sc.parallelize(list)

tuple = (1,2,3,4,5,6,7,8,9,10)
rdd2 = sc.parallelize([tuple])

str = "hello world"
print(type(str))
rdd3 = sc.parallelize([str])

dict = {"a":1,"b":2,"c":3}
rdd4 = sc.parallelize([dict])

coll = {1,2,3,4,5,6,7,8,9,10} 
rdd5 = sc.parallelize(coll)


print(rdd1.collect())   # rdd.collect()方法可以将rdd中的所有元素收集到本地
print(rdd2.collect())
print(rdd3.collect())
print(rdd4.collect())
print(rdd5.collect())


sc.stop()



