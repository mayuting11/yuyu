import copy
def relax_updated(e,lookup_table,Power_max,chargingnode):
    '''
    This function aims to relax the edge 'e'. The logic is as follows: search the lookup_table in the latter node of the edge 'e', 
    calculate the power and length, and then compare the power and length with the lookup_table in the former node of the edge'e' 
    to determine whether the power and length should be inserted into the lookup_table in the former node of the edge 'e'.
    '''
    tmp = copy.deepcopy(lookup_table[e[1]])
    for i in tmp:
        power=e[3]+i
        path_distance=e[2]+lookup_table[e[1]][i][1]
        if power>=0 and power<=Power_max:
            if power in lookup_table[e[0]].keys():
                if path_distance<lookup_table[e[0]][power][1]:
                    lookup_table[e[0]][power][1]=path_distance
            else:
                lookup_table[e[0]][power]=[e[1],path_distance]
        elif power<0 and power>=-Power_max:
            power=0
            if power in lookup_table[e[0]].keys():
                if path_distance<lookup_table[e[0]][power][1]:
                    lookup_table[e[0]][power][1]=path_distance
            else:
                lookup_table[e[0]][power]=[e[1],path_distance]
    

