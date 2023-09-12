import cv2
import numpy as np
from PIL import Image


def cv2_to_PIL(img: np.ndarray, alpha=False):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB if not alpha else cv2.COLOR_BGRA2RGBA)
    img_pil = Image.fromarray(img)
    return img_pil


def PIL_to_cv2(img: Image, alpha=False):
    img = np.asarray(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR if not alpha else cv2.COLOR_RGBA2BGRA)
    return img
