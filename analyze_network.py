import csv
import json
from math import floor
import matplotlib.pyplot as plt
import networkx as nx
from networkx.readwrite import json_graph

G=nx.Graph()

f_user = open('data/yelp_academic_dataset_user.json', 'r')

nodeList = []
with open('processedData/user_w2500reviews.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(spamreader, None)  # skip the headers
    for row in spamreader:
        nodeList.append( row[0] )
print len(nodeList)
G.add_nodes_from(nodeList)
for line in f_user:
    data = json.loads(line)
    user_id = data['user_id']
    if user_id in nodeList:
    	G.node[user_id]['name'] = data['name']
    	G.node[user_id]['count'] = data['review_count']
    	G.node[user_id]['group'] = floor(data['average_stars'])
    	for friend in data['friends']:
    		if friend in nodeList:
    			if not G.has_edge(user_id, friend) and not G.has_edge(friend, user_id):
    				G.add_edge(user_id, friend)
    		
res = json_graph.node_link_data(G) # node-link format to serialize

print len(res['nodes'])
#res['links'] = [{'source': res['nodes'][link['source']]['id'],'target': res['nodes'][link['target']]['id']} for link in res['links']]
# write json
json.dump(res, open('processedData/force.json','w'))

#print nx.clustering(G)
#nx.draw_spring(G)
#plt.show()