import cv2
import numpy as np
import pytesseract

blankimg = np.zeros([600,800,3],dtype=np.uint8)
blankimg.fill(255) # or img[:] = 255
#cv2.resize(img,(800,800))
cv2.imwrite("C:/Users/Internship004/Desktop/PanCards/blank.jpg",blankimg)
room = cv2.imread("C:/Users/Internship004/Desktop/PanCards/blank.jpg" )
logo = cv2.imread("C:/Users/Internship004/Desktop/PanCards/8crop.jpg" )
logo2 = cv2.imread("C:/Users/Internship004/Desktop/PanCards/11crop.jpg" )

#--- Resizing the logo to the shape of room image ---
#logo = cv2.resize(logo, (200,100))

#--- Apply Otsu threshold to blue channel of the logo image ---
ret, logo_mask = cv2.threshold(logo[:,:,0], 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
ret, logo_mask2 = cv2.threshold(logo2[:,:,0], 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
cv2.imshow('logo_mask', logo_mask)
cv2.imshow('logo2_mask', logo_mask2)
cv2.imwrite("C:/Users/Internship004/Desktop/name.png", logo_mask)
cv2.imwrite("C:/Users/Internship004/Desktop/number.png", logo_mask2)

room2 = room.copy() 

#--- Copy pixel values of logo image to room image wherever the mask is white ---
room2[np.where(logo_mask == 0)] = logo[np.where(logo_mask == 0)]
cv2.imwrite("C:/Users/Internship004/Desktop/room_result.JPG", room2)

room2 = cv2.imread("C:/Users/Internship004/Desktop/room_result.jpg")
room2[np.where(logo_mask2 == 0)] = logo2[np.where(logo_mask2 == 0)]
cv2.imwrite("C:/Users/Internship004/Desktop/room_result.JPG", room2)

cv2.waitKey()
cv2.destroyAllWindows()


'''
#
r1 = cv2.imread("C:/Users/Internship004/Desktop/name.png")
r1 = cv2.resize(r1,(r1.shape[1]*2,r1.shape[0]*2))
cv2.imshow("resize",r1)
print(pytesseract.image_to_string(r1))

r2 = cv2.imread("C:/Users/Internship004/Desktop/number.png")
print(pytesseract.image_to_string(r2))
#
'''