# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 15:26:18 2019

@author: Internship004
"""

import cv2
import pytesseract

''' Read the image and convert it to grayscale '''
img = cv2.imread(r"C:\Users\Internship004\newjap.tiff")
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

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