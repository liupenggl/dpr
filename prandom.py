#-*- coding:utf-8 -*-
from scipy import stats
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
from gfile import *
import networkx as nx
import random
import string 
def del_edge(g,m):
    """remove m edges in g at random"""
    if len(g.edges())>=m:
            medge=random.sample(g.edges(),m)
            return medge
    else:
        print "not enough edges to remove, please check m"
 
def add_edge(g,m):
    compl=nx.complement(g)
    if len(compl.edges())>=m:
        aedge=random.sample(compl.edges(),m)
        return aedge
    else:
        print "not enough nodes to add m edges, please check m"

def binomial_con_di(z,node,g,m):
    """删除m条边 X，然后添加m条边Y，z 是节点的度，node节点的标签，g图
    """
    
    n1=m if m<len(g[node]) else len(g[node])#delete at most min(m,node degree) edges, because a node has only len(g[node]) edges
    p1=1.0*m/len(g.edges())# n1 trails whit deleting probality p1
    
    n2=m if m<(len(g.edges())-1-len(g[node])) else (len(g.edges())-1-len(g[node]))#leave enough node for edges adding
    p2=1.0*m/(len(g.nodes())*(len(g.nodes())-1)/2)

    di=len(g[node])
    sum=0.0
    t=0
    while t<=n1:
        if z-di+t>=0 and z-di+t<=n2:
            sum=sum+stats.binom.pmf(t,n1,p1)*stats.binom.pmf(z-di+t,n2,p2)#adding z-di edges

        t+=1
    return sum

def prand():
    g=nx.Graph()
    filepath=r'D:\program\code\hybrid\data\graph.txt'
    read_file_txt(g,path=filepath)
    bflist=[]

    start='3'
    bflist.append(start)
    for each in nx.bfs_edges(g,start):
        print each
        bflist.append(each[1])

    print bflist

def bflist(g,source):
    bfli=[]
    bfli.append(source)
    for each in nx.bfs_edges(g,source):
        #print each
        bfli.append(each[1])
    #print bflist
    return bfli

def csgraph(bflist,s,node):#calcualte the sublist
    length=len(bflist)
    loc=bflist.index(node)
    if length<2*s:
        return bflist

    a=loc/s#length=ax+b
    b=loc%s
    
    sen=a*s

    if sen+s>length:
        return bflist[(a-1)*s:length]
    elif sen+2*s>length:
        return bflist[a*s:length]
    else:
        return bflist[a*s:(a+1)*s]

def vrisk(node,g,bfli,s,m):#node 
    
    subli=csgraph(bfli,s,node)
    subg=g.subgraph(subli)

    ddiff=len(g[node])-len(subg[node])
    pr=binomial_con_di(len(subg[node])-ddiff,node,subg,m)
    print pr

    prr=1-pr
    f=open("temp.txt",'w')
    
    for each in g:
        subli=[]
        subli=csgraph(bfli,s,each)     
        subg=g.subgraph(subli)
        ddiff=len(g[each])-len(subg[each])
        f.write('{0:>2} {1} {2:.2} {3}'.format(each,' : ',binomial_con_di(len(g[node])-ddiff,each,subg,m),'\n'))
        prr=prr+binomial_con_di(len(g[node])-ddiff,each,subg,m)
    
    print pr*(1.0/prr)
    f.close()


def test_p():
    g=nx.Graph()
    #filepath=r'D:\data\prandom\polbooks.txt'
    #filepath=r'D:\data\prandom\graph3.txt'
    filepath=r'D:\program\code\hybrid\data\graph.txt'
    read_file_txt(g,path=filepath)
    m=2
    node='3'
    z=len(g[node])

    y=[]
    for each in g.nodes():
        y.append((each,binomial_con_di(z,each,g,m)))




    for x in y:
        print x
    DrawGraph(g)


if __name__=="__main__": 
    g=nx.Graph()
    ##filepath=r'D:\data\prandom\polbooks.txt'
    ##filepath=r'D:\data\prandom\graph3.txt'
    filepath=r'D:\program\code\hybrid\data\graph.txt'
    read_file_txt(g,path=filepath)
    #li=bflist(g,'3')
    #s=g.subgraph(li[0:5])

    li=['3','6','7','9','8','4']

    DrawGraph(g)
    #print li
    #ls=range(10)
    #for each in ls:
    #    rr=csgraph(ls,5,each)
    #    print each,"xxx",rr

    #rr=csgraph(ls,3,2)
    #s=5
    #m=2
    #node='2'
    #bfli=bflist(g,node)

    #print bfli

    #vrisk(node,g,bfli,s,m)

    #print rr
   
