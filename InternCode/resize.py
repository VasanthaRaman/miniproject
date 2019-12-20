import cv2
img = cv2.imread("C:/Users/Internship004/Desktop/PanCards/2000.jpg")
img = cv2.resize(img, (0,0), fx = 0.5, fy = 0.5)
cv2.imshow('newres',img)
cv2.imwrite("C:/Users/Internship004/Desktop/PanCards/newres.jpg",img)
cv2.waitKey()
cv2.destroyAllWindows()