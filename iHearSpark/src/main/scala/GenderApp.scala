import java.nio.file.{Files, Paths}

import org.apache.spark.SparkContext
import org.apache.spark.mllib.classification.{NaiveBayesModel, NaiveBayes}
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.mllib.regression.LabeledPoint

/**
 * Created by pradyumnad on 10/24/15.
 */
object GenderApp extends MLApp {

  ModelPath = iHApp.MODEL_URI+"/"+this.getClass.getName
  InputPath = iHApp.DATA_URI+"/mllib/gender.txt"

  def generateNaiveBayesModel(sc : SparkContext) {
    if (Files.exists(Paths.get(ModelPath))) {
      println(s"${ModelPath} exists..")
      return
    }

    val data = sc.textFile(InputPath)
    val parsedData = data.map { line =>
      val parts = line.split(',')
      LabeledPoint(parts(0).toDouble, Vectors.dense(parts(1).trim.split(' ').map(_.toDouble)))
    }
    // Split data into training (60%) and test (40%).
    val splits = parsedData.randomSplit(Array(0.8, 0.2), seed = 11L)
    val training = splits(0)
    val test = splits(1)

    val model = NaiveBayes.train(training, lambda = 0.1, modelType = "multinomial")

    val predictionAndLabel = test.map(p => (model.predict(p.features), p.label))
    val accuracy = 1.0 * predictionAndLabel.filter(x => x._1 == x._2).count() / test.count()

    println("accuracy "+accuracy)
    // Save and load model
    model.save(sc, ModelPath)
  }

  override def testApp(sc: SparkContext): Unit = {
    val sameModel = NaiveBayesModel.load(sc, GenderApp.ModelPath)
    val testdata = Vectors.dense(5.0, 60)
    val prediction = sameModel.predict(testdata)

    println(prediction+" is the prediction\n")
  }
}
