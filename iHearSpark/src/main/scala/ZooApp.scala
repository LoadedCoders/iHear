import java.nio.file.{Paths, Files}

import org.apache.spark.SparkContext
import org.apache.spark.mllib.classification.{NaiveBayesModel, NaiveBayes}
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.mllib.regression.LabeledPoint

import scala.collection.immutable.HashMap

/**
 * Created by pradyumnad on 10/24/15.
 */
object ZooApp extends MLApp {

  ModelPath = iHApp.MODEL_URI + "/" + this.getClass.getName
  InputPath = iHApp.DATA_URI + "/zoo/zoo.data"
  var Classes = List(
    "moth",
    "aardvark",
    "newt",
    "octopus",
    "opossum",
    "antelope",
    "oryx",
    "ostrich",
    "bass",
    "parakeet",
    "bear",
    "penguin",
    "boar",
    "pheasant",
    "buffalo",
    "pike",
    "calf",
    "piranha",
    "carp",
    "pitviper",
    "catfish",
    "platypus",
    "polecat",
    "cavy",
    "pony",
    "porpoise",
    "cheetah",
    "chicken",
    "puma",
    "pussycat",
    "chub",
    "clam",
    "raccoon",
    "reindeer",
    "crab",
    "crayfish",
    "rhea",
    "scorpion",
    "crow",
    "seahorse",
    "deer",
    "dogfish",
    "seal",
    "dolphin",
    "sealion",
    "dove",
    "seasnake",
    "duck",
    "elephant",
    "seawasp",
    "skimmer",
    "flamingo",
    "flea",
    "skua",
    "frog",
    "slowworm",
    "frog",
    "slug",
    "sole",
    "sparrow",
    "squirrel",
    "starfish",
    "stingray",
    "swan",
    "termite",
    "toad",
    "tortoise",
    "tuatara",
    "tuna",
    "vampire",
    "vole",
    "vulture",
    "wallaby",
    "wasp",
    "wolf",
    "fruitbat",
    "giraffe",
    "worm",
    "girl",
    "gnat",
    "goat",
    "wren",
    "gorilla",
    "gull",
    "haddock",
    "hamster",
    "hare",
    "hawk",
    "herring",
    "honeybee",
    "housefly",
    "kiwi",
    "ladybird",
    "lark",
    "leopard",
    "lion",
    "lobster",
    "lynx",
    "mink",
    "mole",
    "mongoose"
  )

  def generateNaiveBayesModel(sc: SparkContext) {
    println("Classes : "+ Classes.size)
    if (Files.exists(Paths.get(ModelPath))) {
      println(s"${ModelPath} exists..")
      return
    }
    val data = sc.textFile(InputPath)

    val bClasses = sc.broadcast(Classes)

    val parsedData = data.map { line =>
      val parts = line.split(',')
      val features = parts.slice(1, parts.length).map(_.trim.toDouble)
      //      println(parts(0) +" - "+parts(0).hashCode.toDouble)
      val cats = bClasses.value
      val num = cats.indexOf(parts(0))
      LabeledPoint(num, Vectors.dense(features))
    }

    val model = NaiveBayes.train(parsedData, lambda = 0.1, modelType = "multinomial")

    // Save and load model
    model.save(sc, ModelPath)
    println(model.labels.mkString(" "))
  }

  override def testApp(sc: SparkContext): Unit = {
    val sameModel = NaiveBayesModel.load(sc, ModelPath)
    val testdata = Vectors.dense(
      0, //hair		Boolean
      0, //feathers		Boolean
      1, //eggs
      1, //milk
      0, //airborne
      0, //aquatic
      0, //predator
      0, //toothed
      0, //backbone
      0, //breathes
      0, //venomous
      0, //fins
      0, //LEGS (set of values: {0,2,4,5,6,8})
      0, //tail
      0, // domestic
      1, //catsize
      0 //type (integer values in range [1,7])
    )
    val prediction = sameModel.predict(testdata)

    println(Classes(prediction.toInt) + " is the prediction\n")
  }
}
