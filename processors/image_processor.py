import logging

import cv2
import numpy as np
from skimage.morphology import skeletonize

from utils.config import Config

logger = logging.getLogger(__name__)


def process_image():
    image = cv2.imread(Config().input_path)

    binary = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = cv2.erode(binary, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1)), iterations=1)
    binary = cv2.dilate(binary, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1)), iterations=1)
    binary = cv2.medianBlur(binary, 3)

    _, binary = cv2.threshold(binary, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    binary = cv2.bilateralFilter(binary, 3, 9, 9)

    skeleton = skeletonize(binary // 255 , method="lee")
    skel_image_opencv = np.asarray(skeleton, dtype=np.uint8) * 255
    cv2.imwrite(Config().skeleton_path, skel_image_opencv)

    return skeleton
