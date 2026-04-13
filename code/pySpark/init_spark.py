from pyspark import SparkContext
from pyspark import SparkConf
import os

os.environ["PYSPARK_PYTHON"] = "C:\\Users\\shan\\AppData\\Local\\Programs\\Python\\Python311\\python3.11.exe"

def init_spark(app_name : str):
    conf = SparkConf().setMaster("local[*]").setAppName(app_name)
    sc = SparkContext(conf=conf)
    return sc

def stop_spark(sc : SparkContext):
    sc.stop()


def get_spark_context(rdd : SparkContext):
    return rdd.collect()

def spark_parallelize(sc : SparkContext, data : list | tuple | str | dict | set | range):
    rdd = sc.parallelize(data)
    return rdd
