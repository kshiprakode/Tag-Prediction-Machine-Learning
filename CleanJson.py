# Step 1 is Tag Prediction - Data Purification
#Script that reads the JSON on the StackOverflow posts and purfies the questions to give us tokens of the key words

import json
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from bs4 import BeautifulSoup
import string

with open("PostsSmall.json") as json_file:
    json_data = json.load(json_file)
    length =  len(json_data["posts"]["row"])
    for i in range(1,length):
    	
    	print i

    	o = json_data["posts"]["row"][i]["@Body"]
    	o = o.replace('&lt;','<')
    	o = o.replace('&gt;','>')
    	
    	# Removing HTML tags using the Beautiful Soup Library
    	soup = BeautifulSoup(o, 'html.parser')
    	o = soup.get_text()
    	o = o.lower()
    	o = o.replace('\u','')
    	
    	# Removing StopWords using the python string.punctuations
    	exclude = set(string.punctuation)
    	o = ''.join(ch for ch in o if ch not in exclude)
    	
    	# Removing StopWords using the nltk library
    	stop = set(stopwords.words('english'))
    	o = ' '.join([word for word in o.split() if word not in (stopwords.words('english'))])
    	print o.encode("utf-8")


