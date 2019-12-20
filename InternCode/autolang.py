# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 16:14:19 2019

@author: Internship004
"""

import pytesseract
import cv2 as cv
import numpy as np
from langdetect import detect

IMG=cv.imread(r"C:\Users\Internship004\Desktop\Licenses\jap4.tiff", 1)
IMG = cv.cvtColor(IMG, cv.COLOR_BGR2RGB)


def clahe_try(img_rd):
    ''' Return image after applying clahe processing '''
    img_new = cv.cvtColor(img_rd, cv.COLOR_BGR2GRAY)
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img_new = clahe.apply(img_new)
    return img_new


def unsharp_mask(img_rd, kernel_size=(5, 5), sigma=1.0, amount=1.0, thresh=0):
    '''  Return a sharpened version of the image, using an unsharp mask '''
    blurred = cv.GaussianBlur(img_rd, kernel_size, sigma)
    sharpened = float(amount + 1) * img_rd - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if thresh > 0:
        low_contrast_mask = np.absolute(img_rd - blurred) < thresh
        np.copyto(sharpened, img_rd, where=low_contrast_mask)
    return sharpened


# Get the width and height of the image
H, W = list(IMG.shape)[0], list(IMG.shape)[1]

# Calculate aspect ratio
ASPECTRATIO = W/H

# Fix a width for passing to tesseract
FIXEDWIDTH = 700

# Resize the read image to the fixed resolution
IMG = cv.resize(IMG, (FIXEDWIDTH, int(FIXEDWIDTH//ASPECTRATIO)))

IMG = unsharp_mask(IMG)
# functon call
IMG = clahe_try(IMG)

text1 = pytesseract.image_to_data(IMG, output_type='data.frame')
text2 = pytesseract.image_to_data(IMG, output_type='data.frame',lang='jpn+eng')
text1 = text1[text1.conf != -1]
lines = text1.groupby('block_num')['text'].apply(list)
conf1 = text1.groupby(['block_num'])['conf'].mean()
TEXT1 = pytesseract.image_to_string(IMG)
TEXT2 = pytesseract.image_to_string(IMG,lang='jpn')
#print(detect(TEXT1))
#print(detect(TEXT2))
text2 = text2[text2.conf != -1]
lines = text2.groupby('block_num')['text'].apply(list)
conf2 = text2.groupby(['block_num'])['conf'].mean()

print("conf1="+str(conf1.mean()))
print("conf2="+str(conf2.mean()))
if(conf1.mean()>conf2.mean()):
    print("english")
else:
    print("jpn")

    
    