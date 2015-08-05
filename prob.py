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

def bib():
    _lambda = 10.0
    x = np.arange(20)
    pl.figure(figsize=(10,4))
    for i, n in enumerate([100, 1000]):
        pl.subplot(121+i)
        y1 = stats.binom.pmf(x, n, _lambda/n)
        y2 = stats.poisson.pmf(x, _lambda)
        pl.plot(x, y1, label=u"binom", lw=2)
        pl.plot(x, y2, label=u"poisson", lw=2, color="red")
        pl.xlabel(u"娆℃暟")
        pl.ylabel(u"姒傜巼")
        pl.title("n=%d" % n)
        pl.legend()

    pl.subplots_adjust(0.1, 0.15, 0.95, 0.90, 0.2, 0.1)
    pl.show()

def bi(n=20,p=0.5):
    p = 1.0/400
    n=200
    x = np.arange(n)
    y = stats.binom.pmf(x,n,p)
    print y

    x1=[]
    y1=[]
    for each in x:
        if y[each]>0.001:
            x1.append(each)
            y1.append(y[each])

    pl.bar(x1, y1,width=0.4, align="center")
    
    pl.xlabel("Number")
    pl.ylabel("Probability")    
    pl.title("n={0} p={1}".format(n,p))

    pl.legend()
    pl.grid(True)
    pl.savefig("n={0} p={1}.png".format(n,p))
    pl.show()

def d():
    x=np.linspace(0,10,100)
    y=np.sin(x)
    plt.figure(figsize=(8,4))
    plt.plot(x,y,label="sin(x)",color="red",lw=1)
    plt.ylim(-1.2,2)
    plt.legend()
    plt.show()

def f():
    plt.figure(1)
    plt.subplot(221,axisbg='r')
    plt.subplot(222,axisbg='g')
    plt.subplot(211,axisbg='b')
    plt.show()
def binomial_con(z=1,n1=10,n2=20,p1=0.1,p2=0.1):
    """z 是节点得度， n1是

    """
    sum=0.0
    t=0
    while t<=n1:
        sum=sum+stats.binom.pmf(t,n1,p1)*stats.binom.pmf(z-t,n2,p2)
        t+=1

    return sum

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
#def binomial_con_di(z,node,g,m):
#    """删除m条边 X，然后添加m条边Y，z 是节点的度，node节点的标签，g图
#    """
    
#    n1=m if m<len(g[node]) else len(g[node])#delete at most min(m,node degree) edges, because a node has only len(g[node]) edges
#    p1=1.0*m/len(g.edges())# n1 trails whit deleting probality p1
    
#    n2=m if m<(len(g.edges())-1-len(g[node])) else (len(g.edges())-1-len(g[node]))#leave enough node for edges adding
#    p2=1.0*m/(len(g.nodes())*(len(g.nodes())-1)/2)

#    di=len(g[node])
#    sum=0.0
#    t=0
#    while t<=n1:
#        if z-di+t>=0 and z-di+t<=n2:
#            sum=sum+stats.binom.pmf(t,n1,p1)*stats.binom.pmf(z-di+t,n2,p2)

#        t+=1
#    return sum
def test_bi(g=None,label=None):
    n1=20
    p1 = 0.1
    
    n2=40
    p2=0.3

    z=n1+n2
    y=[]
    for each in range(z):
        y.append(binomial_con(each,n1,n2,p1,p2))
 
    print sum(y)
    x1=[]
    y1=[]
    for each in range(z):
        if y[each]>0.001:
            x1.append(each)
            y1.append(y[each])

    pl.bar(x1, y1,width=0.4, align="center")
    
    pl.xlabel("Number")
    pl.ylabel("Probability")    
 #   pl.title("n={0} p={1}".format(n,p))

    pl.legend()
    pl.grid(True)
 #   pl.savefig("n={0} p={1}.png".format(n,p))
    pl.show()
    
def test_bi_di(g=None,label=None):
    g=nx.Graph()
    #filepath=r'D:\data\prandom\polbooks.txt'
    #filepath=r'D:\data\prandom\graph3.txt'
    filepath=r'D:\program\code\hybrid\data\graph.txt'
    read_file_txt(g,path=filepath)
    m=4
    node='6'
    z=len(g[node])+m

    y=[]
    for each in range(z):
        y.append(binomial_con_di(each,node,g,m))


    print sum(y)
    x1=[]
    y1=[]
    for each in range(z):
        if y[each]>0.001:
            x1.append(each)
            y1.append(y[each])

    pl.bar(x1, y1,width=0.4, align="center")
    
    pl.xlabel("Number")
    pl.ylabel("Probability")    
 #   pl.title("n={0} p={1}".format(n,p))

    pl.legend()
    pl.grid(True)
 #   pl.savefig("n={0} p={1}.png".format(n,p))
    pl.show()
