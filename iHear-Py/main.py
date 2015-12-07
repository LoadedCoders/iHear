import os

from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
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
NB_PATH = OUTPUT_URI + "/" + "NB"
DT_PATH = OUTPUT_URI + "/" + "DT"

classes = []


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
    print(paths[1])
    c = classes.index(paths[1])

    vec = audio.showFeatures(filepath)
    print(vec)
    return str(c) + "," + vec


def generateFeatures():
    if os.path.exists(FEATURES_PATH):
        print("Already available")
        return

    files = sc.textFile("sounds_full.txt")
    print("Total file : " + str(files.count()))
    features = files.map(fetchFeatures)
    print(features.count())
    features.saveAsTextFile(FEATURES_PATH)


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
    data = sc.textFile(FEATURES_PATH).map(parseLine)
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
    data = sc.textFile(FEATURES_PATH).map(parseLine)

    model = DecisionTree.trainClassifier(data, numClasses=classes.__len__(), categoricalFeaturesInfo={},
                                         impurity='gini', maxDepth=5, maxBins=32)
    print(model)
    # Save and load model
    model.save(sc, DT_PATH)
    print("Decision Tree model saved!")


def test(sc):
    model = DecisionTreeModel.load(sc, DT_PATH)
    # vec = audio.showFeatures("sounds/blender/20150227_193606-licuadora-14.wav")
    vec = audio.showFeatures("sounds/bike/20150227_193806-bici-14.wav")
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
    test(sc)
    sc.stop()
