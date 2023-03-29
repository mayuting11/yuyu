import pandas as pd
import math
from matplotlib import pyplot
from initialize import initialize
from relax import relax
from matplotlib.patches import Circle
file_name='demo'
file_path=r'/home/campus.ncl.ac.uk/nym23/demo_sumo'+'//'+file_name+'.xlsx'
#from get_key import get_key

#read node data
#read node id
node_id=pd.read_excel(file_path,names=None,usecols=[0])
nodeid=[]
nodelist=node_id.values.tolist()
for i in nodelist:
    if math.isnan(i[0]):
        continue
    nodeid.append(i[0])
#read node x coordinate
node_x=pd.read_excel(file_path,names=None,usecols=[1])
nodex=[]
node_x_list=node_x.values.tolist()
for i in node_x_list:
    if math.isnan(i[0]):
        continue
    nodex.append(i[0])
#read node y coordinate
node_y=pd.read_excel(file_path,names=None,usecols=[2])
nodey=[]
node_y_list=node_y.values.tolist()
for i in node_y_list:
    if math.isnan(i[0]):
        continue
    nodey.append(i[0])
#plot node
for i in range(len(nodeid)):
    pyplot.scatter (nodex[i],nodey[i],s=20,c='k')
    pyplot.annotate(str(i),(nodex[i],nodey[i]),(nodex[i]-0.03,nodey[i]+0.1) )
#store node id and coordinate in a dictionary
node_dic={}
for i in range (len(nodeid)):
     node_dic[i]=[nodex[i],nodey[i]]

#read edge data
#read the origine of the edge
edge_from_id=pd.read_excel(file_path,names=None,usecols=[3])
edgefromid=[]
edgefromlist=edge_from_id.values.tolist()
for i in edgefromlist:
    edgefromid.append(i[0])
#read the destination of the edge
edge_to_id=pd.read_excel(file_path,names=None,usecols=[4])
edgetoid=[]
edgetolist=edge_to_id.values.tolist()
for i in edgetolist:
     edgetoid.append(i[0])
#read the parameter of each edge
#read the power consumption of each edge
powerconsumption=pd.read_excel(file_path,names=None,usecols=[7])
consumption_power=[]
powerconsumptionlist=powerconsumption.values.tolist()
for i in powerconsumptionlist:
    if math.isnan(i[0]):
        continue
    consumption_power.append(i[0])
#read the distance of each edge
delayconsumption=pd.read_excel(file_path,names=None,usecols=[5])
consumption_delay=[]
delayconsumptionlist=delayconsumption.values.tolist()
for i in delayconsumptionlist:
    if math.isnan(i[0]):
        continue
    consumption_delay.append(i[0])
#store the edge including the origin and destination and parameter of an edge into a list 
edge=[]
for i in range(len(edge_from_id)):
    edge.append([edgefromid[i],edgetoid[i],consumption_power[i],consumption_delay[i]])
pyplot.xlim(-1,8)
pyplot.ylim(-1,6)
#store information on the edge in a dictionary 
edge_dic={}
for i in edge:
    edge_dic[(i[0],i[1])]=[i[2],i[3]]
#plot edge
for i in range(len(edgefromid)):
   pyplot.plot([nodex[edgefromid[i]],nodex[edgetoid[i]]],[nodey[edgefromid[i]],nodey[edgetoid[i]]],c='k')
   pyplot.annotate((edge_dic[(edgefromid[i],edgetoid[i])][0],edge_dic[(edgefromid[i],edgetoid[i])][1]),xy=(nodex[edgefromid[i]],nodey[edgefromid[i]]),xytext=((nodex[edgefromid[i]]+nodex[edgetoid[i]])/2-0.2,(nodey[edgefromid[i]]+nodey[edgetoid[i]])/2+0.05),weight='bold',color='r' )

#read exit node
exit_node_id=pd.read_excel(file_path,names=None,usecols=[8])
exitnodeid=[]
exitnodelist=exit_node_id.values.tolist()
for i in exitnodelist:
    if math.isnan(i[0]):
        continue
    exitnodeid.append(i[0])
#plot exit node
for i in exitnodeid:
    pyplot.scatter (node_dic[int(i)][0],node_dic[int(i)][1],s=40,c='g')
num_exit=len(exitnodeid)
#print(exitnodeid)

