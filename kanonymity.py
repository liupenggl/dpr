import os
import networkx as nx
import matplotlib.pyplot as plt
from gfile import *

#-------------------------------------------------------------------------------
def graphtodegree(g):
    #calculate the graph's degree sequence
    deglist=list() #deglist is a list of dictionary [{'name': ,'deg': , 'diff':},...]
    for k,v in nx.degree(g).items():
        #print k,v
        deglist.append({'name':k,'deg':v,'diff':None})

    return deglist

#-------------------------------------------------------------------------------
def degree_diff(deglist,begin,end):
    """calculate the difference of a deglist"""
    value=0
    end=end-1
    while begin<end:
        value=value+deglist[begin]['deg']-deglist[end]['deg']
        end-=1
    return value

#-------------------------------------------------------------------------------
def degreee_anony(deglist,k): #greed algorithm use max differece
  
    begin=0  #deglist is a list of dictionary [{'name':"the node" ,'deg':"the node's degreee , 'diff':0,flaga:0 },...]
    nodep=0
    end=len(deglist)

    while(end-nodep>=2*k):
        i=0
        temp=0
        flag=0

        temp=deglist[nodep]['deg']-deglist[nodep+1]['deg']
        while i<2*k-1:
            x=deglist[nodep+i]['deg']-deglist[nodep+i+1]['deg']
            if x>temp:
                temp=x
                flag=i
            i+=1
        if end-nodep-flag-1<k:
            flag=flag-(k-(end-nodep-flag-1))
        if flag<k-1:
            flag=k-1
        deglist[nodep+flag+1]['flaga']=1
        nodep=nodep+1+flag;

 
    j=0 #Calculate the 'diff' and 'flaga'
    temp=deglist[0]['deg']
    for each in deglist:
        if len(each)==4:
            j+=1;
            temp=each['deg']
        each['flaga']=j
        each['diff']=temp-each['deg']
    rvalue=0
    for each in deglist:
        rvalue=rvalue+each['diff']
    return rvalue
#-------------------------------------------------------------------------
def diffSelect(deglist):
    """deglist store the nodes need be annonymized"""
    temp=[]
    for each in deglist:
        if each['diff']!=0:
            temp.append(each)
    deglist=temp
    return deglist

#-------------------------------------------------------------------------
def addEdge(g,deglist,*li):
    i=0
    while i<len(deglist)-1:
        flag=0
        j=i+1
        while j<len(deglist):
            if deglist[i]['name'] not in g.edge[deglist[j]['name']]:
                g.add_edge(deglist[i]['name'],deglist[j]['name'])
                if(li):
                    (li[0]).append((deglist[i]['name'],deglist[j]['name']))#use a parameter list *li 
                deglist[i]['diff']=deglist[i]['diff']-1
                deglist[j]['diff']=deglist[j]['diff']-1                
                if deglist[j]['diff']==0:
                    deglist.pop(j)
                if deglist[i]['diff']==0:
                    deglist.pop(i)
                flag=1
                break
            j=j+1
        if flag!=1:
            i=i+1
    if len(deglist)==0:
        return 0
    else:
        return 1
#-------------------------------------------------------------------------
def addNode(g,deglist,*li):
    for each in deglist:
        while each['diff']>0:
            g.add_edge(each['name'],'a'+str(each['diff']))
            if li:
                (li[0]).append((each['name'],'a'+str(each['diff']))) #use a parameter list *li
            each['diff']-=1


#-------------------------------------------------------------------------
def randomAnony(g,k,*li):
    """Delete and add k nodes from g"""
    import random
    if g.number_of_edges()>=k:
        delEdges=random.sample(g.edges(),k)
        outStr="Randomly delete "+str(k)+" edges:"+"\n"+str(delEdges)+"\n"
    g.remove_edges_from(delEdges)
    noEdges=list(nx.non_edges(g)) #This is an inefficient methond!!!
    if len(noEdges)>k:
        addEdges=random.sample(noEdges,k)
        g.add_edges_from(addEdges)
        outStr=outStr+"Randomly add "+str(k)+" edges:"+"\n"+str(addEdges)+"\n"
    if li:#Display the del/add edges on TxtCtr
        sc=li[0]
        sc.SetValue(outStr)

#-------------------------------------------------------------------------
def clustering(g, nodes=None, weight=None):      
    if g.is_directed():
        raise NetworkXError('Clustering algorithms are not defined ',
                            'for directed graphs.')
    if weight is not None:
        td_iter=_weighted_triangles_and_degree_iter(g,nodes,weight)
    else:
        td_iter=_triangles_and_degree_iter(g,nodes)

    clusterc={}

    for v,d,t in td_iter:
        if t==0:
            clusterc[v]=0.0
        else:
            clusterc[v]=t/float(d*(d-1))

    if nodes in g: 
        return list(clusterc.values())[0] # return single value
    return clusterc

#-------------------------------------------------------------------------
if __name__=='__main__':
    print 'sss'
    #filepath=os.getcwd()
    #filepath=os.path.join(filepath,"data\\AFFIL.NET")

    g=nx.Graph()
    #readFileTxt(g,path=filepath)
    readFileTxt(g)

    deglist=graphtodegree(g)
 
    deglist.sort(key=lambda deg:deg['deg'],reverse=True)

    degreee_anony(deglist,9)

    deglist=diffSelect(deglist)

    addEdge(g,deglist)

    addNode(g,deglist)
    sh(g)
