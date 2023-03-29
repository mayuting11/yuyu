import pandas as pd
from matplotlib import pyplot
import numpy
from distanceg import distance
from graph import graph_construct
from floydalgorithm import floyd
import json
from get_key import get_key
from power_drain import power_drain
from power_consumption import power_consumption
import random
import xlwt
def shortest(num_user,num_chargingstation):
    #color settings
    color_edge='#525353'
    color_node='#494949'
    colors = ["#EAA813","#CB1313"]

    #读取node,转成字典形式
    file_namenode='plain.nod'
    file_nameedge='plain.edg'
    data_node_id=pd.read_csv(r'/home/campus.ncl.ac.uk/nym23/demo_sumo'+'//'+file_namenode+'.csv',sep=';',header=1,usecols=[5])
    array_node_id=data_node_id.values[0::,0::] 
    data_node_coordinate = pd.read_csv(r'/home/campus.ncl.ac.uk/nym23/demo_sumo'+'//'+file_namenode+'.csv',sep=';',header=1,usecols=[7,8])
    array_node_coordinate=data_node_coordinate.values[0::,0::] 
    array_node_coordinate_r = numpy.zeros((len(array_node_id),3))
    for i in range(len(array_node_id)):
        array_node_coordinate_r[i]=numpy.append(array_node_coordinate[i],i)
    dic_node={}
    for i in range(len(array_node_id)):
        dic_node[''.join(array_node_id[i])]=array_node_coordinate_r[i]
    dic_node_r={}
    for i in dic_node:
        dic_node_r[i]=[str(j) for j in dic_node[str(i)]]
    node_id_list=[]
    for i in dic_node:
        node_id_list.append(i)
    #print(len(dic_node_r))

    #读取边
    data_edge_id=pd.read_csv(r'/home/campus.ncl.ac.uk/nym23/demo_sumo'+'//'+file_nameedge+'.csv',sep=';',header='infer',usecols=[3])
    array_edge_id=data_edge_id.values[0::,0::] 
    data_edge_from=pd.read_csv(r'/home/campus.ncl.ac.uk/nym23/demo_sumo'+'//'+file_nameedge+'.csv',sep=';',header='infer',usecols=[2])
    array_edge_from=data_edge_from.values[0::,0::] 
    data_edge_to=pd.read_csv(r'/home/campus.ncl.ac.uk/nym23/demo_sumo'+'//'+file_nameedge+'.csv',sep=';',header='infer',usecols=[8])
    array_edge_to=data_edge_to.values[0::,0::] 
    data_edge_speed=pd.read_csv(r'/home/campus.ncl.ac.uk/nym23/demo_sumo'+'//'+file_nameedge+'.csv',sep=';',header='infer',usecols=[7])
    array_edge_speed=data_edge_speed.values[0::,0::] 
    data_edge_type=pd.read_csv(r'/home/campus.ncl.ac.uk/nym23/demo_sumo'+'//'+file_nameedge+'.csv',sep=';',header='infer',usecols=[9])
    array_edge_type=data_edge_type.values[0::,0::] 
    array_edge_fromto_r = [[0 for j in range(3)] for i in range(len(array_edge_id))]
    for i in range(len(array_edge_id)):
        array_edge_fromto_r[i]=[''.join(str(array_edge_from[i][0])),''.join(str(array_edge_to[i][0])),''.join(str(array_edge_type[i][0])),''.join(str(array_edge_speed[i][0]))]
    dic_edge={}
    for i in range(len(array_edge_id)):
        dic_edge[''.join(array_edge_id[i])]=array_edge_fromto_r[i]

    #print(2*len(dic_edge))

    #plot node and edge
    # for i in range(len(array_node_id)):
    #     pyplot.scatter (array_node_coordinate_r[i][0],array_node_coordinate_r[i][1],s=0,c=color_node)
    #     #pyplot.annotate(str(i),(waypoint[i]['x'],waypoint[i]['y']),(waypoint[i]['x']+2,waypoint[i]['y']+2) )
    # for i in range(len(array_edge_id)):
    #     pyplot.plot([dic_node[''.join(array_edge_from[i])][0],dic_node[''.join(array_edge_to[i])][0]],[dic_node[''.join(array_edge_from[i])][1],dic_node[''.join(array_edge_to[i])][1]],c=color_edge,lw=1,linestyle=':')

    #计算电量数据
    dic_edge=power_drain(dic_edge,dic_node_r)
    #print(dic_edge)

    # #创建图数据
    # data_graph=[]
    # inf=99999999999999999999999999999999999
    # for i in range(len(array_edge_id)):
    #     data_graph.append([dic_node[''.join(array_edge_from[i])][2],dic_node[''.join(array_edge_to[i])][2],distance(dic_node[''.join(array_edge_from[i])][0],dic_node[''.join(array_edge_to[i])][0],dic_node[''.join(array_edge_from[i])][1],dic_node[''.join(array_edge_to[i])][1])])
    # #print(data_graph)

    # #construct the graph
    # for datagraph in data_graph:
    #     datagraph[0]=int(float(str(datagraph[0])))
    #     datagraph[1]=int(float(str(datagraph[1])))

    # num_node=len(array_node_id)
    # graph_roadmap,parents_ini=graph_construct(data_graph,num_node)
    # #print(parents_ini)

    # #floyd algorithm
    # real_graph, parents=floyd(graph_roadmap,num_node,parents_ini)
    # #print (parents)

    # #print path
    # path_list=[]
    # def print_path(i, j):
    #     if i != j:
    #         print_path(i, parents[i][j])
    #     #print(j, end='-->')
    #     path_list.append(get_key(j,dic_node))
    #     return path_list

    #设置node436933812为目的节点
    #endpoint
    endpoint='436933812'
    endpoint_index=numpy.where(array_node_id=='436933812')
    endpoint_index=int(endpoint_index[0])
    #pyplot.scatter (dic_node[endpoint][0],dic_node[endpoint][1],s=60,c='g',marker='s',label='Destination')

    #The initial position of vehicles
    random.seed(3)
    usernodelist=random.sample(node_id_list,num_user)
    usernode_index=[]
    for i in usernodelist:
        usernode_index.append(int(numpy.where(array_node_id==i)[0]))

    #charging station
    random.seed(0)
    charging_station=random.sample(node_id_list,num_chargingstation)

    #save the data into an excel sheet
    book=xlwt.Workbook(encoding='utf-8',style_compression=0)
    filename_result='distance_charging_bar'
    sheet = book.add_sheet(filename_result,cell_overwrite_ok=True)
    #write the headlines
    col = ('Charging station ID','Electric vehicle ID')
    for i in range(len(col)):
            sheet.write(0,i,col[i])
    #write the data on charging station and the initial electrical vehicle
    num_line1=1
    num_line2=1
    for i in charging_station:
        for j in range(0,1):
            sheet.write(num_line1,j,i)
        num_line1=num_line1+1
    for i in usernodelist:
        for k in range(1,2):
            sheet.write(num_line2,k,i)
        num_line2=num_line2+1
    savepath = '/home/campus.ncl.ac.uk/nym23/demo_sumo/distance_charging_bar.xls'
    book.save(savepath)
    charging_station_index=[]
    for i in charging_station:
        charging_station_index.append(int(numpy.where(array_node_id==i)[0]))


    # #plot the charging station
    # for i in range(len(charging_station)-1):
    #     pyplot.scatter(dic_node[charging_station[i]][0],dic_node[charging_station[i]][1],s=60,c='b',marker='^')
    # for i in range(len(charging_station)-1,len(charging_station)):
    #     pyplot.scatter(dic_node[charging_station[i]][0],dic_node[charging_station[i]][1],s=60,c='b',marker='^',label='Charging Station')
    # path_matrix=['NON' for x in range(num_user)]
    # battery_remaining=[[] for z in range(num_user)]
    # energy_initial=30000
    # energy_chagingstation=30000
    # virtual_distance=15*60*13.89
    # cost_tot_list=[]
    # for i in range(num_user):
    #     battery_remaining[i].append(energy_initial)

    # #generate the path list
    # for i in range(num_user):
    #     path_matrix[i]=print_path(usernode_index[i],endpoint_index)
    #     path_list=[]
    #     cost_tot_list.append(real_graph[usernode_index[i]][endpoint_index])
    # for i in range(num_user):
    #     for j in path_matrix[i]:
    #         if j in charging_station:
    #             cost_tot_list[i]+virtual_distance
    # #print('The shortest path of vehicles:',path_matrix)
    # #print('The total length of the path for vehicles:',cost_tot_list)

    # #calculate the remaining battery of each node in the trace 
    # for i in range(num_user):
    #     for j in range (1,len(path_matrix[i])):
    #         if path_matrix[i][j] not in charging_station:
    #             if battery_remaining[i][-1]>=0:
    #                 battery_remaining[i].append(battery_remaining[i][-1]-power_consumption(path_matrix[i][j-1],path_matrix[i][j],dic_node,dic_edge))
    #             else:
    #                 break
    #         else:
    #             battery_remaining[i].append(energy_chagingstation) 
    # #print('The remaining battery of vehicles at each node:',battery_remaining)

    # # the real path of vehicles
    # flag_badpath=False
    # list_bad_path_index=[]
    # for i in range(len(battery_remaining)):
    #     for j in battery_remaining[i]:
    #         if j<0:
    #             flag_badpath=True
    #     if flag_badpath==True:
    #         list_bad_path_index.append(i)
    # print('The number of vehicles running out of electricity:',len(list_bad_path_index))
    # #print(path_matrix)
    # #print(real_charging_station)
    # #print(battery_remaining)
    # #print(cost_tot_list)

    # #print(len(path_matrix))
    # #calculate the number of edges traversed by vehicles
    # num_edge={}
    # for i in range(len(path_matrix)):
    #     for j in range(len(path_matrix[i])-1):
    #         for k in dic_edge:
    #             if (path_matrix[i][j]==dic_edge[k][0] and path_matrix[i][j+1]==dic_edge[k][1]) or (path_matrix[i][j]==dic_edge[k][1] and path_matrix[i][j+1]==dic_edge[k][0]):
    #                 if (path_matrix[i][j],path_matrix[i][j+1]) in num_edge.keys():
    #                     num_edge[(path_matrix[i][j],path_matrix[i][j+1])]+= 1
    #                 else:
    #                     num_edge[(path_matrix[i][j],path_matrix[i][j+1])]=1
    # #print(num_edge)
    # #print('The edge parameter:',dic_edge)

    # #plot the path of vehicles
    # print(path_matrix)
    # print(len(path_matrix))
    # for i in range(num_user):
    #     # print(len(path_matrix[i]))
    #     # print(len(battery_remaining[i]))
    #     if i not in list_bad_path_index:
    #         pyplot.scatter(dic_node[usernodelist[i]][0],dic_node[usernodelist[i]][1],s=100,c=colors[i],marker='*',label='Electric Vehicle')
    #         # for j in range(len(path_matrix[i])-1):
    #         #     if battery_remaining[i][j+1]>=0 and path_matrix[i][j]!=path_matrix[i][j+1]:
    #         #         pyplot.plot([dic_node[path_matrix[i][j]][0],dic_node[path_matrix[i][j+1]][0]],[dic_node[path_matrix[i][j]][1],dic_node[path_matrix[i][j+1]][1]],lw=2*num_edge[(path_matrix[i][j],path_matrix[i][j+1])],c=colors[0])
    #     else:
    #         pyplot.scatter(dic_node[usernodelist[i]][0],dic_node[usernodelist[i]][1],s=100,c=colors[i],marker='*',label='Electric Vehicle')
    #         # for j in range(len(battery_remaining[i])-1):
    #         #     if battery_remaining[i][j+1]>=0 and path_matrix[i][j]!=path_matrix[i][j+1]:
    #         #         pyplot.plot([dic_node[path_matrix[i][j]][0],dic_node[path_matrix[i][j+1]][0]],[dic_node[path_matrix[i][j]][1],dic_node[path_matrix[i][j+1]][1]],lw=2*num_edge[(path_matrix[i][j],path_matrix[i][j+1])],c=colors[1])
    # pyplot.legend(fontsize=15)
    # pyplot.axis('off')
    # pyplot.show()