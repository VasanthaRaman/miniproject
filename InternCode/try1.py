import cv2
import json
import string
import pytesseract
img = cv2.imread("C:/Users/Internship004/Desktop/NewLicenses/L4.jpg")

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2.imshow('sk',img)
cv2.imwrite("C:/Users/Internship004/newL1.jpg",img)
res = pytesseract.image_to_string(img)
words=res.split()
print(words)
print("------------------------------------------------------------------")
print("------------------------------------------------------------------")
print("------------------------------------------------------------------")
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
l.append("EOF")
print(l)
print("------------------------------------------------------------------")
print(len(l))
#cv2.waitKey()
#cv2.destroyAllWindows()
fields = ['Name','DateofBirth','Nationality','DateofIssue','Validity',"Father'sName","BloodGroup","DaieofBirth","FathersName"]
copyF = fields.copy()
c=3
newlist = []
i=0
while(i<len(l)):
    k=i
    if(l[k]!="EOF"):
        check=l[k]
        j=0
        while(check not in fields and j<(c-1)):
            k+=1
            if(l[k]!="EOF"):
                check+=l[k]
                j+=1
            else:
                break
        print(check)
        if(check in fields):
            fields.remove(check)
            newlist.append(check)
            i+=j+1
        else:
            newlist.append(l[i])
            i+=1
    else:
        break
print("------------------------------------------------------------------")
newlist.append("EOF")
print(newlist)
fakelist = newlist.copy()
mainlist=[]
for i in range(len(fakelist)):
    if(fakelist[i]=="DateofIssue" or fakelist[i]=="Validity" or fakelist[i]=="DateofBirth" or fakelist[i]=="DaieofBirth" or fakelist[i]=="BloodGroup"):
        if(fakelist[i+2] not in copyF):
            mainlist.append(fakelist[i])
            mainlist.append(fakelist[i+2])
    elif(fakelist[i] in copyF and (fakelist[i]!="DateofIssue" or fakelist[i]!="Validity" or fakelist[i]!="DateofBirth" or fakelist[i]!="BloodGroup")):
        k=i
        mainlist.append(fakelist[k])
        k+=1
        while(fakelist[k] not in copyF and fakelist[k]!="EOF"):
            mainlist.append(fakelist[k])
            k+=1
mainlist.append("EOF")
print("------------------------------------------------------------------")
print("------------------------------------------------------------------")
print("------------------------------------------------------------------")
print("------------------------------------------------------------------")
print(mainlist)

maindict={}
i=0
while(i<len(mainlist)):
   key,value="",""
   if (mainlist[i]!='EOF'):
       key=mainlist[i]
       i+=1
       while(mainlist[i]!='EOF' and mainlist[i] not in copyF):
           value+=mainlist[i]+" "
           i+=1
       maindict.update({key:value[0:-1]}) 
   else:
       break
#   maindict.update({key:value[0:-1]}) 
print(maindict)
print("------------------------------------------------------------------")
print("------------------------------------------------------------------")
print('DONE')
with open("C:/Users/Internship004/Desktop/newjson.json",'w') as jf:
    json.dump(maindict,jf)