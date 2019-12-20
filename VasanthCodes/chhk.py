import string
import cv2
import pytesseract
import numpy as np

img = cv2.imread(r"C:\Users\Internship005\skew_corrected.png",0)
thresh = cv2.threshold(img, 0, 255,
                       cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
cv2.imshow("threshh",thresh)

result = pytesseract.image_to_string(thresh)
print(result)
cv2.waitKey()
cv2.destryAllWindows()