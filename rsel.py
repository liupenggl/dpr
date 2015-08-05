


import networkx as nx
import matplotlib.pyplot as plt

def readFile(g,path="graph.txt"):
    f=open(path,'r')     
    for eachLine in f:
        if eachLine.find('*Edges')==-1:
            continue
        else:
            break
    for eachLine in f:
        if len(eachLine)<2:
            continue
        li=eachLine.strip().split()
        u=int(li[0])
        v=int(li[1])
        g.add_edge(u,v)
    return g
def sel2(g,k,ad,mi):
    '''g:graph; k:anonymous; ad:increasing one for k-anonmity; mi:decreaseing one;
       '''
    degreeH= nx.degree_histogram(g)
    print degreeH
    if(len(degreeH)<2):
        print "in sel() degreeH<2"
    for i in range(len(degreeH)-1):
        if(degreeH[i+1]>=k and degreeH[i]<k and degreeH[i]!=0):
           ad.append(i)
    for i  in range(len(degreeH)-1,0,-1):
        if(degreeH[i-1]>=k and degreeH[i]<k and degreeH[i]!=0):
            mi.append(i)
    return (ad,mi)
def sel3(g,k,ad,mi,su):
    '''g:graph; k:anonymous; ad:increasing one for k-anonmity; mi:decreaseing one;
       (node' sdegree,'''
  
    degreeH= nx.degree_histogram(g)
##    print degreeH
    if(len(degreeH)<2):
        print "in sel() degreeH<2"
    for i in range(len(degreeH)-1):
        if(degreeH[i+1]>=k and degreeH[i]<k and degreeH[i]!=0):
           ad.append(i)
    for i  in range(len(degreeH)-1,0,-1):
        if(degreeH[i-1]>=k and degreeH[i]<k and degreeH[i]!=0):
            mi.append(i)
    sad=set(ad)
    smi=set(mi)
    ssu=sad&smi

    for eachx in ssu:
        su.append(eachx)
        ad.remove(eachx)
        mi.remove(eachx)
        
    return (ad,mi,su)
def kAnonymit(g,k):
    """return the annonymized node label list"""
    rlist=list()
    degreeH=nx.degree_histogram(g)
##    print degreeH
    li=[[] for i in range(len(degreeH))]
    uNode=dict(zip(range(len(degreeH)),li))
 
    gd=g.degree()
    for e in gd:
        uNode[gd[e]].append(e)
    ad=list()
    mi=list()
    su=list()   
    sel3(g,3,ad,mi,su)
    nodeAd=list()
    nodeMi=list()
    nodeSu=list()     
    for i in ad:
        nodeAd=nodeAd+uNode[i]
        #nodeAd store the graph ID
    for i in mi:
        nodeMi=nodeMi+uNode[i]
    for i in su:
        nodeSu=nodeSu+uNode[i]

    print nodeAd,nodeMi,nodeSu


    i=0#Add edge 
    while i<len(nodeAd)-1:
        j=i+1
        while j<len(nodeAd):
            if not g.has_edge(nodeAd[i],nodeAd[j]):
                g.add_edge(nodeAd[i],nodeAd[j])
                rlist.append(nodeAd[i])
                rlist.append(nodeAd[j])
                nodeAd.pop(j)
                nodeAd.pop(i)
                i=i-1
                break
            else:
                j=j+1
        i=i+1
    print nodeAd
 
    i=0#delet edge
    while i<len(nodeMi)-1:
        j=i+1
        while j<len(nodeMi):
            if  g.has_edge(nodeMi[i],nodeMi[j]):
                g.remove_edge(nodeMi[i],nodeMi[j])
                rlist.append(nodeMi[i])
                rlist.append(nodeMi[j])
                nodeMi.pop(j)
                nodeMi.pop(i)
                i=i-1
                break
            else:
                j=j+1
        i=i+1
    print nodeMi
    
    i=0#Add edge 
    while i<len(nodeSu):
        j=0
        while j<len(nodeAd):
            if not g.has_edge(nodeSu[i],nodeAd[j]):
                g.add_edge(nodeSu[i],nodeAd[j])
                rlist.append(nodeSu[i])
                rlist.append(nodeAd[j])
                nodeAd.pop(j)
                nodeSu.pop(i)
                
                i=i-1
                break
            else:
                j=j+1
        i=i+1
    print nodeSu
    
    i=0#delet edge
    while i<len(nodeSu):
        j=0
        while j<len(nodeMi):
            if  g.has_edge(nodeSu[i],nodeMi[j]):
                g.remove_edge(nodeSu[i],nodeMi[j])
                rlist.append(nodeSu[i])
                rlist.append(nodeMi[j])
                nodeMi.pop(j)
                nodeSu.pop(i)
                i=i-1
                break
            else:
                j=j+1
        i=i+1
    print nodeSu
    return rlist

def sh(g):
    nx.draw(g,with_labels = True,pos=nx.spring_layout(g))
    plt.show()
    
def test(g):
    g.nodes()
    
def main():
    #print 'main running!'
    #g=nx.read_adjlist("te.adj",nodetype=int)
 
    #ad=list()
    #mi=list()
    #su=list()    
    ##print sel3(g,3,ad,mi,su)
    g=nx.Graph()
    g=nx.read_pajek("a.net")
 
    sh(g)
    nx.clustering(g)

  
   

if __name__=='__main__':
    main()
