from pyspark.mllib.tree import DecisionTree, DecisionTreeModel

__author__ = 'pradyumnad'

import os

from pyspark.mllib.classification import NaiveBayes, NaiveBayesModel
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint

import audio

os.environ['SPARK_HOME'] = "/usr/local/spark"
# sys.path.append("/usr/local/spark/python")
# sys.path.append("/usr/local/spark/python/lib/py4j-0.8.2.1-src.zip")

from pyspark import SparkContext, SparkConf

classes = ["bike", "blender"]

conf = SparkConf() \
    .set("spark.driver.port", "4040") \
    .setAppName("MyApp") \
    .setMaster("local")

sc = SparkContext(conf=conf)


# Features saving

def fetchFeatures(filepath):
    print(filepath)
    paths = filepath.split("/")
    print(paths[1])
    if paths[1] == "bike":
        c = 0
    else:
        c = 1

    vec = audio.showFeatures(filepath)
    print(vec)
    return str(c) + "," + vec


def generateFeatures():
    if os.path.exists("features"):
        print("Already available")
        return

    files = sc.textFile("sounds.txt")
    print("Total file : " + str(files.count()))
    features = files.map(fetchFeatures)
    print(features.count())
    features.saveAsTextFile("features")


generateFeatures()


# Naive Bayes Classification
def parseLine(line):
    parts = line.split(',')
    label = float(parts[0])
    features = Vectors.dense([float(x) for x in parts[1].split(' ')])
    return LabeledPoint(label, features)


def generateNBModel():
    if os.path.exists("NBModelPath"):
        print("Already available")
        return

    global model
    data = sc.textFile('features').map(parseLine)
    # Split data aproximately into training (60%) and test (40%)
    # training, test = data.randomSplit([0.6, 0.4], seed=0)
    # Train a naive Bayes model.
    model = NaiveBayes.train(data, 0.1)
    # Make prediction and test accuracy.
    # predictionAndLabel = test.map(lambda p: (model.predict(p.features), p.label))
    # accuracy = 1.0 * predictionAndLabel.filter(lambda (x, v): x == v).count() / test.count()
    # print(accuracy)
    # Save and load model
    model.save(sc, "NBModelPath")


def generateDecisionTree():
    maxDepth = 5
    if os.path.exists("DTModelPath"):
        print("Already available")
        return

    global model
    data = sc.textFile('features').map(parseLine)

    model = DecisionTree.trainClassifier(data, numClasses=2, categoricalFeaturesInfo={},
                                         impurity='gini', maxDepth=5, maxBins=32)
    # Save and load model
    model.save(sc, "DTModelPath")


# generateNBModel()
generateDecisionTree()


def test():
    # model = NaiveBayesModel.load(sc, "NBModelPath")
    model = DecisionTreeModel.load(sc, "DTModelPath")
    # vec = audio.showFeatures("sounds/blender/20150227_193606-licuadora-14.wav")
    vec = audio.showFeatures("sounds/bike/20150227_193806-bici-14.wav")
    testfeatures = Vectors.dense([float(x) for x in vec.split(' ')])
    print(vec)
    pred = model.predict(testfeatures)
    print("Prediction is " + str(pred))


test()

sc.stop()
