from flask import Flask,request
import nltk
import os,sys
from Fetcher import fetchDataForProcessing
import re

app = Flask(__name__)

def extract(lst):
    if extractUnproperDateFromData(lst):
        return extractUnproperDateFromData(lst)
    elif  extractProperDateFromData(lst): 
        return  extractProperDateFromData(lst)
    print "false da cokme"
    return False

def extractUnproperDateFromData(lst):

 print "AAAAAA"   
 for i in range(0,len(lst[0])):
        if  i+2<len(lst[0]) and  lst[0][i] == "date" and lst[0][i+1] == "of" and lst[0][i+2] == "birth":
			print "bulma bunu"
			print lst[0][i+4]+" "+lst[0][i+5]+" "+lst[0][i+6]
			return lst[0][i+4]+" "+ lst[0][i+5]+ " " +lst[0][i+6]
 print "buradayimmmmm"
 return False
        
def extractProperDateFromData(lst):    
 print "BBB"
 for i in range(0,len(lst[0])):
    if "age|" in lst[0][i]:
        return lst[0][i].replace("|"," ")[lst[0][i].index("|"):]
 return False

    
def prepareDataForProccessing(NAME):
    
    data = fetchDataForProcessing(NAME)
    tokenized_data = nltk.word_tokenize(str(data).lower())
    converted_data = nltk.Text(tokenized_data)
    mydata=  nltk.ConcordanceIndex(converted_data.tokens, key = lambda s: s.lower())
    concordance_txt = ([converted_data.tokens[map(lambda x: x-5 if (x-10)>0 else 0,[offset])[0]:offset+10]
                        for offset in mydata.offsets("birth")])
    return concordance_txt



def extractVerb(possed_data):
    for element in possed_data:
        if element[1] == 'VBD' or element[1] == 'VBZ':
            return element[0]

def extractNoun(possed_data):
    result =""
    for element in possed_data:
        if element[1] == 'NNP':
          result +=   element[0] + "_" 
    return result[0:len(result)-1]


            

def processQuestion(questionSentence): 
    tokenized_data = nltk.word_tokenize(questionSentence)
    possed_data = nltk.pos_tag(tokenized_data)
    return extractNoun(possed_data)






@app.route("/",methods=['GET','POST'])
def hello():
	if request.method == 'POST':
	 question = request.form.get('gozde')
	 print question
	 name = processQuestion(question)
	 print name
	 lst = prepareDataForProccessing(name)
	 if len(lst)>0:
	 	return extract(lst)
	 return "sss"
	 return "<p>Ok dddd</p>"
	return """<img style="width:400px;height:400px;margin-top:10%;margin-left:40%" src='http://orig02.deviantart.net/9915/f/2008/349/f/5/corpse_bride_by_linalightning.jpg' ><form style="margin-left:40%;margin-top:12%" action='/' method='POST'>
              <input style="width:400px;height:80px;" name='gozde' type= 'text'>
              <input type = 'submit'></form>"""

if __name__ == "__main__":
    app.run()