import pandas as pd
import math
from matplotlib import pyplot
from initialize import initialize
from relax import relax
from worst_delayprototype import worst_delay
from typicaldelay import typical_delay
import random
#from get_key import get_key
def Modified_ANT(ax,file_path,usernode,nodeid,exitnodeid,num_exit,deadline):
    #read node data
    node_dic={}
   
    #read x coordinate of each node
    node_x=pd.read_excel(file_path,names=None,usecols=[1])
    nodex=[]
    node_x_list=node_x.values.tolist()
    for i in node_x_list:
        if math.isnan(i[0]):
            continue
        nodex.append(i[0])

    #read y coordinate of each node
    node_y=pd.read_excel(file_path,names=None,usecols=[2])
    nodey=[]
    node_y_list=node_y.values.tolist()
    for i in node_y_list:
        if math.isnan(i[0]):
            continue
        nodey.append(i[0])
    
    #plot node
    for i in range(len(nodeid)):
        ax.scatter(nodex[i],nodey[i],s=7,c='darkslategrey')
        ax.text(nodex[i],nodey[i],str(nodeid[i]),color='black')
    for i in range (len(nodeid)):
        node_dic[nodeid[i]]=[nodex[i],nodey[i]]
    #print(node_dic)

    #read edge data
    edge_from_id=pd.read_excel(file_path,names=None,usecols=[4])
    edgefromid=[]
    edgefromlist=edge_from_id.values.tolist()
    for i in edgefromlist:
        if math.isnan(i[0]):
            continue
        edgefromid.append(i[0])
    edge_to_id=pd.read_excel(file_path,names=None,usecols=[5])
    edgetoid=[]
    edgetolist=edge_to_id.values.tolist()
    for i in edgetolist:
        if math.isnan(i[0]):
            continue
        edgetoid.append(i[0])
    # print(edgefromid)
    # print(edgetoid)
    edge=[]
    for i in range(len(edgefromid)):
        edge.append([edgefromid[i],edgetoid[i]])
    #print(edge)
   
    for i in range(len(edgefromid)):
        ax.plot([node_dic[edgefromid[i]][0],node_dic[edgetoid[i]][0]],[node_dic[edgefromid[i]][1],node_dic[edgetoid[i]][1]],c='lightsteelblue',linestyle='dotted',linewidth=1)
    
            
    #plot exit node
    for i in exitnodeid:
        ax.scatter (node_dic[i][0],node_dic[i][1],marker='^',s=40,c='g')

    #define delay parameter
    for i in edge:
            i.append(math.floor(worst_delay(node_dic,i)))
            i.append(math.floor(random.uniform(typical_delay(node_dic,i),worst_delay(node_dic,i))))
    edge_dic={}
    for i in edge:
        edge_dic[(i[0],i[1])]=[i[2],i[3]]
    #print(edge)
    #print(edge_dic)

    #plot user nodes
    colors = ["black","red",'green','blue','purple']
    ncolor = 0
    linewidth=[330,255,180,105,30]
    nlinewidth=0
    for i in usernode:
        ax.scatter (node_dic[i][0],node_dic[i][1],marker='o',s=linewidth[nlinewidth],c='none',edgecolors=colors[ncolor])
        nlinewidth=nlinewidth+1
        ncolor=ncolor+1
    #pyplot.axis('off')
    #pyplot.show()

    #Initialize
    lookup_table=initialize(nodeid,exitnodeid)
    #print(lookup_table)

    for j in exitnodeid:
        for i in range (len(nodeid)-1):
            for e in edge:
                relax(e,lookup_table,deadline)
    #print(lookup_table)
    #print(parents)

    path_list=[[] for i in range(num_exit)]
    table_inter=[]
    #print(edge_dic)
    def addpath(i,j):
        for k in exitnodeid:
            if j[1]!=int(k) and j[1]!=[]:
                m=j[1]
                if type(m)!=list:
                    for l in lookup_table[m]:
                        if l[0]==j[0]-edge_dic[(i,m)][0] or l[0]==j[0]-edge_dic[(i,m)][1]:
                            if l[2]==j[2]-edge_dic[(i,m)][1]:
                                if l not in table_inter:
                                    addpath(m,l)
                                    path_list[exitnodeid.index(k)].append(m)
                                    table_inter.append(l)
                else:
                    for l in lookup_table[m[0][0]]:
                        if (i,m[0][0]) in edge_dic:
                            if l[0]==j[0]-edge_dic[(i,m[0][0])][0] or l[0]==j[0]-edge_dic[(i,m[0][0])][1]:
                                if l[2]==j[2]-edge_dic[(i,m[0][0])][1]:
                                    if l not in table_inter:
                                        addpath(m[0][0],l)
                                        path_list[exitnodeid.index(k)].append(m[0][0])
                                        table_inter.append(l)
            else:
                path_list[exitnodeid.index(k)].append(k)
        return path_list


    look_up_table_user={}
    for i in usernode:
            look_up_table_user[i]=lookup_table[i]
    #print(look_up_table_user)

    for i in look_up_table_user:
        for j in range(len(lookup_table[i])):
        #print(lookup_table[i][j])
            path_list=addpath(i,lookup_table[i][j])
            for k in path_list:
                path_list[path_list.index(k)]=k[::-1]
            look_up_table_user[i][j][1]=path_list
            path_list=[[] for i in range(num_exit)]
            table_inter=[]

    # correct the order of a path
    for i in look_up_table_user:
        for j in look_up_table_user[i]:
            for k in j[1]:
                k.insert(0,i)

    # delete the repeated paths
    look_up_table_user_r={}
    for i in usernode:
        look_up_table_user_r[i]=[]
    for i in look_up_table_user:
        for j in look_up_table_user[i]:
            if j not in look_up_table_user_r[i]:
                look_up_table_user_r[i].append(j)
    #print(look_up_table_user_r)
    return node_dic,look_up_table_user_r,edge_dic


