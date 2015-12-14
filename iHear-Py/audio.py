import os

from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import matplotlib.pyplot as plt

INPUT_DIR = "sounds"


def showFeatures(name):
    print("processing - " + name)
    [Fs, x] = audioBasicIO.readAudioFile(name)
    # print(x)
    F = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.50 * Fs, 0.25 * Fs)
    # print(x.size, Fs, 0.50 * Fs, 0.25 * Fs)
    # a = F[0, :]
    # numpy.savetxt("foo.csv", a, delimiter=",")

    # plt.subplot(3, 1, 1)
    # plt.plot(F[0, :])
    # plt.xlabel('Frame no')
    # plt.ylabel('ZCR')
    #
    # plt.subplot(3, 1, 2)
    # plt.plot(F[1, :])
    # plt.xlabel('Frame no')
    # plt.ylabel('Energy')
    #
    # plt.subplot(3, 1, 3)
    # plt.plot(F[3, :])
    # plt.xlabel('Frame no')
    # plt.ylabel('SC')
    #
    # plt.show()
    # items = ' '.join(map(str, a))
    # print(items)
    # print("--", F[0, :])
    vec = [
        F[0, :].mean(), F[1, :].mean(), F[4, :].mean(), F[5, :].mean(), F[6, :].mean(), F[7, :].mean(),
        F[0, :].std(), F[1, :].std(), F[4, :].std(), F[5, :].std(), F[6, :].std(), F[7, :].std()
    ]

    vecstr = ' '.join(map(str, vec))

    melfeat = melfeature(F)
    # chromafeat = chromafeature(F)
    return vecstr + " " + melfeat


def melfeature(F):
    mel = [
        F[8, :].mean(), F[9, :].mean(), F[10, :].mean(), F[11, :].mean()
    ]

    vecstr = ' '.join(map(str, mel))
    return vecstr


def chromafeature(F):
    chroma = [
        F[31, :].mean(), F[32, :].mean(),
        F[31, :].std(), F[32, :].std()
    ]

    vecstr = ' '.join(map(str, chroma))
    return vecstr


def generateSoundsTextFile():
    file = open("sounds.txt", 'w')

    for dirname, dirnames, filenames in os.walk('sounds'):
        for subdirname in dirnames:
            print(os.path.join(dirname, subdirname))

        # print path to all filenames.
        for filename in filenames:
            if filename.startswith("."):
                continue
            fullPath = os.path.join(dirname, filename)
            print(fullPath)
            file.write(fullPath + "\n")
    file.close()


if __name__ == '__main__':
    print showFeatures("sounds/cough/20150227_194243-tosido-01.wav")
    print showFeatures("sounds/cough/20150227_194243-tosido-02.wav")
