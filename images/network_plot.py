"""
The python script to generate the network plot
Use list that contains the hashtags data in the time window that you want to plot  
"""

import networkx as nx
from itertools import combinations, permutations
import matplotlib.pyplot as plt


def edges(lst):
    """
    Fucntion that return edges between all nodes

    Parameters
    -----------
    lst: all the hashtags in the time window that you want to plot
    
    Returns
    --------
    list of edges of all hashtags (nodes)

    """
    
    att = [item for sublist in lst for item in sublist]


    pointer = []
    for i in lst:
        for item in combinations(i,2):
            pointer.append([item[0], item[1]])
            
    pointer = [x for x in pointer if len(x)>1]
    
    return pointer


network = edges(ref)   # ref are the hashtags from the randon time window in tweets.txt

G=nx.Graph()
G.add_edges_from(network)


# node size based on the its edges
def degree_size(G):
    g_size=[float(len(G.edges(v))) for v in G]
    return g_size

G_size = degree_size(G)


# node color base on the number of nodes that are in the same group (reachable)
node_color = []
for word in G.nodes():
    tw = []
    for reachable_node in nx.dfs_postorder_nodes(G,source=word):
        tw.append(reachable_node)
    node_color.append(len(tw)) 



fig = plt.figure(figsize=(50,50))
vpg = nx.spring_layout(G,scale=1000, iterations=10)
nx.draw_networkx(G,pos=vpg, node_size= np.array(G_size)*800, cmap=plt.cm.YlGnBu, 
                 vmin=min(node_color), vmax=max(node_color)+5, node_color=node_color, 
                 with_labels=True, font_size=12)


limits=plt.axis('off')
plt.savefig("network_plot.png")
plt.show()