def test_bi_g(g=None,label=None):
    g=nx.Graph()
    filepath=r'D:\data\prandom\polbooks.txt'
    read_file_txt(g,path=filepath)
    m=10
    node=g.nodes()

    y=[]
    for each in node:
        y.append(binomial_con_di(len(g[each]),each,g,m))

    node=[string.atoi(x) for x in node]
    print node
    plt.figure(figsize=(16,4))
    plt.scatter(node,y)
    
    plt.xticks(range(0,120,10))
    plt.xlim(0,104)
    plt.grid(True)


    plt.show()
def km_random(g,k=5,m=3,start=None):
    """ k nodes of breath first sequence; m add and del number."""
    if start==None:
        start=g.nodes().pop()
    bfList=list(nx.bfs_edges(g,start))
    bfList.reverse()
    bfList.append((start,start))
    tempk=[]
    try:
        while bfList:
            for each in range(k):
                tempk.append(bfList.pop()[1])
            
            tg=nx.subgraph(g,tempk)
            e=del_edge(tg,m)
            g.remove_edges_from(e)

            tg=nx.subgraph(g,tempk)
            e=add_edge(tg,m)
            g.add_edges_from(e)

            tempk=[]

    except IndexError:
        print "pop finishing"

    #for each in bfList:
    #    print each

def p_kann(g,k):
    """le 包含节减少度1就达到k匿名，gr包含节点增加度1就到k匿名，rr包含节点不满足k匿名且不在前两种情况中。"""
    if not g.nodes():
        print "In hrandom(g,k) g is empty!"
        return 0
  
    le=[]
    gr=[]
    rr=[]
 
    d=g.degree().items()
    dh=nx.degree_histogram(g)

    for each in d:
        if dh[each[1]]<k:
            if each[1]!=0 and dh[each[1]-1]>=k:
                le.append(each[0])
            elif  each[1]!=len(dh)-1 and dh[each[1]+1]>=k:
                gr.append(each[0])
            else:
                rr.append(each[0])

    return le,gr,rr
def p_kannd(g,le,gr,rr):
    """对le中的节点度减少1，gr中的节点度加1，没办法处理的放在rr中"""
    if len(le)>1:
        i=0;
        bflag=False
        while i<len(le)-1:
            j=i+1
            while j<len(le):
                if le[j] in g.neighbors(le[i]):
                    g.remove_edge(le[i],le[j])
                    print (le[i],le[j])
                    del le[i]
                    del le[j-1]
                    bflag=True
                    break
                j+=1
                bflage=False
            if not bflag:
                i+=1
            else:
                bflag=False

    if len(gr)>1:
        i=0;
        bflag=False
        while i<len(gr)-1:
            j=i+1
            while j<len(gr):
                if gr[j] not in g.neighbors(gr[i]):
                    g.add_edge(gr[i],gr[j])
                    print (gr[i],gr[j])
                    del gr[i]
                    del gr[j-1]
                    bflag=True
                    break
                j+=1
                bflage=False
            if not bflag:
                i+=1
            else:
                bflag=False
    rr=rr+le+gr
    return rr

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
 #   x1=[]
 #   y1=[]
 #   for each in range(len(g)):
 #       if y[each]>0.001:
 #           x1.append(each)
 #           y1.append(y[each])

 #   pl.bar(x1, y1,width=0.4, align="center")
    
 #   pl.xlabel("Number")
 #   pl.ylabel("Probability")    
 ##   pl.title("n={0} p={1}".format(n,p))

 #   pl.legend()
 #   pl.grid(True)
 ##   pl.savefig("n={0} p={1}.png".format(n,p))
 #   pl.show()

if __name__=="__main__":
    print  "in prob.py __main__"
    g=nx.Graph()
    #filepath=r'D:\data\prandom\polbooks.txt'
    filepath=r'D:\data\prandom\graph.txt'
    read_file_txt(g,path=filepath)

    #km_random(g)

    #u,v,w=p_kann(g,9)
    #print u
    #print v
    #print w

    #w=p_kannd(g,u,v,w)
    #print w

    #e=del_edge(g,3)
    #g.remove_edges_from(e)
    #print e
    #e=add_edge(g,3)
    #print e
    #g.add_edges_from(e)

    #km_random(g,5,2,'3')

    #DrawGraph(g)
    
    #km_random(g)

    #test_bi_di()
    test_p()
    #test_bi_g()
