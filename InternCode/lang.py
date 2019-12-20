import cv2
import pytesseract
import re
import numpy as np

img = cv2.imread("C:/Users/Internship004/Desktop/NewLicenses/baspic.jpg")
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
#img = cv2.imread("C:/Users/Internship004/Desktop/abcd.jpg")

# get width and height of the image and calculate aspect ratio
w,h=img.shape[1], img.shape[0]
aspectRatio = w/h

# fix a width for passing to tesseract
fixedWidth=600

#resize the read image to the fixed resolution
img = cv2.resize(img,(fixedWidth,int(fixedWidth//aspectRatio)))
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

#sharpen the image
img=unsharp_mask(img)

#apply TOZERO thresholding for extra clarity
ret,img = cv2.threshold(img,127,255,cv2.THRESH_TOZERO)

#convert the image to grayscale
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#display the processed image
cv2.imshow('processed image',img)
custom_config = r"-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/-\'\ ():"
osd = pytesseract.image_to_string(img,config=custom_config)
#angle = re.search('(?<=Rotate: )\d+', osd).group(0)
#script = re.search('(?<=Script: )\d+', osd).group(0)

print(osd)
cv2.waitKey()
cv2.destroyAllWindows()