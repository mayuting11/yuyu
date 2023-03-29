def worst_delay(node_dic,e):
    disp=pow((node_dic[e[0]][0]-node_dic[e[1]][0]),2)+pow((node_dic[e[0]][1]-node_dic[e[1]][1]),2)
    dis=pow(disp,0.5)
    worst_case_delay=dis/0.5
    return worst_case_delay