# read vehicle
#read vehicle location and initial power
user_node_id=pd.read_excel(file_path,names=None,usecols=[9])
user_node_power=pd.read_excel(file_path,names=None,usecols=[10])
usernode=[]
usernodelist=user_node_id.values.tolist()
userpowerlist=user_node_power.values.tolist()
for i in range(len(usernodelist)):
    if math.isnan(usernodelist[i][0]):
        continue
    usernode.append([usernodelist[i][0],userpowerlist[i][0]])
#plot vehicle
for i in usernode:
    pyplot.scatter (node_dic[int(i[0])][0],node_dic[int(i[0])][1],s=40,c='y')
num_user=len(usernode)

# read charging station
charging_node_id=pd.read_excel(file_path,names=None,usecols=[6])
chargingnode=[]
chargingnodelist=charging_node_id.values.tolist()
for i in chargingnodelist:
    if math.isnan(i[0]):
        continue
    chargingnode.append(i[0])
#plot charging station
for i in chargingnode:
    pyplot.scatter (node_dic[int(i)][0],node_dic[int(i)][1],s=40,c='r')
num_chargingstation=len(chargingnode)
#add the loop at the charging station
fig = pyplot.gcf()
ax = fig.gca()
for i in chargingnode:
    edge.append([i,i,-5,0.8])
    edge_dic[(i,i)]=[-5,0.8]
    pyplot.annotate((-5,0.8),xy=(nodex[int(i)],nodey[int(i)]),xytext=((nodex[int(i)]+nodex[int(i)])/2-0.2,(nodey[int(i)]+nodey[int(i)])/2+0.45),weight='bold',color='g' )
    circle = Circle(xy=(nodex[int(i)], nodey[int(i)]+0.2), radius=0.2, alpha=1, color='black',fill=False)
    ax.add_artist(circle)
edge=edge[::-1]
# set the initial power of the vehicle
Power_max=5

#Initialize
lookup_table=initialize(nodeid,exitnodeid)
#print(lookup_table)

#relax
for i in range (int((len(nodeid)-1+num_chargingstation)*2)):
    for e in edge:
        relax(e,lookup_table,Power_max,chargingnode)
#print("This is the lookup table at each vertex:{}".format(lookup_table))

#calculate the path for the vehicle
#repetition delition
lookup_table_r=[]
for i in nodeid: 
    for j in lookup_table[i]:
        if j not in lookup_table_r:
            lookup_table_r.append(j)
    lookup_table[i]=lookup_table_r
    lookup_table_r=[]   
                    
#calculate the path consisting of a sequence of vertexes 
path_list=[]
Power_initial=5
path_list.append([usernode[0][0],Power_initial])
for i in lookup_table:
    lookup_table[i].sort(key=lambda x:x[2])
print("The sorted lookup table at each vertesx is:{}".format(lookup_table) )
print("The source and initial energy are:{}".format(path_list))
print("The destination node:{}".format(exitnodeid))

#utilize the lookup tables to select the optimal path
while int(path_list[-1][0])!=int(exitnodeid[0]):
    path_distance_ini=88888888
    for j in lookup_table[path_list[-1][0]]:
        if path_list[-1][0]!=j[1] or (path_list[-1][0]==j[1] and type(path_list[-1][0])!=type(j[1])):
            if path_list[-1][1]>=j[0] and j[2]<path_distance_ini:
                if int(j[1])!=int(path_list[-1][0]):
                    path_list.append([j[1],path_list[-1][1]-edge_dic[(path_list[-1][0],j[1])][0]])
                    path_distance_ini=j[2]
                    #print("This is the path for the vehicle:{}".format(path_list))
                else:
                    path_list.append([j[1],Power_max])
                    path_distance_ini=j[2]
print("The waypoint and the energy for the vehicle are:{}".format(path_list))

#plot the path of the vehicle and calculate the total distance from the source to the destination
tot_cost=0
for i in range(len(path_list)-1):
    pyplot.plot([nodex[int(path_list[i][0])],nodex[int(path_list[i+1][0])]],[nodey[int(path_list[i][0])],nodey[int(path_list[i+1][0])]],c='yellow')
    tot_cost=tot_cost+edge_dic[(path_list[i][0],path_list[i+1][0])][1]
print("This is the total distance of the path:{}".format(tot_cost))
pyplot.show()
