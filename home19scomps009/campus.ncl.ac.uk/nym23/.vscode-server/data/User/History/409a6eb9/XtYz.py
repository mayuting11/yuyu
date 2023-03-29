from ModifiedANTprototype import Modified_ANT
import sys
sys.path.append("Lib/site-packages/pandas")
import pandas as pd
import math
import random
from matplotlib import pyplot
from evacuation_time_total_centricprototype import evacuation_time_total
from sort_lookuptable import sort_result1
from evacuation_time_centric import evacuation_time
from sort_result import sort_result

file_name='Prototypenew'
file_path=r'D:\Pythonyu\user_centric'+'\\'+file_name+'.xlsx'
def main_prototype(num_user):
    #preliminary of plot 
    pyplot.figure(figsize=(15,15))
    ax = pyplot.subplot(131)
    pyplot.axis('off')

    # read exit node
    exit_node_id=pd.read_excel(file_path,names=None,usecols=[8])
    exitnodeid=[]
    exitnodelist=exit_node_id.values.tolist()
    for i in exitnodelist:
        if math.isnan(i[0]):
            continue
        exitnodeid.append(i[0])
    num_exit=len(exitnodeid)
    #print(exitnodeid)

    # read node id data
    node_id=pd.read_excel(file_path,names=None,usecols=[0])
    nodelist=node_id.values.tolist()
    nodeid=[]
    for i in nodelist:
        if math.isnan(i[0]):
            continue
        nodeid.append(i[0])

    # define user node and user number
    #define only one user
    # num_user=1
    # usernode=[]
    # for i in range(int(num_user)):
    #     usernode.append(random.randint(0,len(nodeid)-1))

    #define more than one users
    num_hotspot=2
    hotspot=[]
    usernode=[]
    for i in range(num_hotspot):
        hotspot.append(random.randint(0,len(nodeid)-1))
    for i in range(int(num_user/2)):
        usernode.append(random.randint(0,len(nodeid)-1))
    for i in range(int(num_user/2)):
        usernode.append(random.choice(hotspot))
    print("The hotspots are: {}" .format(hotspot))
    print("The usernode are: {}" .format(usernode))

    # read node capacity data
    node_capacity=pd.read_excel(file_path,names=None,usecols=[5])
    node_capacity_list=[]
    nodecapacitylist=node_capacity.values.tolist()
    for i in nodecapacitylist:
        if math.isnan(i[0]):
            continue
        node_capacity_list.append(i[0])

    # define the deadline
    deadline=80*60/6

    # call Modified_ANT function
    node_dic,look_up_table_user_r,edge_dic=Modified_ANT(ax,file_path,usernode,nodeid,exitnodeid,num_exit,deadline)
    #print(look_up_table_user_r)
    #print(node_capacity_list)

    #user-centric algorithm
    for i in look_up_table_user_r:
        for j in look_up_table_user_r[i]:
            if j[0]>deadline:
                del j
    for i in look_up_table_user_r:
        look_up_table_user_r[i].sort(key=sort_result1)
    #print(look_up_table_user_r)
    user_loc_num,look_up_table_user_opt=evacuation_time(look_up_table_user_r,usernode,edge_dic)
    #print(look_up_table_user_opt)
    print("The locations and numbers of users are: {}".format(user_loc_num))
    Result_all_perpson,TotalTime_typical=evacuation_time_total(look_up_table_user_opt,num_user,node_capacity_list)
    #print(Result_all_perpson)
    TotalTime_worst=sorted(Result_all_perpson,key=sort_result)[-1][1][2]
    Result_all_perpson=dict(Result_all_perpson)
    print("The total expected time of all users is: {}".format(TotalTime_typical))
    print("The total worst-case time of all users is: {}".format(TotalTime_worst))
    Result_all_perpson_r={}
    for i in Result_all_perpson:
        Result_all_perpson_r[i]=[Result_all_perpson[i]]
    #determine the path of each user
    inf=88888888
    Result_all_perpson_rr={}
    for i in user_loc_num:
        Result_all_perpson_rr[i]=[inf,0,inf]
    for i in Result_all_perpson_r:
        for j in Result_all_perpson_r[i]:
            #print(j)
            if j[0]<deadline:
                if j[2]<Result_all_perpson_rr[i][2]:
                    Result_all_perpson_rr[i][2]=j[2]
                    Result_all_perpson_rr[i][0]=j[0]
                    Result_all_perpson_rr[i][1]=j[1]

    #plot the paths of users
    num_path_segment={}
    for i in Result_all_perpson_rr:
        num_path_segment[i]={}
    for i in Result_all_perpson_rr:
        for j in Result_all_perpson_rr[i]:
            #print(j)
            if type(j)!=int:
                for k in range(len(j[0])-1):
                    #print((j[0][k],j[0][k+1]))
                    num_path_segment[i][(j[0][k],j[0][k+1])]=num_path_segment[i].get((j[0][k],j[0][k+1]),0) + 1
        for l in num_path_segment[i]:
            num_path_segment[i][l]=num_path_segment[i][l]*user_loc_num[i]
    num_path_segment_r={}
    for i in num_path_segment:
        for j in num_path_segment[i]:
            num_path_segment_r[j]=num_path_segment_r.get(j,0) + num_path_segment[i][j]
    #print(num_path_segment)
    #print(num_path_segment_r)
    for i in num_path_segment_r:
        ax.plot([node_dic[i[0]][0],node_dic[i[1]][0]],[node_dic[i[0]][1],node_dic[i[1]][1]],c='red',linestyle='-',linewidth=num_path_segment_r[i])

    #calculate the congestion of each node
    number_path_node={}
    for i in num_path_segment_r:
        if i[0]!=i[1]:
            number_path_node[i[0]]=number_path_node.get(i[0],0)+num_path_segment_r[i]
            number_path_node[i[1]]=number_path_node.get(i[1],0)+num_path_segment_r[i]
        else:
            number_path_node[i[0]]=number_path_node.get(i[0],0)+num_path_segment_r[i]
    print("The congestion of each node is:{}".format(number_path_node))
    return(ax,nodeid,number_path_node,TotalTime_typical,TotalTime_worst)

    


