def relax(e,lookup_table,Power_max,chargingnode):
    '''
    This function aims to relax the edge 'e'. The logic is as follows: search the lookup_table in the latter node of the edge 'e', 
    calculate the power and length, and then compare the power and length with the lookup_table in the former node of the edge'e' 
    to determine whether the power and length should be inserted into the lookup_table in the former node of the edge 'e'.
    '''
    if lookup_table[e[1]]==[]:
        return
        #print('no tables generating')
    else:
        for i in lookup_table[e[1]]:
            power=e[3]+i[0]
            path_distance=e[2]+i[2]
            insert=True
            if power>=0 and power<=Power_max:
                if lookup_table[e[0]]!=[]:
                    for j in lookup_table[e[0]]:
                        if j[0]>=power and j[2]>=path_distance:
                            lookup_table[e[0]].remove(j)
                        elif j[0]<=power and j[2]<=path_distance:
                            insert=False
                            break
                        else:
                            insert=True
            elif power<0 and power>=-Power_max:
                power=0
                if lookup_table[e[0]]!=[]:
                    for j in lookup_table[e[0]]:
                        if j[0]>=power and j[2]>=path_distance:
                            lookup_table[e[0]].remove(j)
                        elif j[0]<=power and j[2]<=path_distance:
                            insert=False
                            break
                        else:
                            insert=True
            else:
                insert=False
            if insert==True:
                lookup_table[e[0]].append([power,e[1],path_distance])
            #print('The lookup table at {} is {}'.format(e[0],lookup_table[e[0]]))
        

