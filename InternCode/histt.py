# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 11:21:34 2019

@author: Internship004
"""

import string
import json
import numpy as np
import pytesseract
import cv2 as cv

IMG = cv.imread(r'C:\Users\Internship004\Desktop/NewLicenses/histt.jpg', 0)
IMG2 = cv.imread(r'C:\Users\Internship004\Desktop/NewLicenses/histt.jpg',1)
W, H = IMG.shape[1], IMG.shape[0]

# Calculate aspect ratio
ASPECTRATIO = W/H

# Fix a width for passing to tesseract
FIXEDWIDTH = 700

# Resize the read image to the fixed resolution
IMG = cv.resize(IMG, (FIXEDWIDTH, int(FIXEDWIDTH//ASPECTRATIO)))
W, H = IMG2.shape[1], IMG2.shape[0]

# Calculate aspect ratio
ASPECTRATIO = W/H

# Fix a width for passing to tesseract
FIXEDWIDTH = 700

# Resize the read image to the fixed resolution
IMG2 = cv.resize(IMG2, (FIXEDWIDTH, int(FIXEDWIDTH//ASPECTRATIO)))
#IMG=cv.equalizeHist(IMG)
clahe=cv.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
IMG=clahe.apply(IMG)
#cv.imwrite(r'C:\Users\Internship004\Desktop\NewLicenses/histt.jpg',IMG)
cv.imshow('hist',IMG)
IMG3 = cv.cvtColor(IMG2,cv.COLOR_BGR2RGB)
cv.imshow('hist2',IMG2)
cv.imshow('hist3',IMG3)
cv.waitKey()
cv.destroyAllWindows()