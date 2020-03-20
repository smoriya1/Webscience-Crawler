from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx

#Initialises the db client
mongo_client = MongoClient()
db = mongo_client.twitterdb
line = db.tweets_RESTapi

#Stores the user, user mentions and hashtag info into a list
df = pd.DataFrame()
df2 = pd.DataFrame()
usr = []
menUsr = []
usr2 = []
hashtags = []
for doc in line.find({}):
    if (doc["entities"]["user_mentions"]):
        temp = []
        for i in range(len(doc["entities"]["user_mentions"])):
            temp.append(doc["entities"]["user_mentions"][i]["screen_name"])
        usr.append(doc['user']['screen_name'])
        menUsr.append(temp)
    if (doc["entities"]["hashtags"]):
        temp = []
        for i in range(len(doc["entities"]["hashtags"])):
            temp.append(doc["entities"]["hashtags"][i]["text"])
        hashtags.append(temp)
        usr2.append(doc['user']['screen_name'])

#Adds the user and its corresponding user mentions to a dataframe
df['user'] = usr[0:10000]
df['mentioned_user'] = menUsr[0:10000]

#Adds the user and its corresponding hashtag info to a dataframe
df2['user'] = usr2[0:2000]
df2['hashtags'] = hashtags[0:2000]

#Initialises the user interaction graph and creates the edges
G = nx.Graph()
for r in df.iterrows():
    for user in r[1]['mentioned_user']:
        G.add_edge(r[1]['user'], user)

#Finds the largest connected subgraph
graphs = []
for c in nx.connected_components(G):
    graphs.append(G.subgraph(c))
largest = max(graphs, key=len)

#Comptues the eigenvector centrality values for the colouring
ecent = nx.eigenvector_centrality(largest)
ecent_color = [value for key, value in ecent.items()]

#Generates the graph
nx.draw(largest, node_color=ecent_color, layout=nx.spring_layout(largest), node_size=1)
plt.savefig('Interaction1.png')

#Initialises the hashtag interaction graph and creates the edges
B = nx.Graph()
for r in df2.iterrows():
    for hashtag in r[1]['hashtags']:
        B.add_edge(r[1]['user'],hashtag)

#Finds the largest connected subgraph
graphs = []
for c in nx.connected_components(B):
    graphs.append(B.subgraph(c))
largest = max(graphs, key=len)

#Generates the graph
G2 = nx.bipartite.weighted_projected_graph(largest, nodes = largest.nodes())
nx.draw(G2, with_labels=True, node_size=2, font_size=5, k=8, iterations=20)
plt.savefig('Hashtag1.png')
