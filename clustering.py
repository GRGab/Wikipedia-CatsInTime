import infomap
import igraph
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as colors
plt.ion()

def calculate_infomap(G, directed=True, use_igraph=False, silent=True):
    """
    Esto falla si G no es conexo
    """
    if use_igraph:
        print("Building igraph network from a NetworkX graph...")
        # Este paso de abajo se tilda, no está bueno trabajar con matrices no esparsas
        np_adj_list = nx.to_numpy_matrix(G)
        g = igraph.Graph.Weighted_Adjacency(np_adj_list.tolist(),mode=igraph.ADJ_UPPER)
        print("Find communities with Infomap...")
        labels = g.community_infomap(edge_weights="weight").membership
        nodes = list(G.nodes())
        communities = {node : label for node, label in zip(nodes, labels)}

    else:
        param_string = "--two-level"
        if directed:
            param_string += " --directed"
        if silent:
            param_string += " --silent"
        myInfomap = infomap.Infomap(param_string)

        print("Building Infomap network from a NetworkX graph...")
        g = nx.convert_node_labels_to_integers(G)
        network = myInfomap.network()
        for e in g.edges():
            network.addLink(*e)
            # myInfomap.addLink(*e)
        print("Find communities with Infomap...")
        myInfomap.run()
        print("Found {} modules with codelength: {}".format(myInfomap.numTopModules(), myInfomap.codelength()))
        communities = {}

        for node in myInfomap.iterTree():
            if node.isLeaf():
                communities[node.physicalId] = node.moduleIndex()

        communities = {attrDict['label'] : communities[node] for node, attrDict
                       in dict(g.nodes()).items()}
    nx.set_node_attributes(G, name='infomap', values=communities)
    return communities

def drawNetwork(G, attribute='infomap'):
    plt.figure()
    # position map
    pos = nx.spring_layout(G)
    # community ids
    communities = [v for k,v in nx.get_node_attributes(G, attribute).items()]
    # Convertimos estos ids a nums. enteros
    community_names = list(set(communities))
    communities = [community_names.index(x) for x in communities]
    numCommunities = len(set(communities))
    # color map from http://colorbrewer2.org/
    cmapLight = colors.ListedColormap(['#a6cee3', '#b2df8a', '#fb9a99', '#fdbf6f', '#cab2d6'], 'indexed', numCommunities)
    cmapDark = colors.ListedColormap(['#1f78b4', '#33a02c', '#e31a1c', '#ff7f00', '#6a3d9a'], 'indexed', numCommunities)

    # Draw edges
    nx.draw_networkx_edges(G, pos)

    # Draw nodes
    nodeCollection = nx.draw_networkx_nodes(G,
        pos = pos,
        node_color = communities,
        cmap = cmapLight
    )
    # Set node border color to the darker shade
    darkColors = [cmapDark(v) for v in communities]
    nodeCollection.set_edgecolor(darkColors)

    # Draw node labels
    for n in G.nodes():
        plt.annotate(n,
            xy = pos[n],
            textcoords = 'offset points',
            horizontalalignment = 'center',
            verticalalignment = 'center',
            xytext = [0, 0],
            color = cmapDark(communities[n])
        )

    plt.axis('off')
    plt.show()