import cv2
from PIL import Image
import numpy as np
from imutils import contours

thresh_area=2048.0
img=cv2.imread("C:/Users/Internship004/Desktop/PanCards/2000.jpg")
img = cv2.resize(img,(800,800))
rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(rgb,cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray,(5,5),0)
#--- performing Otsu threshold ---
_,thresh1 = cv2.threshold(gray, 0, 255,cv2.THRESH_OTSU|cv2.THRESH_BINARY_INV)
#cv2.imshow('thresh1.jpg', thresh1)

rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 3))
dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
#cv2.imshow('dilation.jpg', dilation)

_, cntrs, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cntrs = contours.sort_contours(cntrs,method="top-to-bottom")[0]
im2 = gray.copy()
i=0
maxw,sumh=0,0
mul=2
widthList = []
for cnt in cntrs:
    area=cv2.contourArea(cnt)
    if(area>=thresh_area):
        i+=1
        im2 = gray.copy()
        x, y, w, h = cv2.boundingRect(cnt)
        sumh+=h
        widthList.append(w)
        print(h)
        crop_img = im2[y:y+h, x:x+w]
        crop_img = cv2.resize(crop_img,((crop_img.shape[1])*mul,(crop_img.shape[0])*mul))
        ret, cmask = cv2.threshold(crop_img,127, 255, cv2.THRESH_BINARY)
        adap_thresh = cv2.adaptiveThreshold(crop_img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
        gaus_thresh = cv2.adaptiveThreshold(crop_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
        cv2.imwrite("C:/Users/Internship004/Desktop/PanCards/newset/"+str(i)+"cntr.jpg",gaus_thresh)
#             pr = cv2.imread("C:/Users/Internship004/Desktop/PanCards/crop.jpg")
#             print(pytesseract.image_to_string(pr))
        roi = cv2.rectangle(im2, (x, y), (x + w, y + h), (255,0,255), 0)
        cv2.imwrite("C:/Users/Internship004/Desktop/crops/"+str(i)+".jpg",roi)
maxw = widthList[0]
for itr in widthList:
    if itr>maxw:
        maxw = itr
print(widthList)
print(maxw,sumh)
blankimg = np.zeros([(sumh*mul)+100,(maxw*mul)+100,3],dtype=np.uint8)
blankimg.fill(255)
cv2.imwrite("C:/Users/Internship004/Desktop/PanCards/newset/blank.jpg",blankimg)

blank = Image.open("C:/Users/Internship004/Desktop/PanCards/newset/blank.jpg")

x,sumy=50,1

for j in range(i):
    pst = Image.open("C:/Users/Internship004/Desktop/PanCards/newset/"+str(j+1)+"cntr.jpg")
    blank.paste(pst, (0+x,1+sumy))
    sumy+=pst.size[1]

blank.save("C:/Users/Internship004/Desktop/PanCards/newset/processed.jpg")
    
#cv2.imshow('final.jpg', im2)
#cv2.imwrite("C:/Users/Internship004/Desktop/Licenses/contour.jpg",im2)

cv2.waitKey()
cv2.destroyAllWindows()