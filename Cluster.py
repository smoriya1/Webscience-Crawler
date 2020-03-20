from pymongo import MongoClient
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

#Initialising the DB
mongo_client = MongoClient()
db = mongo_client.twitterdb
line = db.tweets_RESTapi

#Get the twitter text from the DB, strip off the unwanted portions, and append to list
text = []
for doc in line.find({}):
    if 'full_text' in doc:
        txt = doc['full_text']
        content = re.sub(r"http\S+", "", txt)
        content = content.replace('RT ', ' ').replace('&amp;', 'and')
        content = re.sub('[^A-Za-z0-9#@]+', ' ', content)
        content = content.lower()
        text.append(content)

#Split each word by its tokens
all_text = ' '.join(text)
tokens = (TweetTokenizer(preserve_case=False,
                        reduce_len=True,
                        strip_handles=False)
          .tokenize(all_text))

#Configuring the stop words which will be removed from the text list
stop_words = set(stopwords.words('english'))
stop_words.add('u')
stop_words.add('like')
stop_words.add('ur')

#Removing the token words from the list
filtered_sentence = []
for w in tokens:
    if w not in stop_words:
        filtered_sentence.append(w)

#The vectoriser for the K-means algorithm
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(filtered_sentence)
words = vectorizer.get_feature_names()

#Finding out the optimal cluster number by generating an ekbow graph
'''wcss = []
for i in range(1,12):
    kmeans = KMeans(n_clusters=i,init='k-means++',max_iter=300,n_init=10,random_state=0)
    kmeans.fit(x)
    wcss.append(kmeans.inertia_)
plt.plot(range(1,12),wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.savefig('elbow.png')'''

#Generating the algorithm by using 2 clusters
kmeans = KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=300,
    n_clusters=2, n_init=20, n_jobs=-1, precompute_distances='auto', tol=0.0001, verbose=0)
kmeans.fit(X)

#Generating the top 25 entities in the 2 clusters
common_words = kmeans.cluster_centers_.argsort()[:,-1:-25:-1]
for num, centroid in enumerate(common_words):
    print(str(num) + ' : ' + ', '.join(words[word] for word in centroid))

#Plotting the center of each clusters
centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
plt.savefig('Scatter Centres.png')
