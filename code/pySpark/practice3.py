# 将输入转换为spark RDD对象

from pathlib import Path
from pyspark import SparkContext, SparkConf

script_dir = Path(__file__).resolve().parent
file_path = script_dir / "file" / "version.txt"

conf = SparkConf().setMaster("local[*]").setAppName("Practice3")
sc = SparkContext(conf=conf)

rdd = sc.textFile(file_path.as_posix())

fileContent = rdd.collect()
for line in fileContent:
    print(line)


sc.stop()