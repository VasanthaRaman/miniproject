from PIL import Image 

blank = Image.open("C:/Users/Internship004/Desktop/PanCards/blank.jpg")
# open the image 
Image1 = Image.open("C:/Users/Internship004/Desktop/PanCards/2000.jpg") 
  
# make a copy the image so that  
# the original image does not get affected 
Image1copy = Image1.copy() 
Image2 = Image.open("C:/Users/Internship004/Desktop/PanCards/8crop.jpg") 
Image2copy = Image2.copy() 
  
# paste image giving dimensions 
Image1copy.paste(Image2copy, (70, 150)) 
  
# save the image  
Image1copy.save("C:/Users/Internship004/Desktop/PanCards/pasted.jpg")