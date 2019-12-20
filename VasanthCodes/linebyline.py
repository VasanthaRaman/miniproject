# 2018.01.16 01:11:49 CST
# 2018.01.16 01:55:01 CST
import cv2
import numpy as np
import math
from scipy import ndimage

## (1) read
img = cv2.imread(r"C:\Users\Internship005\Desktop\rot2.jpg")

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
img_rotated2=ndimage.rotate(img, 360-median_angle)

cv2.imwrite('orientation_corrected.jpg', img_rotated)
cv2.imwrite('orientation_corrected2.jpg', img_rotated2)

## (2) threshold
th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)



## (3) minAreaRect on the nozeros
pts = cv2.findNonZero(threshed)
ret = cv2.minAreaRect(pts)

(cx,cy), (w,h), ang = ret
#if w>h:
#    w,h = h,w
#    ang += 90

## (4) Find rotated matrix, do rotation
M = cv2.getRotationMatrix2D((cx,cy), ang, 1.0)
rotated = cv2.warpAffine(threshed, M, (img.shape[1], img.shape[0]))

## (5) find and draw the upper and lower boundary of each lines
hist = cv2.reduce(rotated,1, cv2.REDUCE_AVG).reshape(-1)

th = 2
H,W = img.shape[:2]
uppers = [y for y in range(H-1) if hist[y]<=th and hist[y+1]>th]
lowers = [y for y in range(H-1) if hist[y]>th and hist[y+1]<=th]

rotated = cv2.cvtColor(rotated, cv2.COLOR_GRAY2BGR)
for y in uppers:
    cv2.line(rotated, (0,y), (W, y), (255,0,0), 1)

for y in lowers:
    cv2.line(rotated, (0,y), (W, y), (0,255,0), 1)

cv2.imwrite("result.png", img_edges)
#img_edges= cv2.resize(img_rotated,(1000,800))
#comment here


#img = cv2.imread("test.png")
#img = cv2.imread("img02.png")

blurred = cv2.blur(img_rotated, (3,3))
canny = cv2.Canny(blurred, 50, 200)

## find the non-zero min-max coords of canny
pts = np.argwhere(canny>0)
y1,x1 = pts.min(axis=0)
y2,x2 = pts.max(axis=0)
'''
## crop the region
cropped = img[y1:y2, x1:x2]
cv2.imwrite("cropped.png", cropped)

tagged = cv2.rectangle(img_edges.copy(), (x1,y1), (x2,y2), (0,255,0), 3, cv2.LINE_AA)
tagged= cv2.resize(tagged,(1000,800))
cv2.imshow("tagged", tagged)
cv2.waitKey()
'''

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
blur = cv2.GaussianBlur(hsv[:,:,1],(7,7),0)
edged = cv2.Canny(blur, 10, 250)
cv2.imwrite("Edged.jpg", edged)

pts = np.argwhere(edged>0)
y1,x1 = pts.min(axis=0)
y2,x2 = pts.max(axis=0)

## crop the region
cropped = img[y1:y2, x1:x2]
cv2.imwrite("cropped.png", cropped)

tagged = cv2.rectangle(img.copy(), (x1,y1), (x2,y2), (0,255,0), 3, cv2.LINE_AA)
cv2.imshow("tagged", tagged)
cv2.waitKey(0)
