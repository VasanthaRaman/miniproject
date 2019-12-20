import cv2
import pytesseract
import numpy as np

''' Read the image and convert it to grayscale '''
img = cv2.imread(r"C:\Users\Internship004\Desktop\Licenses\jap.tiff",1)
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

def clahe_try(img_rd):
    ''' Return image after applying clahe processing '''
    img_new = cv2.cvtColor(img_rd, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img_new = clahe.apply(img_new)
    return img_new


def unsharp_mask(img_rd, kernel_size=(5, 5), sigma=1.0, amount=1.0, thresh=0):
    '''  Return a sharpened version of the image, using an unsharp mask '''
    blurred = cv2.GaussianBlur(img_rd, kernel_size, sigma)
    sharpened = float(amount + 1) * img_rd - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if thresh > 0:
        low_contrast_mask = np.absolute(img_rd - blurred) < thresh
        np.copyto(sharpened, img_rd, where=low_contrast_mask)
    return sharpened

img = unsharp_mask(img)
# functon call
img = clahe_try(img)
cv2.imshow('jap',img)
''' List of available languages '''
languages = ['eng','hin','jpn','tam','mal']

''' Append STOP to terminate the choosing process '''
languages.append('stop')

print("\nChoose languages\n")
choice=True
lang=""

''' Allow user to select the required languages '''
while choice:
    for i in range(len(languages)):
        print(i+1,languages[i])
    ch=int(input("Enter: "))
    if(ch!=len(languages)):
        lang+=languages[ch-1]+'+'
    else:
        choice=False
print("Chosen language is:",lang[0:-1])

''' Pass the image to tesseract for the chosen languages '''
print(pytesseract.image_to_string(img,lang=lang[0:-1],config='--psm 6'))

# Close the displayed image after any key is pressed
cv2.waitKey()
cv2.destroyAllWindows()