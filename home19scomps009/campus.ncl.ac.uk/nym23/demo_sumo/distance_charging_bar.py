import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from shortest1 import shortest
from shortest_trace1 import shortest_trace
from shortestcharging_trace1 import shortestcharging_trace
from adaptive_updated_trace1 import adaptive_updated_trace
#calculate the average of 20 runs 
num_runs=20
num_user=40
num_approaches=3
num_chargingstation_min=5
num_chargingstation_max=165
cost_shortest_average_r_list=[]
cost_shortestcharging_average_r_list=[]
cost_adaptive_average_r_list=[]
for j in range(num_chargingstation_min,num_chargingstation_max+1,20):
    print(j)
    cost_shortest_average_r=0
    cost_shortestcharging_average_r=0
    cost_adaptive_average_r=0
    for i in range(num_runs):
        print(i)
        shortest(num_user,j)
        cost_shortest_average_r=cost_shortest_average_r+shortest_trace(num_user,j)
        cost_shortestcharging_average_r=cost_shortestcharging_average_r+shortestcharging_trace(num_user,j)
        cost_adaptive_average,node_dic=adaptive_updated_trace(num_user,j)
        cost_adaptive_average_r=cost_adaptive_average_r+cost_adaptive_average
    cost_shortest_average_r_list.append(cost_shortest_average_r/num_runs)
    cost_shortestcharging_average_r_list.append(cost_shortestcharging_average_r/num_runs)
    cost_adaptive_average_r_list.append(cost_adaptive_average_r/num_runs)
cost_three_average_r_list=[]
cost_three_average_r_list.append(cost_shortest_average_r_list)
cost_three_average_r_list.append(cost_shortestcharging_average_r_list)
cost_three_average_r_list.append(cost_adaptive_average_r_list)
#convert the list into array
cost_three_average_r_array=np.array(cost_three_average_r_list)
print(cost_three_average_r_array)
# plot the 3D bar graph
fig = plt.figure()
ax = fig.gca(projection='3d')
#set x axis
cost_three_average_list_x=[i for i in range(num_chargingstation_min,num_chargingstation_max+1,20)]
X=np.array(cost_three_average_list_x)
#set y axis
labels=['SSP','SSP-NN','Our Approach']
cost_three_average_list_y=[i for i in range(len(labels))]
Y=np.array(cost_three_average_list_y)
Z=cost_three_average_r_array
colors=['#72A6FF','#FFAF80','#832700']
color_list = []
for i in range(len(Y)):
    c = colors[i]
    color_list.append([c] * len(X))
color_array = np.asarray(color_list)
label_list = []
for i in range(len(Y)):
    l = labels[i]
    label_list.append([l] * len(X))
label_array = np.asarray(label_list)
xx, yy = np.meshgrid(X, Y)  # 网格化坐标
xx_flat, yy_flat,zz_flat,color_array_flat,label_array_flat= xx.ravel(), yy.ravel(), Z.ravel(),color_array.ravel(),label_array.ravel()  # 矩阵扁平
height=np.zeros_like(xx_flat)
width=0.45
depth=0.15
sc_list=[]
for i in range(len(xx_flat)):
    if i==0 or i==len(X) or i==int(len(X)*2):
        sc=ax.bar3d(xx_flat[i],yy_flat[i],height[i],width,depth,zz_flat[i],color=color_array_flat[i],label=label_array_flat[i],shade=False)
        sc_list.append(sc)
    else:
        sc=ax.bar3d(xx_flat[i],yy_flat[i],height[i],width,depth,zz_flat[i],color=color_array_flat[i],shade=False)
        sc_list.append(sc)
#set the parameter about axis
ax.set_xlabel('Number of Charging Stations')
ax.set_ylabel('Path Planning Approach')
ax.set_zlabel('Path Length')
#ax.set_xticks(list(range(len(cost_three_average_list_x))))
x_tickets=[i for i in range(num_chargingstation_min-1,num_chargingstation_max+3,20)]
ax.set_xticklabels(x_tickets)
ax.set_yticks(list(range(len(Y))))
y_tickets=[i for i in labels]
ax.set_yticklabels(y_tickets)
for i in sc_list:
    i._facecolors2d = i._facecolors3d
    i._edgecolors2d = i._edgecolors3d
plt.legend(fontsize=13)
plt.show()