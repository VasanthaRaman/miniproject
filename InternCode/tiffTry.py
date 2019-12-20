import cv2
import json
import string
import pytesseract
img = cv2.imread("C:/Users/Internship004/Desktop/Licenses/103.jpg")

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

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

words=[]
file = open('C:/Users/Internship004/Desktop/final.txt','r',encoding='utf8')
for line in file:
    w=line.split()
    for i in w:
        if(i[0] not in string.whitespace):
            words.append(i)
for p in range(len(words)):
    if(words[p][0] in string.punctuation):
        q = words[p][1:]
        words[p]=q
print(words)
file.close()
print()
print("Enter 1 for NAME, 2 for ADDRESS, 3 for DOB, 4 for ALL, 5 for JSON")
req = int(input("Enter required field:"))
if(req==1):
    for i in range(len(words)):
        k=i
        if(words[k]=="Name"):
            print("\n"+words[k])
            k+=1
            while(words[k]!="Address" and words[k]!="S/DIW"):
                print(words[k],end=" ")
                k+=1    
if(req==2):
    for i in range(len(words)):
        k=i
        if(words[k]=="Address"):
            print("\n"+words[k])
            k+=1
            while(words[k]!="D.O.B."):
                print(words[k],end=" ")
                k+=1
if(req==3):
    for i in range(len(words)):
        k=i
        if(words[k]=="D.O.B."):
            print("\n"+words[k])
            print(words[k+1])
if(req==4):
    for i in range(len(words)):
        k=i
        if(words[k]=="Name"):
            print("\n"+words[k])
            k+=1
            while(words[k]!="Address" and words[k]!="S/DIW"):
                print(words[k],end=" ")
                k+=1
    print()
    for i in range(len(words)):
        k=i
        if(words[k]=="Address"):
            print("\n"+words[k])
            k+=1
            while(words[k]!="D.O.B."):
                print(words[k],end=" ")
                k+=1
    print()
    for i in range(len(words)):
        k=i
        if(words[k]=="D.O.B."):
            print("\n"+words[k])
            print(words[k+1])
key,value="",""
jsonDict={}
if(req==5):
    for i in range(len(words)):
        k=i
        if(words[k]=="Name"):
            key+=words[k]
            print("\n"+words[k])
            k+=1
            while(words[k]!="Address" and words[k]!="S/DIW"):
                value+=words[k]+" "
                print(words[k],end=" ")
                k+=1
    jsonDict.update({key:value[0:-1]})
#     print(jsonDict)
    print()
    key,value="",""
    for i in range(len(words)):
        k=i
        if(words[k]=="Address"):
            key+=words[k]
            print("\n"+words[k])
            k+=1
            while(words[k]!="D.O.B."):
                value+=words[k]+" "
                print(words[k],end=" ")
                k+=1
    jsonDict.update({key:value[0:-1]})
    print()
    key,value="",""
    for i in range(len(words)):
        k=i
        if(words[k]=="D.O.B."):
            key+=words[k]
            print("\n"+words[k])
            value+=words[k+1]+" "
            print(words[k+1])
    jsonDict.update({key:value})
    print(jsonDict)
    with open("C:/Users/Internship004/Desktop/jsonfile.json","w") as jsonfile:
        json.dump(jsonDict,jsonfile)