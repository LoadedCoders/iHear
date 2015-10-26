package edu.umkc.ihear

import java.net.InetAddress

import apps.SentimentApp
import edu.umkc.helpers.SocketClient
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.{SparkConf, SparkContext}

/**
 * Created by pradyumnad on 10/1/15.
 */
object iHearApp {

  def main(args: Array[String]) {
    println("Hello")

    val conf = new SparkConf()
      .setAppName("iHear")
      .setMaster("local[*]")

    val ssc = new StreamingContext(conf, Seconds(1))
    val sc = ssc.sparkContext

    SentimentApp.generateNaiveBayesModel(sc)
    SentimentApp.testApp(sc)

    val ip = InetAddress.getByName(iHApp.iOS_IP).getHostName

    val lines = ssc.socketTextStream(ip, 1234)

    val data = lines.map(line => {
      line
    })

    data.foreachRDD(sentences => {
      val sc = sentences.context
      if (sentences.count() > 0) {
        val sentence = sentences.collect().mkString(".")
        val result = SentimentApp.classify(sc, sentence)
        SocketClient.sendCommandToRobot(sentence+" is "+result.toString)
      }
    })

    data.print()

    ssc.start()
    ssc.awaitTermination()
  }
}
