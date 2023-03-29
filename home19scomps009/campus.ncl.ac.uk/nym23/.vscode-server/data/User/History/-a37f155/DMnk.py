import sys
sys.path.append("/home/campus.ncl.ac.uk/nym23/usercentricprototype/Lib/site-packages/xlwt")
from main_prototype import main_prototype
import xlwt
import numpy
from matplotlib import pyplot

#The number of users is set as 2,4,...,10
nodeid_numberpathnode=[]
numuser_TotalTime_typical_worst=[]
num_user=4
for i in range(2,num_user+1,2):
    ax,nodeid,number_path_node,TotalTime_typical,TotalTime_worst=main_prototype(i)
    for j in nodeid:
        nodeid_numberpathnode.append([j,number_path_node.get(j,0)])
    numuser_TotalTime_typical_worst.append([i,TotalTime_typical,TotalTime_worst])

#save the data into an excel sheet
book=xlwt.Workbook(encoding='utf-8',style_compression=0)
filename_result='prototyperesultdata'
sheet = book.add_sheet(filename_result,cell_overwrite_ok=True)
#write the headlines
col = ('Node ID','Number of Congestion','Number of users','The Total Expected Time','The Total Worst-case Time')
for i in range(len(col)):
        sheet.write(0,i,col[i])
#write the data
number_line1=1
for i in nodeid_numberpathnode:
        for j in range(0,2):
            sheet.write(number_line1,j,i[j])
        number_line1=number_line1+1
number_line2=1
for i in numuser_TotalTime_typical_worst:
    for j in range(2,5):
        sheet.write(number_line2,j,i[int(j-2)])
savepath = 'D:/Python3.7/user_centric/prototyperesultdata.xls'
book.save(savepath)
print(nodeid_numberpathnode,numuser_TotalTime_typical_worst)

#plot bar graph with congestion data (10 user nodes)
# preliminary
x_data = [i for i in nodeid]
y_data = [number_path_node.get(i,0) for i in nodeid]

#plot a bar graph
ax=pyplot.subplot(132)
for i in range(len(x_data)):
    ax.bar(x_data[i], y_data[i],color="blue")
# set the name of the bar graph
# pyplot.title("The congestion of each node")
# set the lable and range of the x axis
pyplot.xlabel("Node ID")
ax.set_xlim(-1,len(nodeid))
ax.set_xticks(numpy.arange(0,len(nodeid),1))
# set the lable of the y axis
pyplot.ylabel("Congestion")


#plot a line chart
# preliminary
x1_data = [i[0] for i in numuser_TotalTime_typical_worst]
y1_data = [i[1] for i in numuser_TotalTime_typical_worst]
y2_data = [i[2] for i in numuser_TotalTime_typical_worst]

#set the range of x axis
x = range(2,num_user+1,2)
# set the range of y axis
#pyplot.ylim(0.7,0.85) 
ax=pyplot.subplot(133)
ax.plot(x, y1_data, marker='o', mec='r', mfc='w',label='Expected time')
ax.plot(x, y2_data, marker='*', ms=10,label='Worst-case time')
ax.legend()  # enable legend
pyplot.xlabel("Number of user") #Set the label of x axis
ax.set_xticks(numpy.arange(2,num_user+1,2))
pyplot.ylabel("Evacuation time") #Set the label of y axis

# show
pyplot.show()

