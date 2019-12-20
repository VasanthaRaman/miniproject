from fpt import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils
import pytesseract
import PIL
 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image to be scanned")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height = 500)
 
# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)
 
# show the original image and the edge detected image
print("STEP 1: Edge Detection")
cv2.imshow("Image", image)
cv2.imshow("Edged", edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
screenCnt=0
# loop over the contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
 
	# our approximated contour should have four points
	if len(approx) == 4:
		screenCnt = approx
		break
 
# show the contour 
print("STEP 2: Find contours of paper")
cv2.drawContours(gray, [screenCnt], -1, (0, 255, 0), 2)
cv2.imshow("Outline", gray)
cv2.waitKey(0)
cv2.destroyAllWindows()

warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
T = threshold_local(warped, 11, offset=10, method="gaussian")
warped = (warped > T).astype("uint8") * 255

# show the scanned image and save one copy in out folder
print("STEP 3: Apply perspective transform")

imS = cv2.resize(warped, (650, 650))
cv2.imshow("output", imS)
#cv2.imwrite('out/' + 'Output Image.PNG', imS)
cv2.waitKey(0)
output = pytesseract.image_to_string(imS)
print(output)