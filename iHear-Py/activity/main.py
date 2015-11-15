from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("ActivityClassification").setMaster("local")
    sc = SparkContext(conf)
    ssc = StreamingContext(sc)
    ds = ssc.socketTextStream("134.193.128.10", 1234)
