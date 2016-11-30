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
import datetime

def test_cc(path=r"d:\data\facebook1.txt"):
    rstr = ''
    g = nx.Graph()
    g = read_file_txt(g, path)
    sl=g.selfloop_edges()
    print sl
    g.remove_edges_from(sl)
    # bg=g.copy()
    plist = [1.0,0.9, 0.8, 0.7, 0.6,0.5,0.4]
    ds= sorted(nx.degree_centrality(g).items(),key=lambda item: item[1], reverse=True)

    for p in plist:
        pg=r_perturbS(g, p)
        rstr=rstr+'{0:8},{1:10.4}'.format(p,nx.average_clustering(pg))

        dpgs=nx.degree_centrality(pg)#扰动后的结点度中心性
        dsum=0
        for i in range(20):#前20个
            dsum=dsum+abs(ds[i][1]-dpgs[ds[i][0] ])
        rstr = rstr + '{0:8},{1:10.4}'.format(p, dsum)
        rstr = rstr + '\n'

    try:
        tu_path=os.path.splitext(path)
        now = datetime.datetime.now().strftime('%m%d-%H%M')
        path=tu_path[0]+'_pcc_'+now+tu_path[1]
        f=open(path, 'w')
    except:
        print "int readFileTxt open error"

    f.write(rstr)
    f.close()




if __name__=='__main__':
    print 'in temp'
    test_cc(path=r"d:\data\facebook1.txt")
    # test_cc(path=r"d:\data\CA-GrQc.txt")
    #test_cc(path=r"d:\data\Email-Enron.txt")
    #test_cc(path=r"d:\data\p2p-Gnutella08.txt")
    # test_cc(path=r"d:\data\9.txt")



