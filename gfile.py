import os
import networkx as nx
import matplotlib.pyplot as plt

#-------------------------------------------------------------------------------
#  

def read_file_txt(g,path=None):
    #path="D:\\program\\code\\hybrid\\data\\graph.txt"
    """Read .txt file."""

    g.clear()
    import shlex
    
    try:
        f=open(path,'r')
    except:
        print "readFileTxt error" 

    try:
        for line in f:
            if line.lower().startswith("*edges"):
                break

            #temp=shlex.split(line)
            #if len(temp)>=2:
            #    v,l=temp[0:2]
            #    g.add_node(v,label=l) #For simplity,we do not use the node's attribute

        for line in f:
            temp=line.split()
            if len(temp)<2:
                continue
            u,v=temp[0:2]
            g.add_edge(u,v)
    except:
       print "Read file .txt content error!"
   
    f.close()
    return g

#-------------------------------------------------------------------------------
def read_file_net(g,path=None):
    #read .net file. Ues the function of nx.read_pajek()
    g.clear()
 
    try:
        mg=nx.read_pajek(path,encoding='ascii')
        #g=g.to_undirected()
        g=nx.Graph(mg)#Tanslate mg(MultiGraph) to g(Graph)

    except:
        print "readFileTxt error" 

    return g

def save_file_net(g,path=None):
    try:
        nx.write_pajek(g,path)
    except:
        print "Save file .net errro!"
    return True

#-------------------------------------------------------------------------------
def DrawGraph(g, pos=None, ax=None, hold=None, **kwds):
    """call nx.draw to display the data"""
    nx.draw(g,with_labels = True,pos=nx.spring_layout(g))
    plt.show()