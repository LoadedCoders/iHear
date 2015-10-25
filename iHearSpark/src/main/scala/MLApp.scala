import org.apache.spark.SparkContext

/**
 * Created by pradyumnad on 10/24/15.
 */
trait MLApp {
  var ModelPath = ""
  var InputPath = ""
  def testApp(sc: SparkContext)
}
