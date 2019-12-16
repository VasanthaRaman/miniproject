import cv2
import pytesseract
from pytesseract import Output

img = cv2.imread("C:/Users/Internship004/Desktop/PanCards/114.jpg")

img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.imshow("title.jpg",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
#result = pytesseract.image_to_string(img)
#print(result)
#words=result.split()
#print(words)
#print(result)
#print image_to_string(Image.open("C:/Users/Internship004/Desktop/Licenses/103.jpg"))
#print image_to_string(Image.open("C:/Users/Internship004/Desktop/Licenses/103.jpg"), lang='eng')
