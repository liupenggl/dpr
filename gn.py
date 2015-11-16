#!/usr/bin/env python
import networkx as nx
import math
import csv
import random as rand
import sys

#this method just reads the graph structure from the file
def buildG(G,path=None):
    #construct the weighted version of the contact graph from cgraph.dat file
    #reader = csv.reader(open("./VS/graph-751.txt"), delimiter=delimiter_)
    G.clear()
    import shlex
    try:
        f=open(path,'r')
    except :
        print "readfile_net error" 

   
    for line in f:
        if line.lower().startswith("*edges"):
            break


    for line in f:  
        temp=line.split()
        if len(temp)<2:
            continue
        u,v=temp[0:2]
        G.add_edge(u,v)
        #for (u,v) in nx.edges(g): # clean multiple edge
            #if (v,u) in nx.edges(g):
                #g.clear (v,u) 
    f.close()
    return G

#keep removing edges from Graph until one of the connected components of Graph splits into two
#compute the edge betweenness
def CmtyGirvanNewmanStep(G):
    #print "call CmtyGirvanNewmanStep"
    init_ncomp = nx.number_connected_components(G)    #no of components
    ncomp = init_ncomp
    while ncomp <= init_ncomp:
        bw = nx.edge_betweenness_centrality(G)    #edge betweenness for G
        #find the edge with max centrality
        max_ = max(bw.values())
        #find the edge with the highest centrality and remove all of them if there is more than one!
        for k, v in bw.iteritems():
            if float(v) == max_:
                G.remove_edge(k[0],k[1])    #remove the central edge
        ncomp = nx.number_connected_components(G)    #recalculate the no of components

#compute the modularity of current split
def _GirvanNewmanGetModularity(G, deg_, m_):
    New_A = nx.adj_matrix(G)
    New_deg = {}
    New_deg = UpdateDeg(New_A, G.nodes())
    #Let's compute the Q
    comps = nx.connected_components(G)    #list of components    
    #print 'no of comp: %d' % len(comps)
    Mod = 0    #Modularity of a given partitionning
    for c in comps:
        EWC = 0    #no of edges within a community
        RE = 0    #no of random edges
        for u in c:
            EWC += New_deg[u]
            RE += deg_[u]        #count the probability of a random edge
        Mod += ( float(EWC) - float(RE*RE)/float(2*m_) )
    Mod = Mod/float(2*m_)
    #print "Modularity: %f" % Mod
    return Mod

def UpdateDeg(A, nodes):
    deg_dict = {}
    n = len(nodes)  #len(A) ---> some ppl get issues when trying len() on sparse matrixes!
    B = A.sum(axis = 1)
    for i in range(n):
        deg_dict[nodes[i]] = B[i, 0]
    #print deg_dict
    return deg_dict

#run GirvanNewman algorithm and find the best community split by maximizing modularity measure
def runGirvanNewman(G, Orig_deg, m_):
    #let's find the best split of the graph    
    BestQ = 0.0
    Q = 0.0
    Bestcomps = list(nx.connected_components(G))
    while True:    
        CmtyGirvanNewmanStep(G)
        Q = _GirvanNewmanGetModularity(G, Orig_deg, m_);
        #print "current modularity: %f" % Q
        if Q > BestQ:
            BestQ = Q
            Bestcomps = list(nx.connected_components(G))    #Best Split
            #print "comps:" 
            #print Bestcomps
        if G.number_of_edges() == 0:
            break
    """
    if BestQ > 0.0:
        print "Best Q: %f" % BestQ
        print Bestcomps
    else:
        print "Best Q: %f" % BestQ
    """
    return Bestcomps
def main(argv):
    
    graph_fn="./data/7.txt"
    G = nx.Graph()  #let's create the graph first
    buildG(G, graph_fn)

    print G.nodes()
    print G.number_of_nodes()
    
    n = G.number_of_nodes()    #|V|
    A = nx.adj_matrix(G)    #adjacenct matrix

    m_ = 0.0    #the weighted version for number of edges
    for i in range(0,n):
        for j in range(0,n):
            m_ += A[i,j]
    m_ = m_/2.0
    print "m: %f" % m_

    #calculate the weighted degree for each node
    Orig_deg = {}
    Orig_deg = UpdateDeg(A, G.nodes())

    #run Newman alg
    runGirvanNewman(G, Orig_deg, m_)

if __name__ == "__main__":
    exit(main(sys.argv))
