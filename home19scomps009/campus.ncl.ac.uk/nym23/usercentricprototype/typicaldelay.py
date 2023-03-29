def typical_delay(node_dic,e):
    disp=pow((node_dic[e[0]][0]-node_dic[e[1]][0]),2)+pow((node_dic[e[0]][1]-node_dic[e[1]][1]),2)
    dis=pow(disp,0.5)
    typical_case_delay=dis*2/0.8
    return typical_case_delay