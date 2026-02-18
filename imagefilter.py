# takes ~0.01-0.03s

import cv2
import numpy as np

def imgfilter(img): 
    greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    lo = 54
    hi = 55

    layer = (greyscale.astype(np.float32) - lo) / (hi - lo) * 255
    layer = np.clip(layer, 0, 255).astype(np.uint8)

    kernel_small = np.ones((2, 2), np.uint8)
    noise = cv2.morphologyEx(layer, cv2.MORPH_OPEN, kernel_small, iterations=1)

    kernel_close = np.ones((2, 2), np.uint8)
    filled = cv2.morphologyEx(noise, cv2.MORPH_CLOSE, kernel_close, iterations=1) # fills small holes or something

    _, binary = cv2.threshold(filled, 230, 255, cv2.THRESH_BINARY)

    return binary