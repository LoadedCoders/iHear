import numpy as np

from pyAudioAnalysis import audioFeatureExtraction


def mean(data):
    a = np.array(data)
    return np.mean(a)


def standard_deviation(data):
    a = np.array(data)
    return np.std(a)


def median(data):
    a = np.array(data)
    return np.median(a)


def percentile(data, p):
    a = np.array(data)
    return np.percentile(a, p)


def spectral_energy(data):
    data_fft = fft(data)
    return np.square(data_fft)


def fft(data):
    a = np.array(data)
    b = np.fft.fft(a)
    return b


if __name__ == '__main__':
    b = range(-50, 100)
    print(median(b))
    print(mean(b))
    print(percentile(b, 25))
    print(percentile(b, 75))
    print(standard_deviation(b))
    bb = np.array(b)
    f = audioFeatureExtraction.stEnergy(bb)
    print(f)
    ff = audioFeatureExtraction.stZCR(bb)
    print(ff)
