import os

import matplotlib.pyplot as plt

from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction

INPUT_DIR = "sounds"


def showFeatures(name):
    print("processing - " + name)
    [Fs, x] = audioBasicIO.readAudioFile(name)
    print(x)
    F = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.50 * Fs, 0.25 * Fs)
    print(x.size, Fs, 0.50 * Fs, 0.25 * Fs)
    a = F[0, :]
    # numpy.savetxt("foo.csv", a, delimiter=",")

    plt.subplot(3, 1, 1)
    plt.plot(F[0, :])
    plt.xlabel('Frame no')
    plt.ylabel('ZCR')

    plt.subplot(3, 1, 2)
    plt.plot(F[1, :])
    plt.xlabel('Frame no')
    plt.ylabel('Energy')

    plt.subplot(3, 1, 3)
    plt.plot(F[4, :])
    plt.xlabel('Frame no')
    plt.ylabel('SC')

    plt.show()
    items = ' '.join(map(str, a))
    print(items)

    # return str(a.mean())+" "+str(a.var())+" "+str(a.min())+" "+str(a.max())
    return str(a.mean())


def getActivityFeatures(x, Fs):
    F = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.50 * Fs, 0.25 * Fs)
    # print(F)
    a = F[0, :]
    # numpy.savetxt("foo.csv", a, delimiter=",")

    plt.subplot(3, 1, 1)
    plt.plot(F[0, :])
    plt.xlabel('Frame no')
    plt.ylabel('ZCR')

    plt.subplot(3, 1, 2)
    plt.plot(F[1, :])
    plt.xlabel('Frame no')
    plt.ylabel('Energy')

    plt.subplot(3, 1, 3)
    plt.plot(F[4, :])
    plt.xlabel('Frame no')
    plt.ylabel('SC')

    plt.show()
    items = ' '.join(map(str, a))
    print(items)

    # return str(a.mean())+" "+str(a.var())+" "+str(a.min())+" "+str(a.max())
    return str(a.mean())


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
    # print(showFeatures("sounds/cough/20150227_194243-tosido-01.wav"))
    print showFeatures("sounds/cough/20150227_194243-tosido-02.wav")
    b = range(-50, 100)
    # getActivityFeatures(b, 2550)
    Fs = 2550
    F = audioFeatureExtraction.stFeatureExtraction(b, Fs, 0.50 * Fs, 0.25 * Fs)
