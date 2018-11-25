import networkx as nx

def extremal_degrees(g, verbose=False):
    k_min = min(k for (nodo, k) in g.degree)
    k_max = max(k for (nodo, k) in g.degree)
    if verbose:
        print('kmin =', k_min, '| kmax =', k_max)
    if nx.is_directed(g):
        kin_min = min(k for (nodo, k) in g.in_degree)
        kin_max = max(k for (nodo, k) in g.in_degree)
        kout_min = min(k for (nodo, k) in g.out_degree)
        kout_max = max(k for (nodo, k) in g.out_degree)
        if verbose:
            print('kin_min =', kin_min, '| kin_max =', kin_max)
            print('kout_min =', k_min, '| kout_max =', k_max)
        return k_min, k_max, kin_min, kin_max, kout_min, kout_max
    else:
        return k_min, k_max

def graph_summary(g):
    if nx.is_directed(g):
        print('El grafo es dirigido')
    else:
        print('El grafo es no dirigido')
    print('# nodos:', g.order())
    print('# enlaces:', g.size())
    print('Densidad: {:.3g}'.format(nx.density(g)))
    print('Clustering medio: {:.3g}'.format(nx.average_clustering(g)))
    print('Transitividad: {:.3g}'.format(nx.transitivity(g)))
    extremal_degrees(g, verbose=True)

# Medio que esto no sirve para nada pero me costó codearlo y me da pena
def directed_diameter_summary(g):
    assert nx.is_directed(g)
    g_undir = nx.Graph(g)
    if nx.is_connected(g_undir):
        print('El grafo es (débilmente) conexo')
        print('El diámetro no dirigido del grafo es',
            nx.diameter(nx.Graph(g)))
        if nx.is_strongly_connected(g):
            print('Además el grafo es fuertemente conexo! Su diámetro dirigido es', nx.diameter(g))
    else:
        print('El grafo no es conexo. Analizando componente gigante.')
        # Notar que nx.connected_component_subgraphs no está implementado
        # para grafos dirigidos
        # Consideramos como componente gigante la componente débilmente
        # conexa más grande
        g_cg_undir = max(nx.connected_component_subgraphs(g_undir), key=len)
        g_cg = g.subgraph(g_cg_undir.nodes)
        print('# nodos:', g_cg.order(), '| # enlaces:', g_cg.size())
        print('El diámetro no dirigido de la componente gigante es',
            nx.diameter(g_cg_undir))
        if nx.is_strongly_connected(g_cg):
            print('Además el grafo es fuertemente conexo! Su diámetro dirigido es', nx.diameter(g_cg))