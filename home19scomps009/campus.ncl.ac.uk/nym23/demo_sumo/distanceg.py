import math
def distance(node1_x,node2_x,node1_y,node2_y):
    distancep=math.pow ((node1_x-node2_x),2)+math.pow((node1_y-node2_y),2)
    distance=math.sqrt(distancep)*100
    return distance