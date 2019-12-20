import cv2
import string
import pytesseract
import numpy as np
from skimage.filters import threshold_local
img = cv2.imread("C:/Users/Internship004/Desktop/NewLicenses/baspic.jpg")
#img = cv2.resize(img,(img.shape[1]//2,img.shape[0]//2))
#img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#img = cv2.cvtColor(img, cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
def unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
    """Return a sharpened version of the image, using an unsharp mask."""
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
    return sharpened
img=unsharp_mask(img)
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


cv2.imshow('t3',img)

cf = "-l eng --psm 6"
result = pytesseract.image_to_string(img)


print("------------------------------------------------------------------")
print("------------------------------------------------------------------")
text = pytesseract.image_to_data(img, output_type="data.frame")
text = text[text.conf != -1]
lines = text.groupby('block_num')['text'].apply(list)
conf = text.groupby(['block_num'])['conf'].mean()
print(text)
print("------------------------------------------------------------------")
print("------------------------------------------------------------------")
l = []
for i in range(len(text['conf'].values)):
    if(text['conf'].values[i]>=50 and text['text'].values[i] != 'nan' and 
       text['text'].values[i] not in string.punctuation and
       text['text'].values[i][0] not in string.whitespace):
        l.append(text['text'].values[i])
l.append("EOF")
print(l)
print("------------------------------------------------------------------")
print("------------------------------------------------------------------")
print(result)

newlist=[]
lns = result.split("\n")
for i in lns:
    newstr=""
    ww = i.split()
    for k in ww:
        if k in l:
            newstr+=k+" "
    newlist.append(newstr[0:-1])
print(newlist)
#words = result.split("\n")
#for i in words:
#    if i in string.whitespace:
#        words.remove(i)
#d={}
#for i in range(len(words)):
#    d.update({"Line "+str(i+1):words[i]})
#print(d)
cv2.waitKey()
cv2.destroyAllWindows()