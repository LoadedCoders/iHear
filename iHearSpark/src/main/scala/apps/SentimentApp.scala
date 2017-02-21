package apps

import java.nio.file.{Files, Paths}

import edu.umkc.helpers.ModelEvaluation
import edu.umkc.ihear.iHApp
import org.apache.spark.SparkContext
import org.apache.spark.mllib.classification.{NaiveBayes, NaiveBayesModel}
import org.apache.spark.mllib.feature.HashingTF
import org.apache.spark.mllib.regression.LabeledPoint

/**
 * Created by pradyumnad on 10/24/15.
 */
object SentimentApp extends MLApp {

  ModelPath = iHApp.MODEL_URI + "/" + this.getClass.getName
  InputPath = iHApp.DATA_URI + "/sentiment/*.txt"
  var Classes = List("negative", "positive")

  def generateNaiveBayesModel(sc: SparkContext) {
    if (Files.exists(Paths.get(ModelPath))) {
      println(s"${ModelPath} exists..")
      return
    }
    val data = sc.textFile(InputPath)

    val tf = new HashingTF(numFeatures = 100)

    val parsedData = data.map { line =>
      val parts = line.split("\t")
      val sentence = parts(1)
      val hashedWords = tf.transform(sentence.split(" "))

      LabeledPoint(parts(0).trim.toDouble, hashedWords)
    }

    // Split data into training (60%) and test (40%).
    val splits = parsedData.randomSplit(Array(0.6, 0.4), seed = 11L)
    val training = splits(0)
    val test = splits(1)

    val model = NaiveBayes.train(training, lambda = 0.1, modelType = "multinomial")

    val predictionAndLabel = test.map(p => (model.predict(p.features), p.label))
    val accuracy = 1.0 * predictionAndLabel.filter(x => x._1 == x._2).count() / test.count()
    println("Accuracy "+accuracy)
    ModelEvaluation.evaluateModel(predictionAndLabel)

    // Save and load model
//    model.save(sc, ModelPath)
    println(model.labels.mkString(" "))
  }

  override def testApp(sc: SparkContext): Unit = {
    val sameModel = NaiveBayesModel.load(sc, ModelPath)

    val tf = new HashingTF(numFeatures = 100)

    val hashedWords = tf.transform("Every movie sucks".split(" "))

    val prediction = sameModel.predict(hashedWords)

    println(Classes(prediction.toInt) + " is the prediction\n")
  }

  def classify(sc: SparkContext, sentense: String): String = {
    val sameModel = NaiveBayesModel.load(sc, ModelPath)

    val tf = new HashingTF(numFeatures = 100)

    val hashedWords = tf.transform(sentense.split(" "))

    val prediction = sameModel.predict(hashedWords)

    Classes(prediction.toInt)
  }
}
