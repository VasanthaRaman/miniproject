import cv2
import pytesseract
img=cv2.imread("C:/Users/Internship004/Desktop/Licenses/103.jpg")
I=cv2.imread("C:/Users/Internship004/Desktop/Licenses/103.jpg")
i=cv2.imread("C:/Users/Internship004/Desktop/Licenses/103.jpg")
G_Image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#Otsu Thresholding
blur = cv2.GaussianBlur(G_Image,(1,1),0)
ret,th = cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
image, contours, hierarchy = cv2.findContours(th,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
#img = cv2.drawContours(Image, contours, -1, (0,255,0), 3)

for contour in contours:
        # get rectangle bounding contour
        [x, y, w, h] = cv2.boundingRect(contour)

        if h>20:
            continue

        # draw rectangle around contour on original image
        cv2.rectangle(I, (x, y), (x + w, y + h), (255, 0, 255), 0)
cv2.imshow("New.jpg",I)
cv2.waitKey(0)
cv2.destroyAllWindows()