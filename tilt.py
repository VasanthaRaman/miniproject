import cv2
import numpy as np

img = cv2.imread('C:/Users/Internship004/Downloads/IMG_20191206_164454.jpg')
rows, cols, ch = img.shape    
pts1 = np.float32(
    [[cols*.25, rows*.95],
     [cols*.90, rows*.95],
     [cols*.10, 0],
     [cols,     0]]
)
pts2 = np.float32(
    [[cols*0.1, rows],
     [cols,     rows],
     [0,        0],
     [cols,     0]]
)    
M = cv2.getPerspectiveTransform(pts1,pts2)
dst = cv2.warpPerspective(img, M, (cols, rows))
cv2.imshow('sample', dst)
#cv2.imwrite('zen.jpg', dst)
cv2.waitKey()
