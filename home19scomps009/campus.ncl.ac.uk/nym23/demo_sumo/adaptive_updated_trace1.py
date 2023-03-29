import pandas as pd
import math
from matplotlib import pyplot
from initialize import initialize
from relax import relax
from matplotlib.patches import Circle
from distanceg import distance
from power_consumption import power_consumption
import xlrd
from numpy import *
file_namenode='plain.nod'
file_nameedge='plain.edg'
file_pathnode=r'/home/campus.ncl.ac.uk/nym23/demo_sumo'+'//'+file_namenode+'.csv'
file_pathedge=r'/home/campus.ncl.ac.uk/nym23/demo_sumo'+'//'+file_nameedge+'.csv'

def adaptive_updated_trace(num_user,num_chargingstation):
    #color settings
    color_edge='#525353'
    color_node='#494949'
    colors=["#EAA813","#CB1313"]
    linewidth=[3.5,1.5]

    #read node data
    #read node id
    node_id=pd.read_csv(file_pathnode,sep=';',header=1,usecols=[5])
    nodeid=[]
    nodelist=node_id.values.tolist()
    #print(nodelist)
    for i in nodelist:
        nodeid.append(i[0])
    #print(nodeid)
    #read node x coordinate
    node_x=pd.read_csv(file_pathnode,sep=';',header=1,usecols=[7])
    nodex=[]
    node_x_list=node_x.values.tolist()
    for i in node_x_list:
        # if math.isnan(i[0]):
        #     continue
        nodex.append(i[0])
    #read node y coordinate
    node_y=pd.read_csv(file_pathnode,sep=';',header=1,usecols=[8])
    nodey=[]
    node_y_list=node_y.values.tolist()
    for i in node_y_list:
        # if math.isnan(i[0]):
        #     continue
        nodey.append(i[0])
    # #plot node
    # for i in range(len(nodeid)):
    #     pyplot.scatter (nodex[i],nodey[i],s=0,c=color_node)
    #     #pyplot.annotate(nodeid[i],(nodex[i],nodey[i]),(nodex[i]-0.03,nodey[i]+0.1) )
    #store node id and coordinate in a dictionary
    node_dic={}
    for i in range (len(nodeid)):
        node_dic[nodeid[i]]=[nodex[i],nodey[i]]
    #print(node_dic)

    #read edge data
    #read the origin of the edge
    edge_id=pd.read_csv(file_pathedge,sep=';',header='infer',usecols=[3])
    edgeid=[]
    edgeidlist=edge_id.values.tolist()
    for i in edgeidlist:
        edgeid.append(i[0])
    #read the origin of the edge
    edge_from_id=pd.read_csv(file_pathedge,sep=';',header='infer',usecols=[2])
    edgefromid=[]
    edgefromlist=edge_from_id.values.tolist()
    for i in edgefromlist:
        edgefromid.append(i[0])
    #read the destination of the edge
    edge_to_id=pd.read_csv(file_pathedge,sep=';',header='infer',usecols=[8])
    edgetoid=[]
    edgetolist=edge_to_id.values.tolist()
    for i in edgetolist:
        edgetoid.append(i[0])
    #read the speed of the edge 
    edge_speed=pd.read_csv(file_pathedge,sep=';',header='infer',usecols=[7])
    edgespeed=[]
    edgespeedlist=edge_speed.values.tolist()
    for i in edgespeedlist:
        edgespeed.append(i[0])
    #read the type of the edge 
    edge_type=pd.read_csv(file_pathedge,sep=';',header='infer',usecols=[9])
    edgetype=[]
    edgetypelist=edge_type.values.tolist()
    for i in edgetypelist:
        edgetype.append(str(i[0]))
    #store edge id and the relative information in a dictionary
    edge_dic={}
    for i in range (len(edgeid)):
        edge_dic[edgeid[i]]=[edgefromid[i],edgetoid[i],edgetype[i],edgespeed[i]]
    #print(edge_dic)

    #calculate the parameter of each edge
    #calculate the distance of each edge
    for i in edge_dic:
        distance_edge=distance(node_dic[edge_dic[i][0]][0], node_dic[edge_dic[i][1]][0],node_dic[edge_dic[i][0]][1],node_dic[edge_dic[i][1]][1])
        edge_dic[i].append(distance_edge)
    #print(consumption_delay)
    #calculate the power consumption of each edge
    for i in edge_dic:
        power_edge=power_consumption(edge_dic[i][0],edge_dic[i][1],node_dic,edge_dic)
        edge_dic[i].append(power_edge)
    #print(consumption_power)
    #store the edge including the origin and destination and parameter of an edge into a list 
    edge=[]
    for i in edge_dic:
        edge.append([edge_dic[i][0],edge_dic[i][1],edge_dic[i][4],edge_dic[i][5]])
    #set the edge bidirectional
    for i in edge_dic:
        edge.append([edge_dic[i][1],edge_dic[i][0],edge_dic[i][4],edge_dic[i][5]])
    #print(edge)
    #store information on the edge in a dictionary 
    edge_dic_r={}
    for i in edge:
        edge_dic_r[(i[0],i[1])]=[i[2],i[3]]

    # #plot edge
    # #print(edge_dic_r)
    # for i in edge_dic:
    # pyplot.plot([node_dic[edge_dic[i][0]][0],node_dic[edge_dic[i][1]][0]],[node_dic[edge_dic[i][0]][1],node_dic[edge_dic[i][1]][1]],c=color_edge,lw=1,linestyle=':')
    # #pyplot.annotate((edge_dic_r[(edge_dic[i][0],edge_dic[i][1])][0],edge_dic_r[(edge_dic[i][0],edge_dic[i][1])][1]),xy=(node_dic[edge_dic[i][0]][0],node_dic[edge_dic[i][0]][1]),xytext=((node_dic[edge_dic[i][0]][0]+node_dic[edge_dic[i][1]][0])/2-0.2,(node_dic[edge_dic[i][0]][1]+node_dic[edge_dic[i][1]][1])/2+0.05),weight='bold',color='r' )

    #set exit node
    num_exit=1
    exitnodeid=['436933812']
    # #plot exit node
    # for i in exitnodeid:
    #     pyplot.scatter (node_dic[i][0],node_dic[i][1],s=60,c='g',marker='s',label='Destination')
    # #print(exitnodeid)

    #set user node
    #read the data on vehicle node saved in the excel
    file_name = xlrd.open_workbook('/home/campus.ncl.ac.uk/nym23/demo_sumo/distance_charging_bar.xls')#得到文件
    table =file_name.sheets()[0]#得到sheet页
    nrows = table.nrows #总行数
    ncols = table.ncols #总列数
    Power_max=35000
    Power_initial=35000
    usernode=[]
    line_user = 1
    usernodelist=[]
    usernode_index=[]
    while line_user  < num_user+1:
        cell=table.row_values(line_user )[1] #得到users数据
        #ctype = table.cell(i,2).ctype #得到worst-case evacuation time数据的格式
        usernodelist.append(cell)
        line_user =line_user +1
    userpowerlist=[]
    for i in range(num_user):
        userpowerlist.append(Power_initial)
    for i in range(num_user):
        usernode.append([usernodelist[i],userpowerlist[i]])
    # #plot vehicle
    # for i in usernode:
    #     pyplot.scatter(node_dic[i[0]][0],node_dic[i[0]][1],s=40,c='c',marker='*')

    # set charging station
    line_charging=1
    chargingnode=[]
    while line_charging< num_chargingstation+1:
        cell=table.row_values(line_charging)[0] #得到users数据
        #ctype = table.cell(i,2).ctype #得到worst-case evacuation time数据的格式
        chargingnode.append(cell)
        line_charging=line_charging+1
    #print(chargingnode)
    # #plot charging station
    # for i in range(len(chargingnode)-1):
    #     pyplot.scatter(node_dic[chargingnode[i]][0],node_dic[chargingnode[i]][1],s=40,c='b',marker='^')
    # for i in range(len(chargingnode)-1,len(chargingnode)):
    #     pyplot.scatter(node_dic[chargingnode[i]][0],node_dic[chargingnode[i]][1],s=40,c='b',marker='^',label='Charging Station')


    #add the loop at the charging station
    fig= pyplot.gcf()
    ax= fig.gca()
    virtual_distance=15*13.89*60
    for i in chargingnode:
        edge.append([i,i,virtual_distance,-Power_max])
        edge_dic_r[(i,i)]=[virtual_distance,-Power_max]
        #pyplot.annotate((virtual_distance,-Power_max),xy=(node_dic[i][0],node_dic[i][1]),xytext=((node_dic[i][0]+node_dic[i][0])/2-0.2,(node_dic[i][1]+node_dic[i][1])/2+0.45),weight='bold',color='g' )
        # circle = Circle(xy=(node_dic[i][0], node_dic[i][1]+0.2), radius=0.2, alpha=1, color='black',fill=False)
        # ax.add_artist(circle)
    edge=edge[::-1]
    #print(edge)

    #Initialize
    lookup_table=initialize(nodeid,exitnodeid)
    #print(lookup_table)

    #relax
    num_iteration=int((len(nodeid)-1+num_chargingstation)*2)
    #print(num_iteration)
    for i in range(num_iteration):
        #print('this is the number of iterations{}'.format(i))
        for e in edge:
            #print('this is the edge relaxed{}'.format(e))
            relax(e,lookup_table,Power_max,chargingnode)
    #print("This is the lookup table at each vertex:{}".format(lookup_table))

    #calculate the path for the vehicle
    #repetition deletion
    lookup_table_r=[]
    for i in nodeid: 
        for j in lookup_table[i]:
            if j not in lookup_table_r:
                lookup_table_r.append(j)
        lookup_table[i]=lookup_table_r
        lookup_table_r=[]   
    #print(lookup_table_r)

    #calculate the path consisting of a sequence of vertexes 
    path_list=[[] for i in range(num_user)]
    for i in range(num_user):
        path_list[i].append(usernode[i])
    for i in lookup_table:
        lookup_table[i].sort(key=lambda x:x[2])
    #print("The sorted lookup table at each vertesx is:{}".format(lookup_table) )
    #print("The starting point and initial energy are:{}".format(path_list))
    #print("The destination node:{}".format(exitnodeid))

    #utilize the lookup tables to select the optimal path
    list_bad_path_index=[]
    inf=99999999
    for i in range(num_user):
        while path_list[i][-1][0]!=exitnodeid[0]:
            path_distance_ini=inf
            flag_len=len(path_list[i])
            for j in lookup_table[path_list[i][-1][0]]:
                if path_list[i][-1][1]>=j[0] and j[2]<path_distance_ini:
                    if path_list[i][-1][0]!=j[1]:
                        path_list[i].append([j[1],path_list[i][-1][1]-edge_dic_r[(path_list[i][-1][0],j[1])][1]])
                        path_distance_ini=j[2]
                        #print("This is the path for the vehicle:{}".format(path_list[i]))
                    else:
                        path_list[i].append([j[1],Power_max])
                        path_distance_ini=j[2] 
            if len(path_list[i])==flag_len:
                list_bad_path_index.append(usernodelist[i])
                break
    #print(list_bad_path_index)
    print('The number of vehicles running out of electricity for our approach:',len(list_bad_path_index))
    #print("The waypoint and the energy for the vehicle are:{}".format(path_list))

    #calculate the average distance of the paths of vehicles
    cost_tot_list=[]
    cost_tot=0
    for i in range(num_user):
        if usernodelist[i] not in list_bad_path_index:
            for j in range(len(path_list[i])-1):
                cost_tot=cost_tot+distance(node_dic[path_list[i][j][0]][0],node_dic[path_list[i][j+1][0]][0],node_dic[path_list[i][j][0]][1],node_dic[path_list[i][j+1][0]][1])
            cost_tot_list.append(cost_tot)
    if cost_tot_list!=[]:
        cost_adaptive_average=mean(cost_tot_list)
    else:
        cost_adaptive_average=inf
    return cost_adaptive_average,node_dic

    # #plot the path of the vehicle and calculate the total distance from the source to the destination
    # #calculate the number of edges traversed by vehicles
    # num_edge={}
    # for i in range(len(path_list)):
    #     for j in range(len(path_list[i])-1):
    #         if (path_list[i][j][0],path_list[i][j+1][0]) in num_edge.keys():
    #             num_edge[(path_list[i][j][0],path_list[i][j+1][0])]+=1
    #         else:
    #             num_edge[(path_list[i][j][0],path_list[i][j+1][0])]=1
    # #print(num_edge)

    # #plot
    # tot_cost=[]
    # for j in range(num_user):
    #     if usernodelist[j] not in list_bad_path_index:
    #         pyplot.scatter(node_dic[usernodelist[j]][0],node_dic[usernodelist[j]][1],s=100,c=colors[j],marker='*',label='Electric Vehicle')
    #         tot_cost_value=0
    #         for i in range(len(path_list[j])-1):
    #             pyplot.plot([node_dic[path_list[j][i][0]][0],node_dic[path_list[j][i+1][0]][0]],[node_dic[path_list[j][i][0]][1],node_dic[path_list[j][i+1][0]][1]],lw=linewidth[j],c=colors[j])
    #             tot_cost_value=tot_cost_value+edge_dic_r[(path_list[j][i][0],path_list[j][i+1][0])][0]
    #         tot_cost.append(tot_cost_value)
    #         pyplot.scatter (node_dic[path_list[j][len(path_list[j])-1][0]][0], node_dic[path_list[j][len(path_list[j])-1][0]][1],s=100,c=colors[j],marker='*')
    #     else:
    #         pyplot.scatter(node_dic[usernodelist[j]][0],node_dic[usernodelist[j]][1],s=100,c=colors[j],marker='*',label='Electric Vehicle')
    #         for i in range(len(path_list[j])-1):
    #             pyplot.plot([node_dic[path_list[j][i][0]][0],node_dic[path_list[j][i+1][0]][0]],[node_dic[path_list[j][i][0]][1],node_dic[path_list[j][i+1][0]][1]],lw=1.5,c=colors[j]) 
    #         pyplot.scatter(node_dic[path_list[j][i][0]][0],node_dic[path_list[j][i][0]][1],s=100,c=colors[j],marker='*')
    # print("This is the total distance of the path:{}".format(tot_cost))
    # pyplot.legend(fontsize=15)
    # pyplot.axis('off')
    # pyplot.show()
