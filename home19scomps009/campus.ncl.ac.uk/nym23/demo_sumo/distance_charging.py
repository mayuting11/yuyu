from matplotlib import pyplot
from shortest import shortest
from shortest_trace import shortest_trace
from shortestcharging_trace import shortestcharging_trace
from adaptive_updated_trace import adaptive_updated_trace
from mpl_toolkits.mplot3d import Axes3D
from numpy import *
import numpy
import seaborn as sb

num_user=40
num_chargingstation_min=5
num_chargingstation_max=165
cost_shortest_average_list=[]
cost_shortest_charging_average_list=[]
cost_adaptive_average_list=[]
num_approaches=3
for i in range(num_chargingstation_min,num_chargingstation_max+1):
    print(i)
    shortest(num_user,i)
    cost_shortest_average_list.append(shortest_trace(num_user,i))
    cost_shortest_charging_average_list.append(shortestcharging_trace(num_user,i))
    cost_adaptive_average,node_dic=adaptive_updated_trace(num_user,i)
    cost_adaptive_average_list.append(cost_adaptive_average)
cost_three_average_list=[]
cost_three_average_list.append(cost_shortest_average_list)
cost_three_average_list.append(cost_shortest_charging_average_list)
cost_three_average_list.append(cost_adaptive_average_list)
cost_three_average_list_x=[i for i in range(num_chargingstation_min,num_chargingstation_max+1)]

# plot the scatter diagram
colors=['#00C7FA','#111718','#FFA857']
labels=['SPP','SPP-NN','Our Approach']
markers=['+','*','.']
pyplot.xlabel("Number of Charging Stations",fontsize=20)
pyplot.ylabel("Path Length",fontsize=20)
my_x_ticks = numpy.arange(5,num_chargingstation_max+1,20)
pyplot.xticks(my_x_ticks)
for i in range(num_approaches):
    #pyplot.scatter(cost_three_average_list_x,cost_three_average_list[i],c=colors[i],label=labels[i],marker=markers[i],s=sizes[i],alpha=transparency[i])
    sb.regplot(cost_three_average_list_x,cost_three_average_list[i],fit_reg=False,x_jitter = 0.2,y_jitter = 0.2,label=labels[i],color=colors[i],marker=markers[i])
pyplot.legend(loc=2, bbox_to_anchor=(1.05,1.0), borderaxespad = 0.,fontsize=20)
pyplot.grid(ls='--', linewidth=0.3)
pyplot.show()

