package edu.umkc.ihear

import java.net.InetAddress

import apps.SentimentApp
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.{SparkConf, SparkContext}

/**
 * Created by pradyumnad on 10/1/15.
 */
object iHearApp {

  def main(args: Array[String]) {
    println("Hello")

    val conf  = new SparkConf()
      .setAppName("iHear")
      .setMaster("local[*]")

    val ssc = new StreamingContext(conf, Seconds(2))
    val sc = ssc.sparkContext

    SentimentApp.generateNaiveBayesModel(sc)
    SentimentApp.testApp(sc)

    val ip = InetAddress.getByName("10.182.0.192").getHostName

    val lines = ssc.socketTextStream(ip, 5555)

    val data = lines.map(line => {
      line
    })

    data.print()

    ssc.start()
    ssc.awaitTermination()
  }
}
