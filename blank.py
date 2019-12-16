import numpy as np
import cv2
img = np.zeros([512,512,3],dtype=np.uint8)
img.fill(255) # or img[:] = 255
#cv2.resize(img,(800,800))
cv2.imshow("blank.png",img)
cv2.waitKey(0)
cv2.destroyAllWindows()