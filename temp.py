# -*- coding:utf-8 -*-
__author__ = 'Peng<liupeng@gxnu.edu.cn>'
from grandom import *
from scipy import stats
from scipy import sparse
import numpy as np
import matplotlib.pyplot as plt
from gfile import *
from rsel import *
import networkx as nx
import random
import string
import math
import os

def t_facebook_cc1(path=r"d:\data\facebook1.txt"):
    rstr = ''
    g = nx.Graph()
    g = read_file_txt(g, path)
    plist = [1.0,0.9, 0.8, 0.7, 0.6,0.5,0.4]
    ds= sorted(nx.degree(g).items(),key=lambda item: item[1], reverse=True)

    for p in plist:
        pg=r_perturbS(g, p)
        rstr=rstr+'{0:8},{1:10.4}'.format(p,nx.average_clustering(pg))

        dpgs= sorted(nx.degree_centrality(pg).items(),key=lambda item: item[1], reverse=True)
        dsum=0
        for i in range(20):
            dsum=abs(dsum+dpgs[i][1]-ds[i][1])
        rstr = rstr + '{0:8},{1:10.4}'.format(p, dsum)
        rstr = rstr + '\n'

    try:
        path=path.replace('book1','book1_pcc')
        f=open(path, 'w')
    except:
        print "int readFileTxt open error"

    f.write(rstr)
    f.close()

def t_GrQc_cc1(path=r"d:\data\CA-GrQc.txt"):
    rstr = ''
    g = nx.Graph()
    g = read_file_txt(g, path)
    plist = [1.0,0.9, 0.8, 0.7, 0.6,0.5,0.4]
    ds= sorted(nx.degree(g).items(),key=lambda item: item[1], reverse=True)

    for p in plist:
        pg = r_perturbS(g, p)
        rstr = rstr + '{0:8},{1:10.4}'.format(p,nx.average_clustering(pg))

        dpgs= sorted(nx.degree_centrality(pg).items(),key=lambda item: item[1], reverse=True)
        dsum=0
        for i in range(20):
            dsum=abs(dsum+dpgs[i][1]-ds[i][1])
        rstr = rstr + '{0:8},{1:10.4}'.format(p, dsum)
        rstr = rstr + '\n'
    try:
        path=path.replace('GrQc','GrQcp_cc')
        f=open(path, 'w')
    except:
        print "int readFileTxt open error"

    f.write(rstr)
    f.close()

def t_Gnutella_cc1(path=r"d:\data\p2p-Gnutella08.txt"):
    rstr = ''
    g = nx.Graph()
    g = read_file_txt(g, path)
    plist = [1.0,0.9, 0.8, 0.7, 0.6,0.5,0.4]
    ds= sorted(nx.degree(g).items(),key=lambda item: item[1], reverse=True)

    for p in plist:
        pg = r_perturbS(g, p)
        rstr = rstr + '{0:8},{1:10.4}'.format(p,nx.average_clustering(pg))

        dpgs= sorted(nx.degree_centrality(pg).items(),key=lambda item: item[1], reverse=True)
        dsum=0
        for i in range(20):
            dsum=abs(dsum+dpgs[i][1]-ds[i][1])
        rstr = rstr + '{0:8},{1:10.4}'.format(p, dsum)
        rstr = rstr + '\n'

    try:
        path=path.replace('p2p-Gnutella','p2p-Gnutellap_cc.txt')
        f=open(path, 'w')
    except:
        print "int Create File error"

    f.write(rstr)
    f.close()

def t_Email_cc1(path=r"d:\data\Email-Enron.txt"):
    rstr = ''
    g = nx.Graph()
    g = read_file_txt(g, path)
    plist = [1.0,0.9, 0.8, 0.7, 0.6,0.5,0.4]

    for p in plist:
        pg = r_perturbSa(g, p)
        rstr = rstr + '{0:8},{1:10.4}'.format(p,nx.average_clustering(pg))

        dpgs= sorted(nx.degree_centrality(pg).items(),key=lambda item: item[1], reverse=True)
        dsum=0
        for i in range(20):
            dsum=abs(dsum+dpgs[i][1]-ds[i][1])
        rstr = rstr + '{0:8},{1:10.4}'.format(p, dsum)
        rstr = rstr + '\n'

    try:
        path=path.replace('Email-Enron','Email-Enronp_cc')
        f=open(path, 'w')
    except:
        print "int Create File error"

    f.write(rstr)
    f.close()


if __name__=='__main__':
    print 'in temp'
    t_facebook_cc1()
    #t_GrQc_cc1()
    #t_Gnutella_cc1()
    #t_Email_cc1()


