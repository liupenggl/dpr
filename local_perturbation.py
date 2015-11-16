#-*- coding:utf-8 -*-
import os
import networkx as nx
import matplotlib.pyplot as plt
import sys
import gn
from gn import *
import random
import itertools

def f():
    print 4
def modularity(G,newG,Bestcomps):
    m=G.size()
    nm=newG.size()
    q=nq=0
    for coms in Bestcomps:
        subG=G.subgraph(coms)
        l=subG.size()
        list_d=[x for y,x in G.degree_iter(coms)]
        d=0
        for k in list_d:
            d=d+k
        q=q+float(l)/m+(float(d)/(2*m))**2
        subN=newG.subgraph(coms)
        nl=subN.size()
        list_nd=[a for b,a in newG.degree_iter(coms)]
        nd=0
        for k in list_nd:
            nd=nd+k
        nq=nq+float(nl)/nm+(float(nd)/(2*nm))**2
    return q-nq
def disturb(g,cl):
    ng=g.copy()
    ng.remove_edges_from(ng.edges())
    for i in range(len(cl)-1):#连接簇之间不变的线
        j=i+1
        while j<len(cl):
            for x in itertools.product(cl[i],cl[j]):#簇之间两两（cl[i],cl[j]）笛卡尔积
                if g.has_edge(x[0],x[1]):
                    ng.add_edge(x[0],x[1])
            j+=1
    sub=[]
    for i in range(len(cl)):#打乱簇内线
        sub=g.subgraph(cl[i])
        edges=sub.edges()
        numOfe=sub.number_of_edges()
        sub.remove_edges_from(edges)
        setE=[]
        tupleE=[]
        for k in range(numOfe):#生成numOfe条线
            l=set(random.sample(cl[i],2))#随机生成cl[i]内两个数，并生成集合，因为集合无序，容易判断该两个数是否已经生成了
            while l in setE:
                l=set(random.sample(cl[i],2))
            setE.append(l)
        
        for item in setE:#集合变元组，用来添加边
            tupleE.append(tuple(item))
        ng.add_edges_from(tupleE)
    return ng
#global Bestcomps
def analyze(newComps,Bestcomps):
    j={}
    k=0
    for best in Bestcomps:
        best_val=0
        for c in newComps:
            val=len([val for val in best if val in c])
            if val>best_val:
                best_val=val
        j[k]=float(best_val)/float(len(best))
        k+=1
    return j
def readfile_net(G,path=None):

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
        
        if u!=v:#去除单节点
            
            G.add_edge(u,v)
    f.close()
##    return G
    
def togn(G):
    n = G.number_of_nodes()    #|V|
    A = nx.adj_matrix(G)    #adjacenct matrix

    m_ = 0.0    #the weighted version for number of edges
    for i in range(0,n):
        for j in range(0,n):
            m_ += A[i,j]
    m_ = m_/2.0

    #calculate the weighted degree for each node
    Orig_deg = {}
    Orig_deg = UpdateDeg(A, G.nodes())

    #run Newman alg
    Bestcomps=runGirvanNewman(G, Orig_deg, m_)
    return Bestcomps
 

def graphtodegree(G):
    deglist=list()
    for k,v in nx.degree(G).items():
        deglist.append({'name':k,'deg':v})
    return deglist


def node_dis(G,u,v):#计算两个节点的距离
    n = G.number_of_nodes()
    neigbu=G[u]
    setu=set(neigbu.keys())

    neigbv=G[v]
    setv=set(neigbv.keys())

    if u in setv:
        setv.remove(u)
        setu.remove(v)

    val=setu^setv
    p=len(val)
    return 1.0*p/(n-2)

def dist(G,v,list):#计算节点和分组的距离
    m=0
    for i in list:
        m=node_dis(G,v,i)+m
    n=len(list)
    return 1.0*m/n


def delnode(G,v,deglist):#将v从deglist中删除
    temp=[]
    for each in deglist:
        if v!=each['name']:
            temp.append(each)
    deglist=temp
    return deglist

def match(G,u,v,delist):#???判断两节点是否在嵌套列表的同一个分组中
    for i in range(len(delist)):
        if (u in delist[i] and v in delist[i]):
            return True
    return False 

