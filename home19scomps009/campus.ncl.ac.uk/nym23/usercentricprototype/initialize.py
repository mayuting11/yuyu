def initialize (nodeid,exitnodeid):
    lookup_table={}
    for i in nodeid:
        if i not in exitnodeid:
            lookup_table[i]=[]
        else:
            lookup_table[i]=[[0,[],0]]
    return lookup_table
