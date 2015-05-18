# Import your cleaned network information into python to perform some network analysis

# Part 1) Calculate Page Rank
import csv
from collections import defaultdict

pairlist=[]
connections=defaultdict(list)
userset=set()

with open('linkedIn_clean.csv', 'rb') as csvfile:
    allrows = csv.reader(csvfile, delimiter=',')
    for row in allrows:
#        if ((row[0]=='your_name') | (row[1]=='your_name')): continue   # exclude yourself ?
        pairlist.append((row[0], row[1]))
        connections[row[0]].append(row[1])
        connections[row[1]].append(row[0])
        userset.add(row[0])
        userset.add(row[1])
        
pagerank=defaultdict(lambda:1./len(userset))

for iteration in xrange(0, 30):
    newpagerank=defaultdict(lambda:0.)
    for user in userset:
        for connection in connections[user]:
            newpagerank[user] += pagerank[connection]/len(connections[connection])
    pagerank = newpagerank


prs = sorted(pagerank.iteritems(), reverse=True, key=lambda (k,v): v)
# display the pagerank
print prs[:10]
print

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import math

from matplotlib import rcParams
import matplotlib.cm as cm
import matplotlib as mpl

#colorbrewer2 Dark2 qualitative color table
dark2_colors = [(0.10588235294117647, 0.6196078431372549, 0.4666666666666667),
                (0.8509803921568627, 0.37254901960784315, 0.00784313725490196),
                (0.4588235294117647, 0.4392156862745098, 0.7019607843137254),
                (0.9058823529411765, 0.1607843137254902, 0.5411764705882353),
                (0.4, 0.6509803921568628, 0.11764705882352941),
                (0.9019607843137255, 0.6705882352941176, 0.00784313725490196),
                (0.6509803921568628, 0.4627450980392157, 0.11372549019607843)]

rcParams['figure.figsize'] = (10, 6)
rcParams['figure.dpi'] = 150
rcParams['axes.color_cycle'] = dark2_colors
rcParams['lines.linewidth'] = 2
rcParams['axes.facecolor'] = 'white'
rcParams['font.size'] = 14
rcParams['patch.edgecolor'] = 'white'
rcParams['patch.facecolor'] = dark2_colors[0]
rcParams['font.family'] = 'StixGeneral'


def remove_border(axes=None, top=False, right=False, left=True, bottom=True):
    """
    Minimize chartjunk by stripping out unnecesasry plot borders and axis ticks
    The top/right/left/bottom keywords toggle whether the corresponding plot border is drawn
    """
    ax = axes or plt.gca()
    ax.spines['top'].set_visible(top)
    ax.spines['right'].set_visible(right)
    ax.spines['left'].set_visible(left)
    ax.spines['bottom'].set_visible(bottom)
    
    #turn off all ticks
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticks_position('none')
    
    #now re-enable visibles
    if top:
        ax.xaxis.tick_top()
    if bottom:
        ax.xaxis.tick_bottom()
    if left:
        ax.yaxis.tick_left()
    if right:
        ax.yaxis.tick_right()

g = nx.Graph()
plt.figure()
remove_me = False

for user in userset:
    if remove_me & (user=='your_name'): continue
    g.add_node(user)
 
for user in userset:   
    if remove_me & (user=='your_name'): continue
    nconnec = 0
    for connection in connections[user]:
        if remove_me & (connection=='your_name'): continue
        g.add_edge(user, connection, weight = 1)
        nconnec+=1
    if remove_me & (nconnec==0):
        g.remove_node(user)
    
        
pagerank_nx = nx.pagerank_scipy(g)        
        
color = [(min(pagerank_nx[n]*30.,1),min(pagerank_nx[n]*30.,1), min(pagerank_nx[n]*30.,1)) for n in pagerank_nx]
pos = nx.spring_layout(g,  iterations=100)
nx.draw_networkx_edges(g, pos, width=1, alpha=0.4)
nx.draw_networkx_nodes(g, pos, node_color=color, node_size=100, alpha=1, linewidths =0.5)

#plt.show()
plt.savefig('network.png', format='png')

# Checks whether we have the similar, pageranks
sorted_pr = sorted(pagerank_nx.iteritems(), reverse=True, key=lambda (k,v): v)
print sorted_pr[:10]
print


# Part 2) Output a few stats about your network:
f = open(r"networkStats.txt", "w")

# your number of connection
f.write('my degree is: ' + str(g.degree('your_name')) + '\n')

# diameter = maximum nb of edges between 2 nodes = always 2 in this case
f.write('the graph diameter is: ' + str(nx.diameter(g)) + '\n')

# the center of your network is
f.write('the center is: ' + str(nx.center(g)) + '\n')

# the number of clique communities of 5 nodes or more in your network
f.write('there are ' + str(len(list(nx.k_clique_communities(g, 5)))) + 'clique communities\n')

# the most influential node in your network
f.write('degree: ' +  str(g.degree(sorted_pr[2])) + '\n')

# the shortest path between 2 nodes in your network
f.write('shortest path between Friend A and Friend B' + str(nx.shortest_path(g,source='friend_A',target='friend_B')) + '\n')

f.close()