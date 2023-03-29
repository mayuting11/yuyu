from copy import copy
from sort_lookuptable import sort_result1
from sort_centric import  sort_result2
import copy
def evacuation_time_total(look_up_table_user_opt,count_user,node_capacity_list):
    look_up_table_user_opt_sorted_r=[]
    count_add=0
    while count_user!=0:
        for i in look_up_table_user_opt:
            i[1].sort(key=sort_result1)
        look_up_table_user_opt_sorted =sorted(look_up_table_user_opt,key=sort_result2)
        #print(look_up_table_user_opt_sorted)
        look_up_table_user_opt_sorted_r.append([copy.deepcopy(look_up_table_user_opt_sorted[count_add][0]),copy.deepcopy(look_up_table_user_opt_sorted[count_add][1][0])])
        for i in range(len(look_up_table_user_opt_sorted)-1):
            for j in look_up_table_user_opt_sorted[i+1][1]:
                for p in j[1][0]:
                    for k in look_up_table_user_opt_sorted[i::-1]:
                        if p in k[1][0][1][0]:
                            node_index_rea=j[1][0].index(p)
                            node_index_dep=k[1][0][1][0].index(p)
                            if j[1][1][node_index_rea]<k[1][0][1][3][node_index_dep] and count_add+2>node_capacity_list[int(p)]:
                                waiting_extra_typical=k[1][0][1][3][node_index_dep]-j[1][1][node_index_rea]
                                for l in j[1][3][node_index_rea:]:
                                    l=l+waiting_extra_typical
                                for m in j[1][1][node_index_rea+1:]:
                                    m=m+waiting_extra_typical
                                j[2]=j[2]+waiting_extra_typical
                            if j[1][2][node_index_rea]<k[1][0][1][4][node_index_dep] and count_add+2>node_capacity_list[int(p)]:
                                waiting_extra_worst=k[1][0][1][4][node_index_dep]-j[1][2][node_index_rea]
                                for n in j[1][4][node_index_rea:]:
                                    n=n+waiting_extra_worst
                                for o in j[1][2][node_index_rea+1:]:
                                    o=o+waiting_extra_worst
                                j[0]=j[0]+waiting_extra_worst
                            break
        count_user=count_user-1
        if count_add!=0:
            look_up_table_user_opt_sorted_r.append([copy.deepcopy(look_up_table_user_opt_sorted[count_add][0]),copy.deepcopy(look_up_table_user_opt_sorted[count_add][1][0])])
        count_add=count_add+1
        #look_up_table_user_opt_r_sorted_list=dict(look_up_table_user_opt_r_sorted_list)
    return look_up_table_user_opt_sorted_r,look_up_table_user_opt_sorted_r[-1][1][0]