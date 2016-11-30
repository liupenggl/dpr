#-*- coding:utf-8 -*-
__author__ = 'Peng<liupeng@gxnu.edu.cn>'
from scipy import stats
from scipy import sparse
import numpy as np
import matplotlib.pyplot as plt
from gfile import *
import networkx as nx
import random
import string
import math
import itertools as it


def r_perturbS(g, p=None):
    '''固定参数的随机扰动方法，p伯努利实验成功的概率,修改了原图g'''
    n=len(g)
    e_num=len(g.edges())#图中存在的边数

    q = e_num * (1 - p) / ((n * (n - 1)) / 2.0 - e_num)

    listp=stats.bernoulli.rvs(p,size=e_num)
    listp=listp.tolist()
    listq=stats.bernoulli.rvs(q,size=(n * (n - 1)) / 2.0 - e_num)
    listq=listq.tolist()

    del_edges_temp=list()#不能直接删除，后面添加边要用到原始图g。暂存要删除的边。
    for each in g.edges():
        if not listp.pop():
            # print "del{0}".format(each)
            del_edges_temp.append(each)

    for each in nx.non_edges(g):
        if listq.pop():
            # print "add{0}".format(each)
            g.add_edge(*each)
    g.remove_edges_from(del_edges_temp)
    return g#或许不应该提供返回值


def r_perturbSa(g,p=None):
    '''固定参数的随机扰动方法，p伯努利实验成功的概率'''
    A=nx.to_scipy_sparse_matrix(g)
    B=sparse.triu(A).toarray()
    #print B
    n=len(g)
    e_num=len(g.edges())#图中存在的边数

    q = e_num * (1 - p) / ((n * (n - 1)) / 2 - e_num)
    #print q
    i = 0
    ts=0
    listp=stats.bernoulli.rvs(p,size=e_num)
    listp=listp.tolist()
    listq=stats.bernoulli.rvs(q,size=(n * (n - 1)) / 2 - e_num)
    listq=listq.tolist()

    while i<n:
        j=i+1#略过对角线上的0
        while j<n:
            if(B[i,j]==1):
                B[i,j] = listp.pop()#参数p伯努利实验成功的概率
                #ts=ts + 1
                # print "+",ts, ":", i, ",", j, ",", B[i, j]
            else:
                B[i,j] = listq.pop()#参数q伯努利实验成功的概率
                #ts=ts + 1
                # print "-",ts, ":", i, ",", j, ",", B[i, j]
            j = j + 1
        i=i+1

    return nx.from_numpy_matrix(B,create_using=nx.Graph())#重新构建了Graph类型的返回对象


def binomial_vdiS(z,v,g,p):
        """z 是节点的度，node节点的标签，g图,p边仍然存在的概率        """

        n = len(g)
        N=(n*(n-1))/2
        e_num = len(g.edges())  # 图中存在的边数
        q = e_num * (1 - p) / ((n * (n - 1)) / 2 - e_num)

        di = len(g[v])
        sum = 0.0
        t = 0
        while t <= di:
            sum = sum + stats.binom.pmf(t, di, p) * stats.binom.pmf(z-t,N-di, q)
            t += 1
        return sum


def riskS(v,g,p):
    """v是节点，g是图,p边仍然存在的概率，输入为点v被重识别的概率
    """
    di=len(g[v])
    b=binomial_vdiS(di, v, g, p)
    tsum=0
    for each in g:
        tsum=tsum+binomial_vdiS(di, each, g, p)
    return b/tsum


def cal_pS(g, pr):
    """g图,pr要求的隐私保护力度"""
    p=0.05
    for each in g:
        if riskS(each, g, p)>pr:
            while 1:
                p=p+0.05
                print 'v=',each,'p=',p,'r=',riskS(each, g, p)
                if riskS(each, g, p) < pr or p > 0.95:
                    break
    return p


def cal_pSa(g, pr):
    """g图,pr要求的隐私保护力度"""
    p=1
    for each in g:
        if riskS(each, g, p)>pr:
            while 1:
                p=p-0.05
                print 'v=',each,'p=',p,'r=',riskS(each, g, p)
                if riskS(each, g, p) < pr or p<0.05:
                    break
    return p


def r_perturbR(g,R):
    '''可变参数的随机扰动方法'''
    A=nx.to_scipy_sparse_matrix(g)
    B=sparse.triu(A).toarray()
    #print B
    n=len(g)
    i = 0
    ts=0

    while i<n:
        j=i+1
        while j<n:
            if(B[i,j]==1):
                if R[i,j]<1:
                    B[i,j] = stats.bernoulli.rvs(R[i,j])#参数p伯努利实验成功的概率
                else:
                    B[i, j] = stats.bernoulli.rvs(1)  #其实可以去掉
                ts=ts + 1
                #print "+",ts, ":", i, ",", j, ",", B[i, j]
            else:
                if R[i,j]<1:
                    B[i,j] = stats.bernoulli.rvs(R[i,j])#参数q伯努利实验成功的概率
                else:
                    B[i, j] = stats.bernoulli.rvs(0)  #其实可以去掉
                ts=ts + 1
                #print "-",ts, ":", i, ",", j, ",", B[i, j]
            j = j + 1
        i=i+1

    return nx.from_numpy_matrix(B,create_using=nx.Graph())#重新构建了Graph类型的返回对象