def k_cluster(G,deglist,k,Bestcomps):#生成大小为k的n个分组
    #i=1#记录分组数目
    #j=1#记录候选列表中节点数目
    #q=1#记录候选分组中的分组数目
    global dist
    M=[]#候选节点列表
    cl=[]
    m=(len(deglist))/int(k)
    #while(deglist!= None):
    while (len(deglist)>k):
        for i in range(m):
            seed=deglist[0]['name']
            #index(seed,Bestcomps)
            cl.append([seed])
            #del deglist[0]
            deglist=delnode(G,seed,deglist)

           
            while (len(cl[i])<k):
                
                M=[]#sam
                v=deglist[0]['name']
                
                mindist=dist(G,v,cl[i])
                for node in deglist:#找出最小距离的节点
                    j=node['name']
                    dis=dist(G,j,cl[i])
                    if dis<mindist:
                        mindist=dis
                        bestnode=j
                for node in deglist:#找出最小距离的节点集合
                    j=node['name']
                    dis=dist(G,j,cl[i])
                    if dis==mindist:
                        M.append(j)
                if len(M)>1:#候选节点有多个的情况
                    j=0
                    while (j<len(M)):
                        #print seed,M[j],Bestcomps,match(G,seed,M[j],Bestcomps)
                        
                        if(match(G,seed,M[j],Bestcomps)):
                            cl[i].append(M[j])
                            deglist=delnode(G,M[j],deglist)
                            break
                        else:
                            j=j+1
                        if (j==len(M)-1):
                            cl[i].append(M[j])
                            deglist=delnode(G,M[j],deglist)
                            break
                #    for v in M:
                #       if(match(seed,v,Bestcomps)):
                #            cl[i].append(v)
                #            delnode(v,deglist)
                #       else:
                #            cl[i].append(M[len(M)-1])
                #            delnode(M[len(M)-1],deglist)
                if (len(M)==1):#候选节点只有一个
                    cl[i].append(M[0])
                    deglist=delnode(G,M[0],deglist)
    #for remain in deglist:#处理剩下的少于k个的节点
    while(len(deglist)!=0):
        remain=deglist[0]
        v=remain['name']
        mincl=dist(G,v,cl[0])
        bestcl=0
        for i in range(len(cl)):
            if(match(G,cl[i][0],v,Bestcomps)):#优先加入到与seed同社区的分组中
                bestcl=i
                break
                #cl[i].append(j)
                #delnode(j,deglist)
            else:
                distcl=dist(G,v,cl[i])
                if distcl<mincl:
                    mincl=distcl
                    bestcl=i
        cl[bestcl].append(v)
        deglist=delnode(G,v,deglist)
    return cl
def APL(G):#非连通网络的平均最短距离
    n=G.number_of_nodes()
    sum=0.0
    for g in nx.connected_component_subgraphs(G):
        m=g.number_of_nodes()
        if m==1:
            pass
        else:
            sum=sum+(1.0*m/n)*(nx.average_shortest_path_length(g))    
    return sum

def LocalPerturbation(G,k):
    #plt.subplot(111)
    
##    plt.figure("Original Graph")
##    nx.draw(G,with_labels = True,pos=nx.spring_layout(G))
##    plt.show()
    toG=G.copy()#togn会改变G，用副本传递
    Bestcomps=togn(toG)#初探社区
    deglist=graphtodegree(G)
    deglist.sort(key=lambda deg:(-deg['deg'],deg['name']),reverse=False)#将节点降序排列
    cl=k_cluster(G,deglist,k,Bestcomps)#分簇

    nG=disturb(G,cl)#扰乱后新的图
    
    return [cl,nG] #return these cluters
    
def main(argv):

    filepath="./data/9.txt"

    H=nx.Graph()# undirect
    G=H.to_undirected()

    readfile_net(G,path=filepath)



    print nx.average_clustering(G)#CC
    print APL(G)#APL

    #togn(G)
    toG=G.copy()#togn会改变G，用副本传递
    Bestcomps=togn(toG)#初探社区

    readfile_net(G,path=filepath)

    deglist=graphtodegree(G)
    deglist.sort(key=lambda deg:(-deg['deg'],deg['name']),reverse=False)#将节点降序排列
    
    cl=k_cluster(G,deglist,3,Bestcomps)#分簇

    #new G
    newG=disturb(G,cl)

    print nx.average_clustering(newG)#CC
    print APL(newG)#APL
    
    
    toN=newG.copy()
    newComps=togn(toN)#新的划分
    
    j=analyze(newComps,Bestcomps)
    com=0.0
    for i in range(len(j)):
        com+=j[i]
    average=com/len(j)
    print "average lost：",average
    
    delta_q=modularity(G,newG,Bestcomps)
    print "delta_q:",delta_q
##    plt.subplot(211)
##    
##    plt.title("old")
##    nx.draw(G,with_labels = True,pos=nx.spring_layout(G))
##    
##
##    plt.subplot(212)
##    plt.title("new")
##    nx.draw(newG,with_labels = True,pos=nx.spring_layout(newG))
##    plt.show()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
