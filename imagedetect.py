import cv2
from imagefilter import imgfilter

img = cv2.imread("water.png")

processed = imgfilter(img)

cv2.imwrite("processed.png", processed)