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
import xlrd
from numpy import *
def shortestcharging_trace(num_user,num_chargingstation):
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
    #print(dic_node_r)

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


    # #plot node and edge
    # for i in range(len(array_node_id)):
    #     pyplot.scatter (array_node_coordinate_r[i][0],array_node_coordinate_r[i][1],s=0,c=color_node)
    #     #pyplot.annotate(str(i),(waypoint[i]['x'],waypoint[i]['y']),(waypoint[i]['x']+2,waypoint[i]['y']+2) )
    # for i in range(len(array_edge_id)):
    #     pyplot.plot([dic_node[''.join(array_edge_from[i])][0],dic_node[''.join(array_edge_to[i])][0]],[dic_node[''.join(array_edge_from[i])][1],dic_node[''.join(array_edge_to[i])][1]],c=color_edge,lw=1,linestyle=':')

    #计算电量数据
    dic_edge=power_drain(dic_edge,dic_node_r)
    #print(dic_edge)

    #创建图数据
    data_graph=[]
    inf=99999999
    for i in range(len(array_edge_id)):
        data_graph.append([dic_node[''.join(array_edge_from[i])][2],dic_node[''.join(array_edge_to[i])][2],distance(dic_node[''.join(array_edge_from[i])][0],dic_node[''.join(array_edge_to[i])][0],dic_node[''.join(array_edge_from[i])][1],dic_node[''.join(array_edge_to[i])][1])])
    #print(data_graph)

    #建图
    for datagraph in data_graph:
        datagraph[0]=int(float(str(datagraph[0])))
        datagraph[1]=int(float(str(datagraph[1])))
    num_node=len(array_node_id)
    graph_roadmap,parents_ini=graph_construct(data_graph,num_node)
    #print(parents_ini)

    #floyd algorithm
    real_graph, parents=floyd(graph_roadmap,num_node,parents_ini)
    #print (parents)

    #print path
    path_list=[]
    def print_path(i, j):
        if i != j:
            print_path(i, parents[i][j])
        #print(j, end='-->')
        path_list.append(get_key(j,dic_node))
        return path_list

    #设置node436933812为目的节点
    #endpoint
    endpoint='436933812'
    endpoint_index=numpy.where(array_node_id=='436933812')
    endpoint_index=int(endpoint_index[0])
    #pyplot.scatter (dic_node[endpoint][0],dic_node[endpoint][1],s=60,c='g',marker='s',label='Destination')

    #The initial position of vehicles
    #read the data on vehicle node saved in the excel
    file_name = xlrd.open_workbook('/home/campus.ncl.ac.uk/nym23/demo_sumo/traceofvehicle.xls')#得到文件
    table =file_name.sheets()[0]#得到sheet页
    nrows = table.nrows #总行数
    ncols = table.ncols #总列数
    line_user = 1
    usernodelist=[]
    usernode_index=[]
    while line_user  < num_user+1:
        cell=table.row_values(line_user )[1] #得到users数据
        #ctype = table.cell(i,2).ctype #得到worst-case evacuation time数据的格式
        usernodelist.append(cell)
        line_user =line_user +1
    for i in usernodelist:
        usernode_index.append(int(numpy.where(array_node_id==i)[0]))
    #print(usernodelist)

    #set charging station
    #spare charging station
    line_charging=2
    charging_station=[]
    while line_charging< num_chargingstation+1:
        cell=table.row_values(line_charging)[0] #得到users数据
        #ctype = table.cell(i,2).ctype #得到worst-case evacuation time数据的格式
        charging_station.append(cell)
        line_charging=line_charging+1
    charging_station_index=[]
    real_charging_station=['NON' for y in range(num_user)]
    for i in charging_station:
        charging_station_index.append(int(numpy.where(array_node_id==i)[0]))
    #print(charging_station)

    # #plot charging station
    # for i in range(len(charging_station)-1):
    #     pyplot.scatter(dic_node[charging_station[i]][0],dic_node[charging_station[i]][1],s=40,c='b',marker='^')
    # for i in range(len(charging_station)-1,len(charging_station)):
    #     pyplot.scatter(dic_node[charging_station[i]][0],dic_node[charging_station[i]][1],s=40,c='b',marker='^',label='Charging Station')

    #calculate the path list
    path_matrix=['NON' for x in range(num_user)]
    virtual_distance=15*60*13.89
    power_sechal_tot=0
    power_firhal_tot=0
    energy_initial=35000
    energy_chagingstation=35000
    cost_tot_list=[]

    for i in range(num_user):
        cost_tot=inf
        for j in charging_station_index:
            path_matrix[i]=print_path(usernode_index[i],j)
            path_list=[]
            #print('the first half path',path_matrix)
            for l in range(len(path_matrix[i])-1):
                #print(path_matrix[i][l],path_matrix[i][l+1])
                power_dege=power_consumption(path_matrix[i][l],path_matrix[i][l+1],dic_node,dic_edge)
                #print(power_dege)
                power_firhal_tot=power_firhal_tot+power_dege
                #print(power_firhal_tot)
            path_matrix_sec=print_path(j,endpoint_index)
            #print('the second half path',path_matrix_sec)
            path_list=[]
            for k in path_matrix_sec:
                path_matrix[i].append(k)
                if path_matrix[i][-2]!=path_matrix[i][-1]:
                    power_dege=power_consumption(path_matrix[i][-2],path_matrix[i][-1],dic_node,dic_edge)
                    power_sechal_tot=power_sechal_tot+power_dege
            if power_firhal_tot<=energy_initial and power_sechal_tot<=energy_chagingstation:
                if real_graph[usernode_index[i]][j]+real_graph[j][endpoint_index]<cost_tot:
                    cost_tot=real_graph[usernode_index[i]][j]+real_graph[j][endpoint_index]
                    real_charging_station[i]=[j,array_node_id[j]]
                    #print(real_charging_station[i])
        cost_tot_list.append(cost_tot)
        if real_charging_station[i]=='NON':
            print('No path for',array_node_id[usernode_index[i]],'due to eneregy constraint') 
    #print(path_matrix)

    #the real path of vehicles
    list_bad_path_index=[]
    for i in range(num_user):
        if real_charging_station[i]!='NON':
            path_matrix[i]=print_path(usernode_index[i],real_charging_station[i][0])
            path_list=[]
            path_matrix_sec=print_path(real_charging_station[i][0],endpoint_index)
            path_list=[]
            for j in path_matrix_sec:
                path_matrix[i].append(j)
            path_matrix[i].remove(real_charging_station[i][1])
        else:
            path_matrix[i]=print_path(usernode_index[i],endpoint_index)
            path_list=[]
            list_bad_path_index.append(i)
    print('The number of vehicles running out of electricity for SSP-NN:',len(list_bad_path_index))

    #calculate the average distance of paths of vehicles
    cost_tot_list_real=[]
    for i in range(num_user):
        if i not in list_bad_path_index:
            for j in path_matrix[i]:
                if j in charging_station:
                    cost_tot_list[i]=cost_tot_list[i]+virtual_distance
            cost_tot_list_real.append(cost_tot_list[i])
    
    if cost_tot_list_real!=[]:
        cost_shortestcharging_average=mean(cost_tot_list_real)
    else:
        cost_shortestcharging_average=inf
    return cost_shortestcharging_average


    # #calculate the remaining battery of each node in the trace 
    # battery_remaining=[[] for z in range(num_user)]
    # for i in range(len(battery_remaining)):
    #     battery_remaining[i].append(energy_initial)
    # print(path_matrix)
    # for i in range(len(path_matrix)):
    #     for j in range (1,len(path_matrix[i])):
    #         if path_matrix[i][j]!=real_charging_station[i][1]:
    #             if battery_remaining[i][-1]>=0:
    #                 #print([path_matrix[i][j-1],path_matrix[i][j]])
    #                 battery_remaining[i].append(battery_remaining[i][-1]-power_consumption(path_matrix[i][j-1],path_matrix[i][j],dic_node,dic_edge))
    #             else:
    #                 break
    #         else:
    #             battery_remaining[i].append(energy_chagingstation)   
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
    #                     num_edge[(path_matrix[i][j],path_matrix[i][j+1])] = 1
    # #print(num_edge)
    # #print('The path of vehicles:',path_matrix)
    # #print('The total length of the path for vehicles:',cost_tot_list)
    # #print('The remaining battery of vehicles at each node:',battery_remaining)
    # #print('The edge parameter:',dic_edge)

    # #plot the trace
    # for i in range(len(path_matrix)):
    #     # print(len(path_matrix[i]))
    #     # print(len(battery_remaining[i]))
    #     if i not in list_bad_path_index:
    #         pyplot.scatter(dic_node[usernodelist[i]][0],dic_node[usernodelist[i]][1],s=100,c=colors[i],marker='*',label='Electric Vehicle')
    #         for j in range(len(path_matrix[i])-1):
    #             pyplot.plot([dic_node[path_matrix[i][j]][0],dic_node[path_matrix[i][j+1]][0]],[dic_node[path_matrix[i][j]][1],dic_node[path_matrix[i][j+1]][1]],lw=num_edge[(path_matrix[i][j],path_matrix[i][j+1])],c=colors[i])
    #         pyplot.scatter (dic_node[path_matrix[i][len(path_matrix[i])-1]][0], dic_node[path_matrix[i][len(path_matrix[i])-1]][1],s=100,c=colors[i],marker='*')
    #     else:
    #         pyplot.scatter(dic_node[usernodelist[i]][0],dic_node[usernodelist[i]][1],s=100,c=colors[i],marker='*',label='Electric Vehicle')
    #         for j in range(len(battery_remaining[i])-1):
    #             if battery_remaining[i][j+1]>=0 and path_matrix[i][j]!=path_matrix[i][j+1]:
    #                 #slope=(dic_node[path_matrix[i][j+1]][1]-dic_node[path_matrix[i][j]][1])/(dic_node[path_matrix[i][j+1]][0]-dic_node[path_matrix[i][j]][0])
    #                 pyplot.plot([dic_node[path_matrix[i][j]][0],dic_node[path_matrix[i][j+1]][0]],[dic_node[path_matrix[i][j]][1],dic_node[path_matrix[i][j+1]][1]],lw=1.5,c=colors[i])
    #             else:
    #                 #slope=(dic_node[path_matrix[i][j]][1]-dic_node[path_matrix[i][j-1]][1])/(dic_node[path_matrix[i][j]][0]-dic_node[path_matrix[i][j-1]][0])
    #                 pyplot.scatter(dic_node[path_matrix[i][j]][0],dic_node[path_matrix[i][j]][1],s=100,c=colors[i],marker='*')

    # pyplot.legend(fontsize=15)
    # pyplot.axis('off')
    # pyplot.show()