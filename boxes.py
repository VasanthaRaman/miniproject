import string
import cv2
import pytesseract
import numpy as np
import json

''' Read the image '''
img = cv2.imread(r"C:\Users\Internship004\Desktop\NewLicenses/basha.jpg",1)

''' Improvise RGB ratio of the image '''
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

'''Return a sharpened version of the image, using an unsharp mask.'''
def unsharp_mask(img, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
    blurred = cv2.GaussianBlur(img, kernel_size, sigma)
    sharpened = float(amount + 1) * img - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(img - blurred) < threshold
        np.copyto(sharpened, img, where=low_contrast_mask)
    return sharpened

''' Function call '''
img = unsharp_mask(img)

''' Get the width and height of the image '''
w,h=img.shape[1], img.shape[0]

''' Calculate aspect ratio '''
aspectRatio = w/h

''' Fix a width for passing to tesseract'''
fixedWidth=700

''' Resize the read image to the fixed resolution'''
img = cv2.resize(img,(fixedWidth,int(fixedWidth//aspectRatio)))

''' Convert the image to grayscale '''
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

cv2.imshow('show',img)

''' Pass the image to tesseract and convert it as a dataframe '''
text = pytesseract.image_to_data(img, output_type="data.frame")

''' Remove the words with negative confidence scores '''
text = text[text.conf != -1]
lines = text.groupby('block_num')['text'].apply(list)
conf = text.groupby(['block_num'])['conf'].mean()

''' Remove punctuations from the extracted text and append the remaining to a new list '''
confList = []
for i in range(len(text['conf'].values)):
    if(text['conf'].values[i]>=50 and text['text'].values[i] != 'nan' and 
       text['text'].values[i] not in string.punctuation and
       text['text'].values[i][0] not in string.whitespace):
        confList.append(text['text'].values[i])
confList.append("EOF")

''' Pass the image to pytesseract to extract the text from the image '''
result = pytesseract.image_to_string(img)

''' Split the extracted text line-by-line '''
words=result.split('\n')

''' Remove white spaces from the extracted text and append the wanted text '''
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

''' Update the dictionary with line number and the line contents '''
d={}
for i in range(len(q)):
    d.update({"Line "+str(i+1):q[i]})

''' Open a json file and dump the dictionary into it '''
with open("C:/Users/Internship004/Desktop/newjson.json",'w') as jsonFile:
    json.dump(d,jsonFile,indent=2)

''' Close the json file '''   
jsonFile.close()

''' Extract the required field from the json file '''
cnt=0
f = open("C:/Users/Internship004/Desktop/newjson.json",'r',encoding='utf8')
for line in f:
    cnt+=1
    if("Date of Issue" in line):
        break
for line in f:
    if("Line "+str(cnt) in line):
        print(line)
        break

''' Close the displayed image after any key is pressed '''
cv2.waitKey()
cv2.destroyAllWindows()