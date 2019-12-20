import cv2
import numpy as np
import math
import pytesseract
from scipy import ndimage

## (1) read
img = cv2.imread(r"C:\Users\Internship004\Desktop\rot2.jpg")

''' Get the width and height of the image '''
w,h=img.shape[1], img.shape[0]

''' Calculate aspect ratio '''
aspectRatio = w/h

''' Fix a width for passing to tesseract'''
fixedWidth=700

''' Resize the read image to the fixed resolution'''
img2 = cv2.resize(img,(fixedWidth,int(fixedWidth//aspectRatio)))

gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

img_edges = cv2.Canny(gray, 100, 100, apertureSize=3)
    # Using Houghlines to detect lines
lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=100, maxLineGap=5)

angles = []
for x1, y1, x2, y2 in lines[0]:
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
    angles.append(angle)

# Getting the median angle
median_angle = np.median(angles)
print(median_angle)

if(median_angle<3):
     cv2.imshow('orig',img)
     cv2.imwrite('orig.jpg', img)
else:
    # Rotating the image with this median angle
    img_rotated = ndimage.rotate(img2, median_angle)
    img_rotated2=cv2.rotate(img_rotated,cv2.ROTATE_180)
    
    cv2.imwrite('orientation_corrected.jpg', img_rotated)
    cv2.imwrite('orientation_corrected2.jpg', img_rotated2)
    
    
    ''' Pass the image to tesseract and convert it as a dataframe '''
    text1 = pytesseract.image_to_data(img_rotated, output_type="data.frame")
    text2 = pytesseract.image_to_data(img_rotated2, output_type="data.frame")
    
    ''' Remove the words with negative confidence scores '''
    text1 = text1[text1.conf != -1]
    lines = text1.groupby('block_num')['text'].apply(list)
    conf1 = text1.groupby(['block_num'])['conf'].mean()
    
    text2 = text2[text2.conf != -1]
    lines = text2.groupby('block_num')['text'].apply(list)
    conf2 = text2.groupby(['block_num'])['conf'].mean()

    if(conf1.mean()>conf2.mean()):
        cv2.imshow('orig',img_rotated)
        #print(r1)
        cv2.imwrite('orig.jpg', img_rotated)
    else:
        cv2.imshow('orig',img_rotated2)
        cv2.imwrite('orig.jpg',img_rotated2)
    #print(r2)
cv2.waitKey()
cv2.destroyAllWindows()