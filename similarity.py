from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from nltk.corpus import stopwords


print ("Creating the bag of words...\n")


print ("English stopwords are:", stopwords.words("english"))

text1 = open("Oasis.txt").read().decode('iso-8859-9')#.decode('utf8')
text2 = open("Beatles.txt").read().decode('iso-8859-9')#.decode('utf8')

texts =[text1,text2]

def review_to_words(texts):
  for i in texts:
          letters_only = re.sub("[^a-zA-Z]", " ",i)
          #tokenization
          words = letters_only.lower().split()
          stops = set(stopwords.words("turkish"))
          meaningful_words = [w for w in words if not w in stops]

          result = ( " ".join( meaningful_words ))

          return result
#bagofwords
vectorizer = CountVectorizer()
bag_of_words = vectorizer.fit_transform(texts)

#bigram model
bigram_vectorizer = CountVectorizer(ngram_range=(2,2), token_pattern=r'\b\w+\b', min_df=1)
#bigram_vectorizer2= vectorizer.fit_transform().toarray()
analyze = bigram_vectorizer.build_analyzer()

ngram_vectorizer = CountVectorizer(ngram_range=(1,2), token_pattern=r'\b\w+\b', min_df=1)
analyze2= ngram_vectorizer.build_analyzer()


atemp = analyze(text1) [100].__str__().split(" ")

def cosine_sim(text1, text2):
    vectorizer1 = TfidfVectorizer(stopwords.words('english'))
    tfidf = vectorizer1.fit_transform([text1, text2])
    cosine = cosine_similarity(tfidf[-1], tfidf)
    return cosine


print( vectorizer.get_feature_names())
print((bag_of_words))
print ("vectorizer will get 'band' word:",vectorizer.vocabulary_.get("band"))
print (review_to_words(texts))
print(analyze(text1))
print(analyze2(text1))
print cosine_sim(atemp[0], atemp[1])
