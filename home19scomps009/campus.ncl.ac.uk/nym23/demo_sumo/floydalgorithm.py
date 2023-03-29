def floyd(graph,num_node,parents):
    for k in range(num_node):
        for i in range(num_node):
            for j in range(num_node):
                if graph[i][k] + graph[k][j] < graph[i][j]:
                    graph[i][j] = graph[i][k] + graph[k][j]
                    parents[i][j] = parents[k][j]  # 更新父结点
    return graph, parents