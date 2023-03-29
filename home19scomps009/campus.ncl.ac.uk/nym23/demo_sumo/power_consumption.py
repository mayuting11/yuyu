import math
def power_consumption(node_start,node_end,node_dic,edge_dic):
    dis=100*math.sqrt(pow((float(node_dic[node_start][0])-float(node_dic[node_end][0])),2)+pow((float(node_dic[node_start][1])-float(node_dic[node_end][1])),2))
    for i in edge_dic:
        if (edge_dic[i][0]==node_start and edge_dic[i][1]==node_end) or (edge_dic[i][0]==node_end and edge_dic[i][1]==node_start):
            #print(node_start,node_end,edge_dic[i])
            v=float(edge_dic[i][3])*3600/1000
            #print(edge_dic[i])
            if 'highway.primary' in edge_dic[i][2]:
                power=(5.492/v+0.004*v-0.179)*(dis/1000)*1000
            elif 'highway.secondary' in edge_dic[i][2]:
                power=(1.531/v-0.001*v+0.21)*(dis/1000)*1000
            else:
                power=(1.553/v-0.002*v+0.208)*(dis/1000)*1000
    return power