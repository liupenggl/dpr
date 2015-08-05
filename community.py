import networkx as nx
import matplotlib.pyplot as plt

from collections import defaultdict
import networkx as nx
import numpy
from scipy.cluster import hierarchy
from scipy.spatial import distance
 
 


def create_hc(G, t=1.0):
    """
    Creates hierarchical cluster of graph G from distance matrix
    Maksim Tsvetovat ->> Generalized HC pre- and post-processing to work on labelled graphs and return labelled clusters
    The threshold value is now parameterized; useful range should be determined experimentally with each dataset
    """

    """Modified from code by Drew Conway"""
    
    ## Create a shortest-path distance matrix, while preserving node labels
    labels=G.nodes()    
    path_length=nx.all_pairs_shortest_path_length(G)
    distances=numpy.zeros((len(G),len(G))) 
    i=0   
    for u,p in path_length.items():
        j=0
        for v,d in p.items():
            distances[i][j]=d
            distances[j][i]=d
            if i==j: distances[i][j]=0
            j+=1
        i+=1
    
    # Create hierarchical cluster
    Y=distance.squareform(distances)
    Z=hierarchy.complete(Y)  # Creates HC using farthest point linkage
    # This partition selection is arbitrary, for illustrive purposes
    membership=list(hierarchy.fcluster(Z,t=t))
    # Create collection of lists for blockmodel
    partition=defaultdict(list)
    for n,p in zip(list(range(len(G))),membership):
        partition[p].append(labels[n])
    return list(partition.values())

def pc():
    import random
    Y=[random.randint(1,30) for x in range(10) ]

   

    print distance.squareform(Y)
    Z=hierarchy.complete(Y)  # Creates HC using farthest point linkage
    # This partition selection is arbitrary, for illustrive purposes
    print Z
    membership=list(hierarchy.fcluster(Z,1))
    # Create collection of lists for blockmodel
    print 'membership',membership
    partition=defaultdict(list)
    for n,p in zip(list(range(10)),membership):
        partition[p].append(n)
    return list(partition.values())


if __name__=='__main__':

    g=nx.generators.small.krackhardt_kite_graph()
    nx.draw(g,with_labels = True,pos=nx.spring_layout(g))
    
    #r=nx.find_cliques_recursive(g)  
    r=create_hc(g)
    print r
    #print pc()
    #plt.show()
 