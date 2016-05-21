from flask import Flask,request
import nltk
import os,sys
import urllib2
import re
import work
import Fetcher
from time import strftime
import QuestionClassification as Qc

app = Flask(__name__)



#model = work.loadModel_two("our.model")


@app.route("/",methods=['GET','POST'])
def hello():
	if request.method == 'POST':
		question = request.form.get('pageContent')
		result = work.extractWithStanfordNer(question)
		print "geldim 1"
		ectracted_result = result[0]
		imgUrl=  ""
		imgStrPrefBeg =  "<img style=\"max-width:600;max-height:600;\" src=\""
		imgStrPrefENd  =  "\"/>"
		if  result[1][0] != None and len(result[1])>0:
			for element in result[1]:
				imgUrl  += imgStrPrefBeg + element + imgStrPrefENd
		else:
			imgUrl = ""
		print "cokmuyorum burada"
		reelResult = ""
		for element in result[0]:
			print type(element)
			reelResult = reelResult+element+"<br>"
		print "geldim 2"	
			
		#result2 = work.findCorrectAnswer(result)
		#rrr = ""+result2[1:]
		#imageUrl = work.findImage(rrr)
                #resultCon = reduce(lambda x,y:x+"<br>"+y,result)
		return "<title>Unicorn</title><p style=\"font-size:45px;\">The answer is:"+ reelResult +"</p>" + "<br>" + imgUrl

	return """<html style=\" background:#DDDDDD\">
			 <title>Unicorn QA</title>
			 <body>
			
			 <script type="text/javascript" src="https://stiltsoft.com/blog/wp-content/demo/web-speech-api/textarea/jquery.min.js"></script>
             <script type="text/javascript" src="https://stiltsoft.com/blog/wp-content/demo/web-speech-api/textarea/textarea-helper.js"></script>
             <script type="text/javascript" src="https://stiltsoft.com/blog/wp-content/demo/web-speech-api/textarea/speech-recognizer.js"></script>

			 <img style="width:400px;height:400px;margin-top:10%;margin-left:40%" src='http://orig12.deviantart.net/ee73/f/2014/345/a/a/unicorn_by_amylovespenguins-d89hm7b.gif' >
	         <form style="margin-left:36%;margin-top:12%" action='/' method='POST'>
             <textarea  style="width:600px;height:100px; font-size:40px" name='pageContent' id="speech-page-content" type= 'text' ></textarea>
			 <div style="margin-left:%40;height:50px;width:40px;background-color:black" class="speech-content-mic speech-mic"/></div>
             <input value="Ask a question" type = 'submit'></form></html>"""

if __name__ == "__main__":
    app.run()



