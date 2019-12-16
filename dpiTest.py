from PIL import Image
import pytesseract
import cv2
im = Image.open("C:/Users/Internship004/Desktop/PanCards/114.jpg")
im.save("C:/Users/Internship004/Desktop/PanCards/tank.jpg",dpi=(300,300))

print(pytesseract.image_to_string(im))
print("---------------------------------")
newim = cv2.imread("C:/Users/Internship004/Desktop/PanCards/tank.jpg")
#newim = cv2.
print(pytesseract.image_to_string(newim))