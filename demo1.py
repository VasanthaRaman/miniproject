import cv2
import string
import pytesseract
img = cv2.imread("C:/Users/Internship004/Desktop/Licenses/103.jpg")

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print("qwertyui")
text = pytesseract.image_to_data(img, output_type="data.frame")
text = text[text.conf != -1]
lines = text.groupby('block_num')['text'].apply(list)
conf = text.groupby(['block_num'])['conf'].mean()

print("------------------------------------------------------------------")
l = []
for i in range(len(text['conf'].values)):
    if(text['conf'].values[i]>=50 and text['text'].values[i] != 'nan' and 
       text['text'].values[i] not in string.punctuation and
       text['text'].values[i][0] not in string.whitespace):
        l.append(text['text'].values[i])
print(l)
print("------------------------------------------------------------------")

file = open('C:/Users/Internship004/out.txt','r',encoding='utf8')
opfile = open('C:/Users/Internship004/Desktop/final.txt','w')
for line in file:
    print(str(line))

    wl=line.split()
    for i in wl:
        if i in l:
            opfile.write(i+' ')
    opfile.write('\n')
file.close()
opfile.close()

print("asdcsvzad")