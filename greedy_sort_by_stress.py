import networkx as nx
import matplotlib.pyplot as plt
import parse
import sys

assert len(sys.argv) >= 2
path = sys.argv[1]
print("input_file: ", path)
groups = sys.argv[2]
print("number of groups: ", groups)
G, stress_budget = parse.read_input_file(path)

stress_per_group = stress_budget/float(groups)
print("per group stress budget: ", stress_per_group )

#plt.subplot(121)
#nx.draw(G, with_labels=True, font_weight='bold')
#plt.show()

# print("happiness graph")
# pos = nx.spring_layout(G,19)#nx.circular_layout(G)
# nx.draw(G, pos, with_labels=True, cmap = plt.get_cmap('jet'))
# labels = nx.get_edge_attributes(G,'happiness')
# nx.draw_networkx_edge_labels(G,pos, edge_labels=labels)
# plt.show()

# print("stress graph")
# pos = nx.spring_layout(G,19)#nx.circular_layout(G)
# nx.draw(G, pos, with_labels=True, cmap = plt.get_cmap('jet'))
# labels = nx.get_edge_attributes(G,'stress')
# nx.draw_networkx_edge_labels(G,pos, edge_labels=labels)
# plt.show()

edges = []
for e in G.edges.data():
    print(e, e[2]["stress"] < stress_per_group)
    if e[2]["stress"] < stress_per_group:
        edges.append(e)


edges.sort(key = lambda x: x[2]["stress"])
print(edges)









