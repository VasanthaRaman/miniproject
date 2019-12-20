import cv2
import string
import pytesseract
import numpy as np
import json


# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 5)


# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


# erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)


# skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

img = cv2.imread(r"C:\Users\Internship005\Desktop\imgs\203.jpeg")
img = cv2.resize(img,(img.shape[1]//2, img.shape[0]//2))
#img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
#img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
#cv2.imshow('sample',img)

gray = get_grayscale(img)
cv2.imshow('gray',gray)
blurred=remove_noise(img)
cv2.imshow('blurr',blurred)
thresh = thresholding(gray)
cv2.imshow('thresh',thresh)
opening = opening(gray)
cv2.imshow('opening',opening)
canny = canny(gray)
cv2.imshow('canny',canny)
eroded=erode(gray)
cv2.imshow('erodd',eroded)
deskwed=deskew(img)
cv2.imshow('deskewd',deskwed)
def unsharp_mask(img, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
    """Return a sharpened version of the image, using an unsharp mask."""
    blurred = cv2.GaussianBlur(img, kernel_size, sigma)
    sharpened = float(amount + 1) * img - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(img - blurred) < threshold
        np.copyto(sharpened, img, where=low_contrast_mask)
    return sharpened
img=unsharp_mask(img)


ret,thresh4 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO)

cv2.imshow('sample4',thresh4)
thresh4 = cv2.cvtColor(thresh4, cv2.COLOR_BGR2GRAY)

#print("------------------------------------------------------------------")
cf = "-l eng --psm 6"
result = pytesseract.image_to_string(thresh4)
print(result)

#print("------------------------------------------------------------------")
#print("------------------------------------------------------------------")
text = pytesseract.image_to_data(thresh4, output_type="data.frame")
text = text[text.conf != -1]
lines = text.groupby('block_num')['text'].apply(list)
conf = text.groupby(['block_num'])['conf'].mean()
print(text)
#print("------------------------------------------------------------------")

l = []
for i in range(len(text['conf'].values)):
    if(text['conf'].values[i]>=20 and text['text'].values[i] != 'nan' and 
       text['text'].values[i] not in string.punctuation and
       text['text'].values[i][0] not in string.whitespace):
        l.append(text['text'].values[i])
l.append("EOF")
#print(l)
#print("------------------------------------------------------------------")

newlist=[]
lns = result.split("\n")
for i in lns:
    newstr=""
    ww = i.split()
    for k in ww:
        if k in l:
            newstr+=k+" "
    newlist.append(newstr[0:-1])
#print(newlist)
#print("------------------------------------------------------------------")
#print("------------------------------------------------------------------")
for i in newlist:
    if i in string.whitespace or i in string.punctuation or i=="'":
        newlist.remove(i)
#print(newlist)
#print("------------------------------------------------------------------")
#print("------------------------------------------------------------------")
d={}
k=0
for i in range(len(newlist)):
    if(newlist[i] not in string.whitespace):
        k+=1
        d.update({"Line "+str(k):newlist[i]})
print(d)

with open("C:/Users/Internship005/Desktop/newjson.json",'w') as jf:
    json.dump(d,jf,indent=2)
jf.close()
cv2.waitKey()
cv2.destroyAllWindows()