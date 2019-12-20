"""
TEXT EXTRACTION FROM IMAGES
"""
import sys
import string
import json
import numpy as np
import pytesseract
import cv2 as cv
from crop_orient_mix import crop_orient
# Read the image
if len(sys.argv) == 2:
    PATH = sys.argv[1]
    IMG = cv.imread(PATH, 1)
    IMG = crop_orient(PATH, IMG)
    # Improvise RGB ratio of the image
    IMG = cv.cvtColor(IMG, cv.COLOR_BGR2RGB)
    
    
    def clahe_try(img_rd):
        """ Return image after applying clahe processing """
        img_new = cv.cvtColor(img_rd, cv.COLOR_BGR2GRAY)
        clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        img_new = clahe.apply(img_new)
        return img_new
    
    
    def unsharp_mask(img_rd, kernel_size=(5, 5), sigma=1.0, amount=1.0, thresh=0):
        """  Return a sharpened version of the image, using an unsharp mask """
        blurred = cv.GaussianBlur(img_rd, kernel_size, sigma)
        sharpened = float(amount + 1) * img_rd - float(amount) * blurred
        sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
        sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
        sharpened = sharpened.round().astype(np.uint8)
        if thresh > 0:
            low_contrast_mask = np.absolute(img_rd - blurred) < thresh
            np.copyto(sharpened, img_rd, where=low_contrast_mask)
        return sharpened
    
    
    # Get the width and height of the image
    H, W = list(IMG.shape)[0], list(IMG.shape)[1]
    
    # Calculate aspect ratio
    ASPECTRATIO = W/H
    
    # Fix a width for passing to tesseract
    FIXEDWIDTH = 700
    
    # Resize the read image to the fixed resolution
    IMG = cv.resize(IMG, (FIXEDWIDTH, int(FIXEDWIDTH//ASPECTRATIO)))
    
    IMG = unsharp_mask(IMG)
    # functon call
    IMG = clahe_try(IMG)
    
    # show and save final image
    cv.imshow('show', IMG)
    cv.imwrite('output.jpg', IMG)
    
    # Pass the image to tesseract and convert it as a dataframe
    TEXT = pytesseract.image_to_data(IMG, output_type='data.frame')
    
    # Remove the WORDS with negative CONFidence scores
    TEXT = TEXT[TEXT.conf != -1]
    LINES = TEXT.groupby('block_num')['text'].apply(list)
    CONF = TEXT.groupby(['block_num'])['conf'].mean()
    
    # Remove punctuations from the extracted TEXT and append
    # the remaining to a new list
    CONFLIST = []
    for i in range(len(TEXT['conf'].values)):
        if(TEXT['conf'].values[i] >= 25 and TEXT['text'].values[i] != 'nan' and
           TEXT['text'].values[i] not in string.punctuation and
           TEXT['text'].values[i][0] not in string.whitespace):
            CONFLIST.append(TEXT['text'].values[i])
    CONFLIST.append('EOF')
    
    # Pass the image to pytesseract to extract the TEXT from the image
    RESULT = pytesseract.image_to_string(IMG)
    
    # Remove white spaces from the extracted TEXT and append the wanted TEXT
    NEWLIST = []
    EACHLINE = RESULT.split('\n')
    for i in EACHLINE:
        NEWSTR = ''
        WORDS = i.split()
        for k in WORDS:
            if k in CONFLIST:
                NEWSTR += k+' '
        NEWLIST.append(NEWSTR[0:-1])
    
    # remove special characters and white spaces from the list
    for i in NEWLIST:
        if i in string.whitespace or i in string.punctuation:
            NEWLIST.remove(i)
    
    # Update the dictionary with line number and the line contents
    D = {}
    k = 0
    for i, j in enumerate(NEWLIST, 1):
        if j not in string.whitespace:
            k += 1
            D.update({'Line '+str(k): j})
    
    # Open a json file and dump the dictionary into it
    with open('C:/Users/Internship004/Desktop/newjson.json', 'w') as jsonfile:
        json.dump(D, jsonfile, indent=2)
    
    # Close the json file
    jsonfile.close()
    
    # Extract the required field from the json file
    CNT = 0
    F = open('C:/Users/Internship004/Desktop/newjson.json', 'r', encoding='utf8')
    for LINE in F:
        CNT += 1
        if 'Date of Issue' in LINE:
            break
    for LINE in F:
        if 'Line '+str(CNT) in LINE:
            print(LINE)
            break
    
    # Close the displayed image after any key is pressed
    cv.waitKey()
    cv.destroyAllWindows()
else:
    print('Insufficient arguments')
