import copy
from sort_centric import sort_result2
def evacuation_time(look_up_table_user_r,usernode,edge_dic):
    inf=88888888
    look_up_table_user_opt=[]
   #calculate how many users are there at each user node
    user_loc_num = {}
    for key in usernode:
        user_loc_num[key] = user_loc_num.get(key,0) + 1
    
   #储存每个用户到达每个点的typical time和worst-case time以及minimum capacity和对应的node
    for i in look_up_table_user_r:
        for j in look_up_table_user_r[i]:
            j[1].append([])
            j[1].append([])
            j[1].append([])
            j[1].append([])

    for i in usernode:
        look_up_table_user_opt.append([int(i),copy.deepcopy(look_up_table_user_r[i])])
        #print(i)
   #sort the users according to the typical evacuation time
    look_up_table_user_opt.sort(key=sort_result2)

    #reserve the arrival time and departure time of each user at each node  
        #reserve the arrrival time and departure time of each user at the initial node
    for i in look_up_table_user_opt:
        for j in i[1]:
            evacuation_time_typical_node_rea=0
            evacuation_time_worst_node_rea=0
            evacuation_time_typical_node_dep=0
            evacuation_time_worst_node_dep=0
            j[1][1].append(evacuation_time_typical_node_rea)
            j[1][2].append(evacuation_time_worst_node_rea)
            j[1][3].append(evacuation_time_typical_node_dep)
            j[1][4].append(evacuation_time_worst_node_dep)
        #reserve the arrival time and departure time of each node at subsequent nodes
            for l in range(len(j[1][0])-1):
                if int(j[1][0][l+1])!=int(j[1][0][l]):
                    evacuation_time_typical_node_rea=j[1][1][-1]+edge_dic[(int(j[1][0][l]),int(j[1][0][l+1]))][1]
                    evacuation_time_worst_node_rea=j[1][2][-1]+edge_dic[(int(j[1][0][l]),int(j[1][0][l+1]))][0]
                    evacuation_time_typical_node_dep=j[1][3][-1]+edge_dic[(int(j[1][0][l]),int(j[1][0][l+1]))][1]
                    evacuation_time_worst_node_dep=j[1][4][-1]+edge_dic[(int(j[1][0][l]),int(j[1][0][l+1]))][0]
                    j[1][1].append(evacuation_time_typical_node_rea)
                    j[1][2].append(evacuation_time_worst_node_rea)
                    j[1][3].append(evacuation_time_typical_node_dep)
                    j[1][4].append(evacuation_time_worst_node_dep)
    return user_loc_num,look_up_table_user_opt