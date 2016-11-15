#-*- coding:utf-8 -*-
__author__ = 'Peng<liupeng@gxnu.edu.cn>'
from scipy import stats
from scipy import sparse
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
from gfile import *
import networkx as nx
import random
import string
#-------------------------------------------------------------------------------------------------------
def RPerturbSp(g,p=None):
    '''固定参数的随机扰动方法'''
    A=nx.to_scipy_sparse_matrix(g)
    B=sparse.triu(A).toarray()
    #print B
    n=len(g)
    i=0

    ts=0
    while i<n:
        j=i
        while j<n:
            if(B[i,j]==1):
                B[i,j] = stats.bernoulli.rvs(p)#p伯努利实验成功的概率
                ts=ts + 1
                print ts,":",i,",",j,",",B[i,j]
            j = j + 1
        i=i+1
    return nx.from_numpy_matrix(B,create_using=nx.Graph())#重新构建了Graph类型的返回对象
#-------------------------------------------------------------------------------------------------------
def RPerturbS(g,p=None):
    '''固定参数的随机扰动方法'''
    A=nx.to_scipy_sparse_matrix(g)
    B=sparse.triu(A).toarray()
    #print B
    n=len(g)
    e_num=len(g.edges())#图中存在的边数

    q = e_num * (1 - p) / ((n * (n - 1)) / 2 - e_num)
    print q
    i = 0
    ts=0

    while i<n:
        j=i+1
        while j<n:
            if(B[i,j]==1):
                B[i,j] = stats.bernoulli.rvs(p)#p伯努利实验成功的概率
                ts=ts + 1
                print "+",ts, ":", i, ",", j, ",", B[i, j]
            else:
                B[i,j] = stats.bernoulli.rvs(q)#p伯努利实验成功的概率
                ts=ts + 1
                print "-",ts, ":", i, ",", j, ",", B[i, j]
            j = j + 1
        i=i+1

    return nx.from_numpy_matrix(B,create_using=nx.Graph())#重新构建了Graph类型的返回对象
#-------------------------------------------------------------------------------------------------------
def binomial_vdi(z,v,g,p):
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
#-------------------------------------------------------------------------------------------------------
def risk(v,g,p):
    """v是节点，g是图,p边仍然存在的概率，输入为点v被重识别的概率
    """
    di=len(g[v])
    b=binomial_vdi(di, v, g, p)
    tsum=0
    for each in g:
        tsum=tsum+binomial_vdi(di, each, g, p)
    return b/tsum
#-------------------------------------------------------------------------------------------------------
def cal_p(g, pr):
    """g图,p边仍然存在的概率"""
    p=0.05
    for each in g:
        if risk(each, g, p)>pr:
            while 1:
                p=p+0.05
                print 'v=',each,'p=',p,'r=',risk(each, g, p)
                if risk(each, g, p) < pr or p > 0.95:
                    break
    return p
#-------------------------------------------------------------------------------------------------------


def RPerturbS(g,p=None):
    '''可变参数的随机扰动方法'''
    A=nx.to_scipy_sparse_matrix(g)
    B=sparse.triu(A).toarray()
    #print B
    n=len(g)
    e_num=len(g.edges())#图中存在的边数

    q = e_num * (1 - p) / ((n * (n - 1)) / 2 - e_num)
    print q
    i = 0
    ts=0

    while i<n:
        j=i+1
        while j<n:

#-------------------------------------------------------------------------------------------------------


if __name__=='__main__':
    print 'in grandom'
    g=nx.Graph()
    da(g)
    p=0.7
    #r=RPerturbS(g,p)

    # for v in g:
    #     print "z:",v,"=",risk(v,g,p)
    print cal_p(g,0.1)

    #DrawGraph(r)
