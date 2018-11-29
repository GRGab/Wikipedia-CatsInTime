import networkx as nx
from collections import deque

#### Funciones sumario ####

def extremal_degrees(g, verbose=False):
    k_min = min(k for (nodo, k) in g.degree)
    k_max = max(k for (nodo, k) in g.degree)
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
        if verbose:
            print('kmin =', k_min, '| kmax =', k_max)
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

#### Funciones para manipular grafos de networkx ####

def enrich_interestingcats_snapshot(g, snapshot_data, interesting_cats): 
    names = snapshot_data['names']
    categories = snapshot_data['categories']
    cat_dict = {name : cat for name, cat in zip(names, categories)}
    for nodo, dict_nodo in dict(g.nodes).items():
        # Notar que no todos los nodos aparecen en names
        for cat in interesting_cats:
            if nodo in names:
                dict_nodo[cat] = True if cat in cat_dict[nodo] else False
                dict_nodo['<<EXTERNAL>>'] = False
            else:
                dict_nodo[cat] = False
                dict_nodo['<<EXTERNAL>>'] = True

def enrich_interestingcats_history(graphs, data, interesting_cats):
    for date, g in graphs.items():
        enrich_interestingcats_snapshot(g, data[date], interesting_cats)

def enrich_visitedcats_snapshot(g, snapshot_data, children):
    subcats = get_visited_subcats(children)
    names = snapshot_data['names']
    categories = snapshot_data['categories']
    cat_dict = {name : cat for name, cat in zip(names, categories)}
    for nodo, dict_nodo in dict(g.nodes).items():
        # Notar que no todos los nodos aparecen en names
        if nodo in names:
            for cat in subcats:
                if cat in cat_dict[nodo]:
                    dict_nodo['category'] = cat
                    break
        else:
            dict_nodo['category'] = '<<EXTERNAL>>'

def enrich_visitedcats_history(graphs, data, children):
    for date, g in graphs.items():
        enrich_visitedcats_snapshot(g, data[date], children)

#### Utilities

def get_visited_subcats(children):
    """
    Toma el diccionario children generado por CazadorDeDatos y devuelve una lista
    con los nombres de las categorías visitadas durante la adquisición, formateados
    del mismo modo que las listas 'categories' para cada página.
    """
    subcats = list(children.keys())
    for ls in children.values():
        subcats += ls
    subcats = [string[9:].replace(' ', '_') for string in set(subcats)]
    return subcats

def get_children_level(children, root, depth):
    if depth == 0:
        return root
    
    cats_visited = []
    queue = deque()
    queue.append(root)
    queue.append('<<END_OF_LEVEL>>')
    nlevels = 0

    while len(queue) > 1 and nlevels <= depth:
        cat_actual = queue.popleft()
        cats_visited.append(cat_actual)
        if cat_actual == '<<END_OF_LEVEL>>':
            nlevels += 1
            queue.append('<<END_OF_LEVEL>>')
            cat_actual = queue.popleft()
            cats_visited.append(cat_actual)
        
        for subcat in children[cat_actual]:
            if subcat not in cats_visited and subcat not in queue:
                queue.append(subcat)

def get_ancestordict(children, root, depth):
    pass