
import cv2
import numpy
import io
from PIL import Image
#img = cv2.imread('C:/Users/Internship004/Desktop/NewLicenses/sidhu.jpg')
#string = cv2.imencode('.jpg', img)[1].tostring()
#f=open('C:/Users/Internship004/Desktop/b64.txt','wb')
#f.write(string)
#f.close()
f = open('C:/Users/Internship004/Desktop/b64.txt','rb')
string = f.read()
image = numpy.array(Image.open(io.BytesIO(string)))
#cv2.imshow('hi',numpy.asarray(image))

im1 = cv2.imread('C:/Users/Internship004/Desktop/NewLicenses/sidhu.jpg')
im1=cv2.resize(im1,(600,600))
cv2.imshow('n1',im1)

im2 = numpy.asarray(image)
im2=cv2.resize(im2,(600,600))
im2=cv2.cvtColor(im2,cv2.COLOR_RGB2BGR)
cv2.imshow('n2',im2)

cv2.waitKey()
cv2.destroyAllWindows()