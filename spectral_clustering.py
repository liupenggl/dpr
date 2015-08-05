#coding=utf-8
#MSC means Multiple Spectral Clustering 
import numpy as np
import scipy.linalg as linalg
import networkx as nx
import matplotlib.pyplot as plt
from scipy.cluster.vq import vq, kmeans
from gfile import *

def getNormLaplacian(W):
	"""input matrix W=(w_ij)
	"compute D=diag(d1,...dn)
	"and L=D-W
	"and Lbar=D^(-1/2)LD^(-1/2)
	"return Lbar
	"""
	d=[np.sum(row) for row in W]
	D=np.diag(d)
	L=D-W
	#Dn=D^(-1/2)
	Dn=np.power(np.linalg.matrix_power(D,-1),0.5)
	Lbar=np.dot(np.dot(Dn,L),Dn)
	return Lbar

def getKSmallestEigVec(Lbar,k):
	"""input
	"matrix Lbar and k
	"return
	"k smallest eigen values and their corresponding eigen vectors
	"""
	eigval,eigvec=linalg.eig(Lbar)
	dim=len(eigval)

	#查找前k小的eigval
	dictEigval=dict(zip(eigval,range(0,dim)))
	kEig=np.sort(eigval)[0:k]
	ix=[dictEigval[k] for k in kEig]
	return eigval[ix],eigvec[:,ix]

def checkResult(Lbar,eigvec,eigval,k):
	"""
	"input
	"matrix Lbar and k eig values and k eig vectors
	"print norm(Lbar*eigvec[:,i]-lamda[i]*eigvec[:,i])
	"""
	check=[np.dot(Lbar,eigvec[:,i])-eigval[i]*eigvec[:,i] for i in range(0,k)]
	#print ("check:%s" % check)		
	length=[np.linalg.norm(e) for e in check]/np.spacing(1)
	print("Lbar*v-lamda*v are %s * %s" % (length,np.spacing(1)))



def spectral_clustering(g,k=2):
    m=nx.to_numpy_matrix(g)
    Lbar=getNormLaplacian(m)#获取拉普拉斯矩阵
    kEigVal,kEigVec=getKSmallestEigVec(Lbar,k)#获取k个特征kEigVal和对应的k个特征向量
    center = kmeans(kEigVec, k, iter=1000)[0]#采用kmeans进行聚类，可以选择iter
    result = vq(kEigVec, center)[0]#result存储分组信息，如：[0,0,0,1,1]表示有两个分组，第一组包含3个元素
    return result


def shs(g,clist):
    colList=dict.fromkeys(g.nodes())
    for index,lable in  enumerate(g.nodes()):
        colList[lable]=0.1*clist[index]
    plt.figure(figsize=(8,8))
    pos=nx.spring_layout(g)
    nx.draw_networkx_edges(g,pos,alpha=0.4)
    nx.draw_networkx_nodes(g,pos,nodelist=colList.keys(),
		    node_color=colList.values(),
		    cmap=plt.cm.rainbow)
    nx.draw_networkx_labels(g,pos,font_size=10,font_family='sans-serif')
    plt.axis('off')
    plt.title(g.name)
    import time
    #plt.savefig("ssss.png")
    plt.show()


if __name__=="__main__":
    k=5
    g=nx.planted_partition_graph(k,10,0.8,0.02)

    result=spectral_clustering(g,k)
    shs(g,result)

    #k=8
    #g=nx.Graph()
    #filepath=r'D:\data\prandom\polbooks.txt'
    #read_file_txt(g,path=filepath)
    #result=spectral_clustering(g,k)
    #shs(g,result)


#g=nx.karate_club_graph()

#nodeNum=len(g.nodes())
#m=nx.to_numpy_matrix(g)
#Lbar=getNormLaplacian(m)

#kEigVal,kEigVec=getKSmallestEigVec(Lbar,k)
##print("k eig val are %s" % kEigVal)
#print("k eig vec are %s" % kEigVec)

##跳过k means，用最简单的符号判别的方法来求点的归属
#center = kmeans(kEigVec, k, iter=1000)[0]
#print "center"
#print center

#result = vq(kEigVec, center)[0]
#print result
#checkResult(Lbar,kEigVec,kEigVal,k)

##clusterA=[i for i in range(0,nodeNum) if kEigVec[i,1]>0]
##clusterB=[i for i in range(0,nodeNum) if kEigVec[i,1]<0]
###draw graph
#colList=dict.fromkeys(g.nodes())
#for index,lable in  enumerate(g.nodes()):
#    colList[lable]=0.1*result[index]

##for node,score in colList.items():
##	if node in clusterA:
##		colList[node]=0
##	else:
##		colList[node]=0.6
#plt.figure(figsize=(8,8))
#pos=nx.spring_layout(g)
#nx.draw_networkx_edges(g,pos,alpha=0.4)
#nx.draw_networkx_nodes(g,pos,nodelist=colList.keys(),
#		node_color=colList.values(),
#		cmap=plt.cm.Reds_r)
#nx.draw_networkx_labels(g,pos,font_size=10,font_family='sans-serif')
#plt.axis('off')
#plt.title("karate_club spectral clustering")
#plt.savefig("spectral_clustering_result.png")
#plt.show()
