# stack overflow 
# https://stackoverflow.com/questions/24536552/how-to-combine-pywavelet-and-opencv-for-image-processing
import numpy as np
import pywt
import cv2

def transform_image(img, mode='haar', level=1):
    imageArray = img
    # converting the image to grayscale
    imageArray = cv2.cvtColor(imageArray, cv2.COLOR_RGB2GRAY)
    # conver the image array to float
    imageArray = np.float32(imageArray)
    imageArray /= 255;
    # compute coefficients
    coeffs = pywt.wavedec2(imageArray, mode, level=level)

    #process coeffs
    coeffsH = list(coeffs)
    coeffsH[0] *= 0;

    #reconstruction
    imageArrayH = pywt.waverec2(coeffsH, mode);
    imageArrayH *= 255
    imageArrayH = np.uint8(imageArrayH)

    return imageArrayH