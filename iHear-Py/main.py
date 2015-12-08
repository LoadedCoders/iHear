import os

from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.mllib.tree import DecisionTree, RandomForest, RandomForestModel, DecisionTreeModel
from pyspark.mllib.classification import NaiveBayes
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint
from pyspark import SparkContext, SparkConf

import audio

__author__ = 'pradyumnad'

os.environ['SPARK_HOME'] = "/usr/local/spark"
# sys.path.append("/usr/local/spark/python")
# sys.path.append("/usr/local/spark/python/lib/py4j-0.8.2.1-src.zip")

OUTPUT_URI = "Models"
FEATURES_PATH = OUTPUT_URI + "/" + "features"
FEATURES2_PATH = OUTPUT_URI + "/" + "features2"
FEATURES3_PATH = OUTPUT_URI + "/" + "features3"
NB_PATH = OUTPUT_URI + "/" + "NB"
DT_PATH = OUTPUT_URI + "/" + "DT"
RF_PATH = OUTPUT_URI + "/" + "RF"

classes = []

F_PATH = FEATURES_PATH


def generateTrainTextFile():
    file = open("sounds_full.txt", 'w')

    for dirname, dirnames, filenames in os.walk('sounds/'):
        for subdirname in dirnames:
            # print("-", os.path.join(dirname, subdirname))
            classes.append(subdirname)

        # print path to all filenames.
        for filename in filenames:
            if filename.endswith(".csv"):
                continue
            elif filename.startswith("."):
                continue
            elif filename.endswith(".npy"):
                continue
            if filename.endswith(".wav"):
                fullPath = os.path.join(dirname, filename)
                print(fullPath)
                file.write(fullPath + "\n")
    file.close()

    print classes


# Features saving
def fetchFeatures(filepath):
    print(filepath)
    paths = filepath.split("/")
    c = classes.index(paths[1])
    print(paths[1], c)

    vec = audio.showFeatures(filepath)
    return str(c) + "," + vec


def generateFeatures():
    if os.path.exists(F_PATH):
        print("Already available")
        return

    files = sc.textFile("sounds_full.txt")
    print("Total file : " + str(files.count()))
    features = files.map(fetchFeatures)
    print(features.count())
    features.saveAsTextFile(F_PATH)


# Naive Bayes Classification
def parseLine(line):
    parts = line.split(',')
    label = float(parts[0])
    features = Vectors.dense([float(x) for x in parts[1].split(' ')])
    return LabeledPoint(label, features)


def generateNBModel():
    if os.path.exists(NB_PATH):
        print("Already available")
        return

    global model
    data = sc.textFile(F_PATH).map(parseLine)
    # Split data aproximately into training (60%) and test (40%)
    # training, test = data.randomSplit([0.6, 0.4], seed=0)
    # Train a naive Bayes model.
    model = NaiveBayes.train(data, 0.1)
    # Make prediction and test accuracy.
    # predictionAndLabel = test.map(lambda p: (model.predict(p.features), p.label))
    # accuracy = 1.0 * predictionAndLabel.filter(lambda (x, v): x == v).count() / test.count()
    # print(accuracy)
    # Save and load model
    model.save(sc, NB_PATH)


def generateDecisionTree():
    if os.path.exists(DT_PATH):
        print("Already available")
        return

    global model
    data = sc.textFile(F_PATH).map(parseLine)

    (trainingData, testData) = data.randomSplit([0.7, 0.3])

    model = DecisionTree.trainClassifier(trainingData, numClasses=classes.__len__(), categoricalFeaturesInfo={},
                                         impurity='gini', maxDepth=5, maxBins=32)
    # Evaluate model on test instances and compute test error
    predictions = model.predict(testData.map(lambda x: x.features))
    labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
    testErr = labelsAndPredictions.filter(lambda (v, p): v != p).count() / float(testData.count())
    print('Test Error = ', str(testErr))

    print('Learned classification tree model:')
    print(model.toDebugString())

    modelStatistics(labelsAndPredictions)

    # Save and load model
    model.save(sc, DT_PATH)
    print("Decision Tree model saved!")


def generateRandomForest():
    if os.path.exists(RF_PATH):
        print("Already available")
        return

    data = sc.textFile(F_PATH).map(parseLine)

    (trainingData, testData) = data.randomSplit([0.8, 0.2])

    # Train a RandomForest model.
    #  Note: Use larger numTrees in practice.
    #  Setting featureSubsetStrategy="auto" lets the algorithm choose.
    model = RandomForest.trainClassifier(trainingData, numClasses=classes.__len__(), categoricalFeaturesInfo={},
                                         numTrees=5, featureSubsetStrategy="auto",
                                         impurity='gini', maxDepth=4, maxBins=32)

    # Evaluate model on test instances and compute test error
    predictions = model.predict(testData.map(lambda x: x.features))
    labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
    testErr = labelsAndPredictions.filter(lambda (v, p): v != p).count() / float(testData.count())
    print('Test Error', str(testErr))
    print('Learned classification forest model:')
    print(model.toDebugString())

    modelStatistics(labelsAndPredictions)

    # Save and load model
    model.save(sc, RF_PATH)
    print("Saved RF Model.")


def modelStatistics(labelsAndPredictions):
    metrics = MulticlassMetrics(labelsAndPredictions)
    print(metrics.confusionMatrix())

    # Overall statistics
    precision = metrics.precision()
    recall = metrics.recall()
    f1Score = metrics.fMeasure()
    print("Summary Stats")
    print("Precision = %s" % precision)
    print("Recall = %s" % recall)
    print("F1 Score = %s" % f1Score)

    # Weighted stats
    print("Weighted recall = %s" % metrics.weightedRecall)
    print("Weighted precision = %s" % metrics.weightedPrecision)
    print("Weighted F(1) Score = %s" % metrics.weightedFMeasure())
    print("Weighted F(0.5) Score = %s" % metrics.weightedFMeasure(beta=0.5))
    print("Weighted false positive rate = %s" % metrics.weightedFalsePositiveRate)


def test(sc):
    # model = RandomForestModel.load(sc, RF_PATH)
    model = DecisionTreeModel.load(sc, DT_PATH)
    files = ["sounds/flushing/20150227_193109-flushing-04.wav",
             "sounds/bike/20150227_193806-bici-14.wav",
             "sounds/blender/20150227_193606-licuadora-14.wav"
             ]

    for f in files:
        vec = audio.showFeatures(f)
        testfeatures = Vectors.dense([float(x) for x in vec.split(' ')])
        print(vec)
        pred = model.predict(testfeatures)
        print("Prediction is " + str(pred), classes[int(pred)])
        # print(classes)


if __name__ == '__main__':
    conf = SparkConf() \
        .set("spark.driver.port", "4040") \
        .setAppName("MyApp") \
        .setMaster("local")

    sc = SparkContext(conf=conf)

    generateTrainTextFile()

    generateFeatures()
    generateDecisionTree()
    generateRandomForest()

    test(sc)
    sc.stop()
