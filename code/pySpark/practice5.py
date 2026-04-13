from init_spark import init_spark, stop_spark, get_spark_context, spark_parallelize


sc = init_spark("Practice4")

# 准备数据
list = ["python java c++","mysql mangoDB redis oracle","spark hadoop spring mybatis"]

rdd = spark_parallelize(sc, list)

# 定义一个函数，用于将输入的字符串拆分成单词列表
def func(str : str) -> str:
    return str.split(" ")

# (T) -> (U)    T: 输入数据的类型，U: 输出数据的类型
# 结果拆分出来的字符串是列表中嵌套列表 [['python', 'java', 'c++'], ['mysql', 'mangoDB', 'redis', 'oracle'], ['spark', 'hadoop', 'spring', 'mybatis']]
# rdd_new = rdd.map(func) 
rdd_new = rdd.flatMap(func)  # 将嵌套列表展开为平铺列表

print(get_spark_context(rdd_new))

stop_spark(sc)


