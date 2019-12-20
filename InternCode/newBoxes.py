import string
import cv2
import pytesseract
import numpy as np
import json

img = cv2.imread(r"C:\Users\Internship004\Desktop\Licenses\103.jpg",1)
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
#ret,img=  cv2.threshold(img,127,255,cv2.THRESH_TOZERO)
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
img = unsharp_mask(img)
w,h=img.shape[1], img.shape[0]
aspectRatio = w/h

# fix a width for passing to tesseract
fixedWidth=800

#resize the read image to the fixed resolution
img = cv2.resize(img,(fixedWidth,int(fixedWidth//aspectRatio)))
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

cv2.imshow('show',img)
text = pytesseract.image_to_data(img, output_type="data.frame")
#print(type(text))
text = text[text.conf != -1]
lines = text.groupby('block_num')['text'].apply(list)
conf = text.groupby(['block_num'])['conf'].mean()
#print(text)

confList = []
for i in range(len(text['conf'].values)):
    if(text['conf'].values[i]>=25 and text['text'].values[i] != 'nan' and 
       text['text'].values[i] not in string.punctuation and
       text['text'].values[i][0] not in string.whitespace):
        confList.append(text['text'].values[i])
confList.append("EOF")

#print(confList)
result = pytesseract.image_to_string(img)
#print(result)
words=result.split('\n')

l=[]
p=[]
q=[]
for i in words:
    l=i.split()
    for j in l:
        if j not in string.whitespace:
            p.append(i)

for i in p:
    if(i not in q):
        q.append(i)
#print(q)

d={}
for i in range(len(q)):
    d.update({"Line "+str(i+1):q[i]})

with open("C:/Users/Internship004/Desktop/newjson.json",'w') as jsonFile:
    json.dump(d,jsonFile,indent=2)

#close the json file   
jsonFile.close()

cnt=0
f = open("C:/Users/Internship004/Desktop/newjson.json",'r',encoding='utf8')
for line in f:
    cnt+=1
    if("Date of Birth" in line):
        break
for line in f:
    if("Line "+str(cnt) in line):
        print(line)
        break

cv2.waitKey()
cv2.destroyAllWindows()
