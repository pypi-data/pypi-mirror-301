from . import igraph_testing as ig

def STAT_n_D(graph):
    vertices = graph.vcount()
    count = 0;

    for vertex in range(vertices):
        if graph.vs[vertex]['color'] == 'black':
            count += 1
    
    return f'STAT_n_D {count}'

def STAT_n_A(graph):
    vertices = graph.vcount()
    count = 0;

    for vertex in range(vertices):
        if graph.vs[vertex]['color'] == 'white':
            count += 1
    
    return f'STAT_n_A {count}'
    
def STAT_CC_D_An(graph):
    cc = graph.connected_components();
    count = 0;

    for c in cc:
        if graph.vs[c][0]['color'] == 'black':
            count += 1
    
    return f'STAT_CC_D_An {count}'

def STAT_CC_A_Ca(graph):
    cc = graph.connected_components();
    count = 0;

    for c in cc:
        if graph.vs[c][0]['color'] == 'white':
            count += 1
    
    return f'STAT_CC_A_Ca {count}'

def descriptors(graph, fileName):
    fg = ig.filterGraph(graph)

    f = open(fileName,"x")

    with open(fileName,'a') as f:
        f.write(STAT_n_D(graph) + '\n')
        f.write(STAT_n_A(graph) + '\n')
        f.write(STAT_CC_D_An(fg) + '\n')
        f.write(STAT_CC_A_Ca(fg) + '\n')
