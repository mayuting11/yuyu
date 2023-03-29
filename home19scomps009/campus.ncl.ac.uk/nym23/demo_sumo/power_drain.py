import math
def power_drain(edge_dic,node_dic):
    node_dic_r={}
    for i in node_dic:
        node_dic_r[i]=[''.join(str(j) for j in node_dic[str(i)])]
    for i in edge_dic:
        dis=100*math.sqrt(pow((float(node_dic[edge_dic[i][0]][0])-float(node_dic[edge_dic[i][1]][0])),2)+pow((float(node_dic[edge_dic[i][0]][1])-float(node_dic[edge_dic[i][1]][1])),2))
        v=float(edge_dic[i][3])*3600/1000
        if 'highway.primary' in edge_dic[i][2]:
            power=(5.492/v+0.004*v-0.179)*(dis/1000)*1000
        elif 'highway.secondary' in edge_dic[i][2]:
            power=(1.531/v-0.001*v+0.21)*(dis/1000)*1000
        else:
            power=(1.553/v-0.002*v+0.208)*(dis/1000)*1000
        edge_dic[i].append(power)
    return edge_dic