package edu.umkc.helpers

import org.apache.spark.mllib.evaluation.MulticlassMetrics
import org.apache.spark.rdd.RDD

/**
 * Created by pradyumnad on 10/24/15.
 */

object ModelEvaluation {
  def evaluateModel(predictionAndLabels: RDD[(Double, Double)]) = {
    val metrics = new MulticlassMetrics(predictionAndLabels)
    val cfMatrix = metrics.confusionMatrix
    println(" |== Confusion matrix ==|")
    println(cfMatrix)
    println(metrics.fMeasure)
    for (label <- metrics.labels) {
      println(label+" - "+metrics.fMeasure(label))
    }
    //    println(metrics.labels.mkString("\t"))
  }
}
