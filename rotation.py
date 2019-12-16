import cv2
import numpy as np
import math
import pytesseract
from scipy import ndimage

## (1) read
img = cv2.imread(r"C:\Users\Internship004\Desktop\rot3.jpg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img_edges = cv2.Canny(gray, 100, 100, apertureSize=3)
    # Using Houghlines to detect lines
lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=100, maxLineGap=5)

angles = []
for x1, y1, x2, y2 in lines[0]:
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
    angles.append(angle)

# Getting the median angle
median_angle = np.median(angles)

# Rotating the image with this median angle
img_rotated = ndimage.rotate(img, median_angle)

cv2.imwrite(r"C:\Users\Internship004\Desktop\orientation_corrected.jpg", img_rotated)

print(pytesseract.image_to_string(img_rotated))