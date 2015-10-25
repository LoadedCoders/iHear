import org.apache.spark.{SparkContext, SparkConf}

/**
 * Created by pradyumnad on 10/1/15.
 */
object iHearApp {

  def main(args: Array[String]) {
    println("Hello")

    val conf  = new SparkConf()
      .setAppName("iHear")
      .setMaster("local[*]")

    val sc = new SparkContext(conf)

    SentimentApp.generateNaiveBayesModel(sc)
    SentimentApp.testApp(sc)

    sc.stop()
  }
}
