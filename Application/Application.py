from flask import Flask,request
import nltk
import os,sys
import urllib2
import re
import work
import Fetcher

app = Flask(__name__)



#model = work.loadModel_two("our.model")


@app.route("/",methods=['GET','POST'])
def hello():
	if request.method == 'POST':
		question = request.form.get('gozde')
		result = work.extractWithStanfordNer(question)
		resultCon = reduce(lambda x,y:x+"<br>"+y,result)
		return str(resultCon)

	return """<img style="width:400px;height:400px;margin-top:10%;margin-left:40%" src='https://upload.wikimedia.org/wikipedia/commons/b/b0/PHAROS2006.jpg' >
	           <form style="margin-left:36%;margin-top:12%" action='/' method='POST'>
              <input style="width:600px;height:100px; font-size:40px" name='gozde' type= 'text'>
              <input type = 'submit'></form>"""

if __name__ == "__main__":
    app.run()



