__author__ = 'pradyumnad'

import cv2
import numpy as np
import itertools

img = cv2.imread("Flat1.jpg")

detector = cv2.FeatureDetector_create("SIFT")
descriptor = cv2.DescriptorExtractor_create("SIFT")

skp = detector.detect(img)
skp, sd = descriptor.compute(img, skp)

print(skp.count)

print(sd.size)
