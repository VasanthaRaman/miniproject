from flask import Flask
from flask import jsonify
from flask import request
import string

app = Flask(__name__)

newlist=[]
f=open('newjson.json','r',encoding='utf8')
for line in f:
	newlist.append(line)
f.close()
d={}
k=0
for i in range(len(newlist)):
    if(newlist[i] not in string.whitespace):
        k+=1
        d.update({"Line "+str(k):newlist[i]})
print(d)


quarks = [{'name': 'up', 'charge': '+2/3'},
          {'name': 'down', 'charge': '-1/3'},
          {'name': 'charm', 'charge': '+2/3'},
          {'name': 'strange', 'charge': '-1/3'}]

lines = {
  "Line 1": "India Driving Licence(Tamil Nadu) OG",
  "Line 2": "TNO6 2017 0011050 \u201d",
  "Line 3": "Date of Issue Validity",
  "Line 4": "13-12-2017 @ 12-12-2037",
  "Line 5": "Nationality",
  "Line 6": "INDIA",
  "Line 7": "4 Date of Birth Blood Group",
  "Line 8": "05-08-1999 B+",
  "Line 9": "Name",
  "Line 10": "| SITHARTHAN",
  "Line 11": "Father's Name",
  "Line 12": "S ILLANGOVAN"
}

@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({'message' : 'Hello, World!'})

@app.route('/quarks', methods=['GET'])
def returnAll():
    return jsonify({'quarks' : quarks})

@app.route('/op', methods=['GET'])
def returnAllLines():
    return jsonify({'lines' : d})

if __name__ == "__main__":
    app.run(port=4996,debug=True)