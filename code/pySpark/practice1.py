# 导入SparkContext和SparkConf
from pyspark import SparkContext, SparkConf

# 创建SparkConf对象
conf = SparkConf().setMaster("local[*]").setAppName("Practice1")

# 创建SparkContext对象
sc = SparkContext(conf=conf)

# 打印SparkContext对象的版本号
print(sc.version)

sc.stop()
