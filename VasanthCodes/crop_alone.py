import cv2
import numpy as np
import math
from scipy import ndimage

img = cv2.imread(r"C:\Users\Internship005\Desktop\NewLicenses\sidhu.jpg")
w,h=img.shape[1], img.shape[0]
aspectRatio = w/h

# fix a width for passing to tesseract
fixedWidth=700

#resize the read image to the fixed resolution
img = cv2.resize(img,(fixedWidth,int(fixedWidth//aspectRatio)))
#img=cv2.resize(img,(800,1000))
blurred = cv2.blur(img, (3,3))
canny = cv2.Canny(blurred, 50, 200)

## find the non-zero min-max coords of canny
pts = np.argwhere(canny>0)
y1,x1 = pts.min(axis=0)
y2,x2 = pts.max(axis=0)

## crop the region
cropped = img[y1:y2, x1:x2]
cv2.imwrite("cropped.png", cropped)

tagged = cv2.rectangle(img.copy(), (x1,y1), (x2,y2), (0,255,0), 3, cv2.LINE_AA)
#tagged= cv2.resize(tagged,(1000,800))
cv2.imshow("tagged", tagged)
cv2.waitKey()
