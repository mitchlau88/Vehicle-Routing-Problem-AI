import networkx as nx
import matplotlib.pyplot as plt
import random as rand

def makeMap(m, n, gapfreq):
    """ Creates a graph in the form of a grid, with mXn nodes.
    The graph has irregular holes poked into it by random deletion.

    :param m: number of nodes on one dimension of the grid
    :param n: number of nodes on the other dimension
    :param gapfreq: the fraction of nodes to delete (see function prune() below)
    :return: a networkx graph with nodes and edges.

    The default edge weight is  (see below).  The edge weights can be changed by
    designing a list that tells the frequency of weights desired.
      100% edge weights 1:  [(1,100)]
      50% weight 1; 50% weight 2: [(1,50),(2,100)]
      33% each of 1,2,5: [(1,33),(2,67),(5,100)]
      a fancy distribution:  [(1,10),(4,50),(6,90),(10,100)]
      (10% @ 1, 40% @ 4, 40% @ 6, 10% @ 10)
    """
    g = nx.grid_2d_graph(m, n)
    weights = [(1,10),(4,50),(6,90),(10,100)]
    prune(g, gapfreq)
    setWeights(g, weights)
    return g


def setWeights(g, weights):
    """ Use the weights list to set weights of graph g
    :param g: a networkx graph
    :param weights: a list of pairs [(w,cf) ... ]
    :return: nothing

    weights are [(w,cf) ... ]
    w is the weight, cf is the cumulative frequency

    This function uses a uniform random number to index into the weights list.
    """
    for (i, j) in nx.edges(g):
        c = rand.randint(1,100)
        w = [a for (a,b) in weights if b >= c] # drop all pairs whose cf is < c
        g.edge[i][j]['weight'] = w[0]  # take the first weight in w
    return


def draw(g):
    """ Draw the graph, just for visualization.  Also creates a jpg in $CWD
    :param g: a networkx graph
    :return:
    """
    pos = {n: n for n in nx.nodes(g)}
    nx.draw_networkx_nodes(g, pos, node_size=20)
    nx.draw_networkx_labels(g,pos)
    edges = nx.edges(g)
    nx.draw_networkx_edges(g, pos, edgelist=edges, width=1)
    # Label the edge by its weight
    edge_labels = dict([((u, v,), d['weight'])
                    for u, v, d in g.edges(data=True)])

    nx.draw_networkx_edge_labels(g, pos, edge_labels)
    plt.axis('off')
    plt.savefig("simplegrid.png")  # save as png
    plt.show()  # display
    return


def prune(g, gapf):
    """ Poke random holes the graph g by deleting random nodes, with probability gapf.
    Then clean up by deleting all but the largest connected component.

    Interesting range (roughly):  0.1 < gapf < 0.3
    values too far above 0.3 lead to lots of pruning, but rather smaller graphs

    :param g: a networkx graph
    :param gapf: a fraction in [0,1]
    :return: nothing
    """
    # creating gaps...
    for node in nx.nodes(g):
        if rand.random() < gapf:
            g.remove_node(node)
    # deleting all but the largest connected component...
    comps = sorted(nx.connected_components(g), key=len, reverse=False)
    while len(comps) > 1:
        nodes = comps[0]
        for node in nodes:
            g.remove_node(node)
        comps.pop(0)

def setGarageLocation(g):
    #return: garage location
    x = rand.randint(0,g.number_of_nodes() -1)
    garaLoc = g.nodes()[x]
    return garaLoc

def setPickupLocation(g,packageNumber):
    #reutrn: list of pick up location

    #use for loop to get package locations and store in the pickLoclist
    #should be same for deliver location
    pickLoclist = []
    for i in range(0, packageNumber):
        x = rand.randint(0, g.number_of_nodes() - 1)
        #pickLoc =
        pickLoclist.insert(i, g.nodes()[x])
    return pickLoclist

def setDeliverLocation(g, packageNumber):
    # reutrn: list of pick up location

    # haven't finished this part yet
    # use for loop to get package locations and store in the pickLoclist
    # should be same for deliver location
    deliverLoclist = []

    for i in range(0, packageNumber):
        x = rand.randint(0, g.number_of_nodes() - 1)
        #deliverLoclist[i] = g.nodes()[x]
        #deliverLoclist.__add__(g.nodes()[x])
        deliverLoclist.insert(i,g.nodes()[x])
    return deliverLoclist

def findShortestPathGraph(graph):
    nodesNumber = len(graph.nodes())
    Result2DArray = [[0 for x in range(nodesNumber)] for x in range(nodesNumber)]
    for x in range(nodesNumber):
        for y in range (nodesNumber):

            Result2DArray[x][y]= nx.astar_path_length(graph,(graph.nodes()[x]),(graph.nodes()[y]))

    print 'this is shortest path'
    print graph.nodes()
    for j in range(nodesNumber):
        print Result2DArray[j]


    return Result2DArray

# script to use the above functions
dim = 5
gapfreq = 0.45
w = makeMap(dim, dim, gapfreq)      # a square graph
garage = setGarageLocation(w)                                                  #set garage at random postion on the map
numPackage = rand.randint(1, len(w.nodes()))                                   #random package number, less or equal than node number
pickLoclist = setPickupLocation(w, numPackage)
deliverLoclist = setDeliverLocation(w,numPackage)

for i in range(numPackage):
    if pickLoclist[i] == deliverLoclist[i]:
        deliverLoclist = setDeliverLocation(w,numPackage)

package = []
for j in range(numPackage):
    package.insert(j, [pickLoclist[j], deliverLoclist[j]])
	
shortestPathGraph = findShortestPathGraph(w)
#result printed
print "Total number of node in the map: ", w.nodes().__len__()          #same as len(w.nodes()), show the length of the nodelist
print "Garage location: ", garage
print "Package number: ", numPackage
print "Deliver location list: ", deliverLoclist
print "Pick up location list: ", pickLoclist

#print(nx.astar_path(w,(0,0),(2,2)))
#print(nx.astar_path_length(w,(0,0),(2,2)))
draw(w)
