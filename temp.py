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
    w = [1945, 1294, 860, 643]
    for each in w:
        R=gRa(g,each)
        pg=r_perturbR(g, R)
        rstr=rstr+'{0:8},{1:10.4}'.format(each,nx.average_clustering(pg))
        rstr=rstr+'\n'

    try:
        path=path.replace('book1','book1_cc')
        f=open(path, 'w')
    except:
        print "int readFileTxt open error"

    p = np.array(w)/4813.0
    for each in p:
        pg=r_perturbS(g, each)
        rstr=rstr+'{0:8},{1:10.4}'.format(each,nx.average_clustering(pg))
        rstr=rstr+'\n'

    f.write(rstr)
    f.close()

def t_GrQc_cc1(path=r"d:\data\CA-GrQc.txt"):
    rstr = ''
    g = nx.Graph()
    g = read_file_txt(g, path)
    w = [14496,13454,12394,9782]
    for each in w:
        R=gRa(g,each)
        pg=r_perturbR(g, R)
        rstr=rstr+'{0:8},{1:10.4}'.format(each,nx.average_clustering(pg))
        rstr=rstr+'\n'

    try:
        path=path.replace('GrQc','GrQc_cc')
        f=open(path, 'w')
    except:
        print "int readFileTxt open error"

    p = np.array(w)/14496.0
    for each in p:
        pg=r_perturbS(g, each)
        rstr=rstr+'{0:8},{1:10.4}'.format(each,nx.average_clustering(pg))
        rstr=rstr+'\n'

    f.write(rstr)
    f.close()

def t_Gnutella_cc1(path=r"d:\data\p2p-Gnutella08.txt"):
    rstr = ''
    g = nx.Graph()
    g = read_file_txt(g, path)
    w = [20777,18700,17995,17023]
    for each in w:
        R=gRa(g,each)
        pg=r_perturbR(g, R)
        rstr=rstr+'{0:8},{1:10.4}'.format(each,nx.average_clustering(pg))
        rstr=rstr+'\n'

    try:
        path=path.replace('p2p-Gnutella','GrQcp2p-Gnutella_cc')
        f=open(path, 'w')
    except:
        print "int Create File error"

    p = np.array(w)/20777.0
    for each in p:
        pg=r_perturbS(g, each)
        rstr=rstr+'{0:8},{1:10.4}'.format(each,nx.average_clustering(pg))
        rstr=rstr+'\n'

    f.write(rstr)
    f.close()

def t_t_cc1(path=r"d:\data\9.txt"):
    rstr = ''
    g = nx.Graph()
    g = read_file_txt(g, path)
    w = [14,13,12,6]
    print nx.average_clustering(g)
    for each in w:
        R=gRa(g,each)
        pg=r_perturbR(g, R)
        rstr=rstr+'{0:8},{1:10.4}'.format(each,nx.average_clustering(pg))
        rstr=rstr+'\n'

    try:
        path=path.replace('9','9_cc')
        f=open(path, 'w')
    except:
        print "int Create File error"

    p = np.array(w)/14.0
    for each in p:
        pg=r_perturbS(g, each)
        rstr=rstr+'{0:8},{1:10.4}'.format(each,nx.average_clustering(pg))
        rstr=rstr+'\n'

    f.write(rstr)
    f.close()
if __name__=='__main__':
    print 'in temp'
    t_t_cc1(path=r"d:\data\9.txt")


