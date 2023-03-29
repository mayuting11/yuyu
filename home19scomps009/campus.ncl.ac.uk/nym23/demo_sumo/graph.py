def graph_construct(datas,num_node):
    inf = 9999999999
    graph = [[(lambda x: 0 if x[0]==x[1] else inf)([i, j]) for j in range(num_node)] for i in range(num_node)]

    for u, v, d in datas:
        graph[u][v] = d	# 因为是有向图，边权只赋给graph[u][v]
        graph[v][u] = d # 如果是无向图，要加上这条。

    ##print costs
    #print('Costs:')
    #for row in graph:   
    #    for e in row:
    #        print('∞' if e == inf else e, end='\t')
    # print()

    #floyd algorithm
    parents = [[i] * num_node for i in range(num_node)]  # 关键地方，i-->j 的父结点初始化都为i
    return graph, parents 