# -------------------------------------------------------------------------------------------------------
def gRa(g, w):
    '''w为图中的边数，表示经过减边p扰动后仍然留在数据中的边数'''
    tg = g.copy()
    Rq = nx.to_scipy_sparse_matrix(g)
    Rq = Rq.toarray()

    bw = nx.edge_betweenness_centrality(g, normalized=False)
    norm = sum(bw.values())
    e_num = len(g.edges())

    n = len(g)
    N = (n * (n - 1)) / 2
    for k, v in bw.items():
        g.add_edge(*k, weight=v)
#    print g.edges(data=True)
    R = nx.to_scipy_sparse_matrix(g, weight='weight')
    Rp = R.toarray()

    Rp = w * Rp * 2.0 / Rp.sum()

    q = float(e_num - w) / (N - e_num)

    for i, each in enumerate(Rq):
        for j, e in enumerate(each):
            if e == 0:
                Rp[i, j] = q  # 超级绕采用特别方式在Rp中加入Rq
    for i in range(n):
        Rp[i,i]=0 #去除对角线上的q
    return Rp


def normal_vdiR(z, v, g, Rp):
    """z 是节点的度，v节点的标签，Rp是扰动将矩阵        """
    n = len(g)
    di = len(g[v])
    i=g.nodes().index(v)
    mvar=0
    for each in Rp[i]:
        each=(each if each<1 else 1)
        mvar=mvar+each*(1-each)

    X=stats.norm(di,mvar)
    sum=X.cdf(z+0.5)-X.cdf(z-0.5)

    return sum


def riskR(v,g,R):
    """v是节点，R是扰动将矩阵，输出为点v被重识别的概率
    """
    di=len(g[v])
    b=normal_vdiR(di, v, g, R)
    tsum=0
    for each in g:
        tsum=tsum+normal_vdiR(di, each, g, R)
    return b/tsum
#-------------------------------------------------------------------------------------------------------
def cal_pR(g, pr):
    """g图,pr要求的隐私保护力度"""
    w=len(g.edges())
    w=math.ceil(w*0.8)
    step=math.ceil(0.05*w)
    R=gRa(g, w)
    for each in g:
        if riskR(each, g, R)>pr:
            while 1:
                w=w-step
                R = gRa(g, w)
                print 'v=',each,'w=',w,'r=',riskR(each, g, R)
                if riskR(each, g, R) < pr or w<step:
                    break
    return w
def cal_pRv(v,g,pr):
    w=len(g.edges())
    w=math.ceil(w*0.9)
    step=math.ceil(0.05*w)
    R=gRa(g, w)
    if riskR(v, g, R) > pr:
        while 1:
            w = w - step
            R = gRa(g, w)
            print 'v=', v, 'w=', w, 'r=', riskR(v, g, R)
            if riskR(v, g, R) < pr or w < step:
                break
    return w


def g_r():
    """返回两跳邻居内，可能加入的边"""
    g = nx.Graph()
    da(g)
    print 'g.size=',len(g.nodes())
    h= nx.Graph()
    for node in g:
        h.add_edges_from(com_neigbor(g,node))



def com_neigbor(g,node):
    print 'g.size=',len(g.nodes())
    nb_nodes=set(g.neighbors(node))#防止缺少邻居自己
    for each in g.neighbors(node):
        nb_nodes=nb_nodes.union(set(g.neighbors(each)))
    print nb_nodes
    h=g.subgraph(nb_nodes)
    ch=nx.complement(h)

    return ch.edges()




if __name__=='__main__':
    print 'in grandom'
    g=nx.Graph()

    #    g = read_file_txt(g,r"E:\data\facebook1.txt")
    #g = read_file_txt(g, r"d:\data\facebook1.txt")
    #g = read_file_txt(g,r"d:\data\Cora.txt")
    #g = read_file_txt(g,r"d:\data\CA-GrQc.txt")
    # da(g)
    # p=0.7
    #r=RPerturbS(g,p)
    # r_perturbS(g,0)
    g_r()



    # d=nx.degree(g)
    # print d
    # print sorted(d.items(),key=lambda item:item[1],reverse=True)
    # bw = nx.edge_betweenness_centrality(g, normalized=False)
    # print bw
    #t_facebook_cc(path=r"d:\data\facebook1.txt")
    #t_GrQc_cc(path=r"d:\data\CA-GrQc.txt")
    #t_t_cc(path=r"d:\data\9.txt")
    #DrawGraph(r)
