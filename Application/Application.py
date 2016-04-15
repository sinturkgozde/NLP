from flask import Flask,request
import nltk
import os,sys
import urllib2
import re
import work
import Fetcher

app = Flask(__name__)



model = work.loadModel_two("our.model")


@app.route("/",methods=['GET','POST'])
def hello():
	if request.method == 'POST':
		lst = request.form.get('gozde')
		noun_and_verb =  work.extractNounAndVerb(lst)
		name = noun_and_verb["name"]
		verb = noun_and_verb["verb"]
		data = work.myGetForTest(name)
		result = work.extractSimilarSentences(name,verb,data,model)
		print result
		return str(result)

	return """<img style="width:400px;height:400px;margin-top:10%;margin-left:40%" src='http://orig02.deviantart.net/9915/f/2008/349/f/5/corpse_bride_by_linalightning.jpg' >
	           <form style="margin-left:40%;margin-top:12%" action='/' method='POST'>
              <input style="width:400px;height:80px;" name='gozde' type= 'text'>
              <input type = 'submit'></form>"""

if __name__ == "__main__":
    app.run()