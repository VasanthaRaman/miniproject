#import required packages
import cv2
import string
import pytesseract
import numpy as np
import json

#This function sharpens the image
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

#read the image from local file system
img = cv2.imread("C:/Users/Internship004/Desktop/NewLicenses/sidpic.jpg",0)

# get width and height of the image and calculate aspect ratio
w,h=img.shape[1], img.shape[0]
aspectRatio = w/h

# fix a width for passing to tesseract
fixedWidth=600
kernel = np.ones((5,5), np.uint8)
#resize the read image to the fixed resolution
imgM = cv2.resize(img,(fixedWidth,int(fixedWidth//aspectRatio)))

img1 = imgM.copy()
img1 = cv2.GaussianBlur(img1,(5,5),0)
ret,img1 = cv2.threshold(img1,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imshow('c1',img1)

img2 = imgM.copy()
img2 = cv2.adaptiveThreshold(img2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
img2 = cv2.GaussianBlur(img2,(5,5),0)
img2Erode = cv2.erode(img2, kernel, iterations=1) 
cv2.imshow('c6',img2Erode)
img2Dil = cv2.dilate(img2, kernel, iterations=1)
cv2.imshow('c6',img2Dil)
img2M = cv2.erode(img2Dil, kernel, iterations=1)
result = pytesseract.image_to_string(img2M)
print(result)
print("------------------------------------")
cv2.imshow('c2',img2)

img3 = imgM.copy()
img3 = cv2.medianBlur(img3,5)
ret,img3 = cv2.threshold(img3,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imshow('c3',img3)

img4 = imgM.copy()
img4 = cv2.medianBlur(img4,5)
img4 = cv2.adaptiveThreshold(img4,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
cv2.imshow('c4',img4)

img5 = imgM.copy()
ret,img5 = cv2.threshold(img5,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
img5=unsharp_mask(img5)
cv2.imshow('c5',img5)
result = pytesseract.image_to_string(img5)
print(result)
print("------------------------------------")


img6 = imgM.copy()
img6 = cv2.adaptiveThreshold(img6,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
img6=unsharp_mask(img6)

result = pytesseract.image_to_string(img6)
print(result)
print("------------------------------------")

# Taking a matrix of size 5 as the kernel 

#sharpen the image
#img=unsharp_mask(img)
#
##apply TOZERO thresholding for extra clarity
##ret,img = cv2.threshold(img,127,255,cv2.THRESH_TOZERO)
##
###convert the image to grayscale
##img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#
##display the processed image
#cv2.imshow('processed image',img)
#
##set configuration to be passed to the tesseract(set only if required)
#configuration = "-l eng"
#
##pass the processed image to tesseract to extract text
#result = pytesseract.image_to_string(img)
#
##extract text from image and store as a dataframe
##This part of the code gives the CONFIDENCE SCORES of each word extracted from the image
##With this CONFIDENCE SCORE the junk values can be removed
#text = pytesseract.image_to_data(img, output_type="data.frame")
#print(type(text))
#text = text[text.conf != -1]
#lines = text.groupby('block_num')['text'].apply(list)
#conf = text.groupby(['block_num'])['conf'].mean()
#print(text)
##Append the words that pass the threshold value into the list
#confList = []
#for i in range(len(text['conf'].values)):
#    if(text['conf'].values[i]>=25 and text['text'].values[i] != 'nan' and 
#       text['text'].values[i] not in string.punctuation and
#       text['text'].values[i][0] not in string.whitespace):
#        confList.append(text['text'].values[i])
#confList.append("EOF")
#
##store all the required values line by line by comparing it with the extracted text
#newlist=[]
#eachLine = result.split("\n")
#for i in eachLine:
#    newstr=""
#    words = i.split()
#    for k in words:
#        if k in confList:
#            newstr+=k+" "
#    newlist.append(newstr[0:-1])
#
##remove special characters and white spaces from the list
#for i in newlist:
#    if i in string.whitespace or i in string.punctuation:
#        newlist.remove(i)
#
##create new dictionary d{} so that json file can be created easily
#d={}
#k=0
#for i in range(len(newlist)):
#    if(newlist[i] not in string.whitespace):
#        k+=1
#        #Update the dictionary with Line Number and the corresponding line value 
#        d.update({"Line "+str(k):newlist[i]})
#
##open a json file to output the dictionary
#with open("C:/Users/Internship004/Desktop/newjson.json",'w') as jsonFile:
#    json.dump(d,jsonFile,indent=2)
#
##close the json file   
#jsonFile.close()

#These 2 functions are to close the displayed image (Image closes whenever any key is pressed)
cv2.waitKey()
cv2.destroyAllWindows()