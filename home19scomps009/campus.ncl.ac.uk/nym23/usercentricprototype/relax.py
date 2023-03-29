def relax(e,lookup_table,deadline):
    minworstbound=88888888888
    if lookup_table[e[1]]==[]:
        return
    else:
        # if parents[e[1]][exitnode]!=exitnode:
        #         parents[e[0]][exitnode]=parents[e[1]][exitnode]
        for i in lookup_table[e[1]]:
            if e[2]+i[0]< minworstbound:
                minworstbound=e[2]+i[0]
        for i in lookup_table[e[1]]:
            worstbound=max(e[2]+i[0],minworstbound)
            typicalbound=e[3]+i[2]
            if worstbound<=deadline:
                lookup_table[e[0]].append([worstbound,e[1],typicalbound])




