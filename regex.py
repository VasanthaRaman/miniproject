import re
import pytesseract
import cv2

img = cv2.imread("C:/Users/Internship004/L1.jpg")
f = re.compile(r'Nationality+\s*\w*')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
res = pytesseract.image_to_string(img,config="-l eng --psm 4")
print(res)
x = re.findall(f,res)
print(x)