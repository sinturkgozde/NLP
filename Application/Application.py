from flask import Flask,request
import nltk
import os,sys
import urllib2
import re

app = Flask(__name__)

def extract(lst):
    if extractUnproperDateFromData(lst):
        return extractUnproperDateFromData(lst)
    elif  extractProperDateFromData(lst): 
        return  extractProperDateFromData(lst)
    return "Enter a person name"

def extractUnproperDateFromData(lst):
    
 for i in range(0,len(lst[0])):
        if lst[0][i] == "date" and lst[0][i+1] == "of" and lst[0][i+2] == "birth":
            return lst[0][i+4]+" "+ lst[0][i+5]+ " " +lst[0][i+6]
 return False
        
def extractProperDateFromData(lst):    
 for i in range(0,len(lst[0])):
    if "age|" in lst[0][i]:
        return lst[0][i].replace("|"," ")[lst[0][i].index("|"):]
 return False

    
def prepareDataForProccessing(NAME):
    
    data = urllib2.urlopen("https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles="+ NAME + "&rvprop=content&redirects=true&format=json").read().decode('utf8')
    tokenized_data = nltk.word_tokenize(str(data).lower())
    converted_data = nltk.Text(tokenized_data)
    mydata=  nltk.ConcordanceIndex(converted_data.tokens, key = lambda s: s.lower())
    concordance_txt = ([converted_data.tokens[map(lambda x: x-5 if (x-10)>0 else 0,[offset])[0]:offset+10]
                        for offset in mydata.offsets("birth")])
    return concordance_txt

dataPrepared= prepareDataForProccessing("Xi_Jinping")

print extract(dataPrepared)

@app.route("/",methods=['GET','POST'])
def hello():
	if request.method == 'POST':
	 lst = prepareDataForProccessing(request.form.get('gozde'))
	 return extract(lst)
	 return "<p>Ok dddd</p>"
	return """<img style="width:400px;height:400px;margin-top:10%;margin-left:40%" src='http://orig02.deviantart.net/9915/f/2008/349/f/5/corpse_bride_by_linalightning.jpg' ><form style="margin-left:40%;margin-top:12%" action='/' method='POST'>
              <input style="width:400px;height:80px;" name='gozde' type= 'text'>
              <input type = 'submit'></form>"""

if __name__ == "__main__":
    app.run()