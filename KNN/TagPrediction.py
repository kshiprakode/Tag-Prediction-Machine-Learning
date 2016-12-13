import json
import string
from pprint import pprint
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from bs4 import BeautifulSoup
import string
import numpy
import math

def cleanPost(post):
	
	# Removes encoded html tags
	post = post.replace('&lt;','<')
	post = post.replace('&gt;','>')
	post = post.encode("utf-8")

	# Removes HTML tags
	soup = BeautifulSoup(post, 'html.parser')
	post = soup.get_text()

	# To lower case
	post = post.lower()

	# Removes punctuation
	exclude = set(string.punctuation)
	post = ''.join(ch for ch in post if ch not in exclude)

	# Removes stop words
	stop = set(stopwords.words('english'))
	post = ' '.join([word for word in post.split() if word not in (stopwords.words('english'))])

	post = post.encode("utf-8").split()

	# Takes the list and removes duplicates
	sorted_list = list(set(post))

	# Sorts the list
	sorted_list.sort()
	
	return sorted_list

def distance(trainScore,testScore,length):
	dist = 0
	for x in range(length):
		dist += pow((trainScore[x] - testScore[x]),2)
	return math.sqrt(dist)

# cleaning the entered post
testPost =  "&lt;p&gt;In a standard algorithms course we are taught that &lt;strong&gt;quicksort&lt;/strong&gt; is $O(n \log n)$ on average and $O(n^2)$ in the worst case. At the same time, other sorting algorithms are studied which are $O(n \log n)$ in the worst case (like &lt;strong&gt;mergesort&lt;/strong&gt; and &lt;strong&gt;heapsort&lt;/strong&gt;), and even linear time in the best case (like &lt;strong&gt;bubblesort&lt;/strong&gt;) but with some additional needs of memory.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;After a quick glance at &lt;a href=&quot;http://en.wikipedia.org/wiki/Sorting_algorithm#Comparison_of_algorithms&quot;&gt;some more running times&lt;/a&gt; it is natural to say that quicksort &lt;strong&gt;should not&lt;/strong&gt; be as efficient as others.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;Also, consider that students learn in basic programming courses that recursion is not really good in general because it could use too much memory, etc. Therefore (and even though this is not a real argument), this gives the idea that quicksort might not be really good because it is a recursive algorithm.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;&lt;strong&gt;Why, then, does quicksort outperform other sorting algorithms in practice?&lt;/strong&gt; Does it have to do with the structure of &lt;em&gt;real-world data&lt;/em&gt;? Does it have to do with the way memory works in computers? I know that some memories are way faster than others, but I don't know if that's the real reason for this counter-intuitive performance (when compared to theoretical estimates).&lt;/p&gt;&#xA;&#xA;&lt;hr&gt;&#xA;&#xA;&lt;p&gt;&lt;strong&gt;Update 1:&lt;/strong&gt; a canonical answer is saying that the constants involved in the $O(n\log n)$ of the average case are smaller than the constants involved in other $O(n\log n)$ algorithms. However, I have yet to see a proper justification of this, with precise calculations instead of intuitive ideas only.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;In any case, it seems like the real difference occurs, as some answers suggest, at memory level, where implementations take advantage of the internal structure of computers, using, for example, that cache memory is faster than RAM. The discussion is already interesting, but I'd still like to see more detail with respect to memory-management, since it appears that &lt;em&gt;the&lt;/em&gt; answer has to do with it.&lt;/p&gt;&#xA;&#xA;&lt;hr&gt;&#xA;&#xA;&lt;p&gt;&lt;strong&gt;Update 2:&lt;/strong&gt; There are several web pages offering a comparison of sorting algorithms, some fancier than others (most notably &lt;a href=&quot;http://www.sorting-algorithms.com/&quot;&gt;sorting-algorithms.com&lt;/a&gt;). Other than presenting a nice visual aid, this approach does not answer my question.&lt;/p&gt;&#xA; Why is quicksort better than other sorting algorithms in practice?"

testPost =  cleanPost(testPost)
# print testPost

# Openning train data
with open('postsSmall.json') as data_file:    
    data = json.load(data_file)

# Number of train data found
size_json = len(data["posts"]["row"])

distances = [0]*size_json

for p in range(size_json):
	print "ID is - "
	print data["posts"]["row"][p]["@Id"]

	trainPost = cleanPost(data["posts"]["row"][p]["@Body"])
	trainTest = []
	trainTest.extend(testPost)
	trainTest.extend(trainPost)
	trainTest_list = list(set(trainTest))
	trainTest_list.sort()
	# print trainTest_list

	testScore = [0]*len(trainTest_list)
	for i in range(len(testPost)):
		if testPost[i] in trainTest_list:
			loc = trainTest_list.index(testPost[i])
			testScore[loc] = testScore[loc] + 1

	# print "Test Score"
	# print testScore		

	trainScore = [0]*len(trainTest_list)
	for i in range(len(trainPost)):
		if trainPost[i] in trainTest_list:
			loc = trainTest_list.index(trainPost[i])
			trainScore[loc] = trainScore[loc] + 1

	# print "Train Score"
	# print trainScore	

	dist = distance(trainScore,testScore,len(trainScore))	
	distances[p] = dist
train_loc = distances.index(min(distances))
print train_loc
print data["posts"]["row"][train_loc]["@Tags"]