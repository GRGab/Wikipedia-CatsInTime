#### Utilities para asignación de categorías a los nodos

def format_catstrings(catstrings):
    if isinstance(catstrings, str):
        catstrings = catstrings[9:].replace(' ', '_')
    else:
        catstrings = [string[9:].replace(' ', '_') for string in catstrings]
    return catstrings

def get_visited_subcats(childrendict):
    """
    Toma el diccionario childrendict generado por CazadorDeDatos y devuelve una lista
    con los nombres de las categorías visitadas durante la adquisición, formateados
    del mismo modo que las listas 'categories' para cada página.
    """
    subcats = list(childrendict.keys())
    for ls in childrendict.values():
        subcats += ls
    subcats = format_catstrings(set(subcats))
    return subcats

def flatten_subtree(node, childrendict):
    flattened = [node]
    # Caso base: devuelvo flattened tal cual está
    # Caso recursivo:
    if node in childrendict.keys():
        for child in childrendict[node]:
            flattened += flatten_subtree(child, childrendict)
    # Como puede no ser un árbol posta, elimino repetidos antes de terminar
    return list(set(flattened))

def get_root(childrendict):
    children_of_someone = [node for children in childrendict.values()
                                    for node in children]
    for node in childrendict.keys():
        if node not in children_of_someone:
            root = node
            break
    else: # No se encontró ningún nodo raíz
        raise ValueError('El diccionario childrendict no corresponde a una \
                          estructura con un nodo raíz.')
    return root

def get_tree_level(childrendict, depth):
    """
    Devuelve el conjunto de nodos de un árbol que se encuentran en el nivel
    dado por 'depth'. La raíz del árbol está en el nivel 0. El árbol se
    representa por el diccionario childrendict y puede no ser realmente un árbol.
    """
    # Determinamos cuál es el nodo raíz
    root = get_root(childrendict)
    # Comenzamos la búsqueda en anchura
    visited = []
    output = []
    queue = deque()
    queue.append(root)
    queue.append('<<END_OF_LEVEL>>')
    nlevels = 0
    while len(queue) > 1:

        current_node = queue.popleft()
        if current_node == '<<END_OF_LEVEL>>':
            nlevels += 1
            if nlevels > depth:
                break
            queue.append('<<END_OF_LEVEL>>')
            current_node = queue.popleft()
            visited.append(current_node)
        
        if nlevels == depth:
            output.append(current_node)
        else:
            for child in childrendict[current_node]:
                if child not in visited and child not in queue:
                    queue.append(child)
    return output

def get_descendantsdict(childrendict, depth):
    """
    Devuelve un diccionario que a cada nodo en el nivel 'depth' del grafo dado
    por 'childrendict' le asigna el conjunto de sus nodos descendientes
    Dado que el grafo puede no ser un árbol propiamente dicho, un nodo puede
    ser descendiente de más de un nodo en el nivel analizado.
    """
    target_level = get_tree_level(childrendict, depth)
    descendantsdict = {}
    for node in target_level:
        formated_node = format_catstrings(node)
        formated_descendants = format_catstrings(flatten_subtree(node, childrendict))
        descendantsdict[formated_node] = formated_descendants     
    return descendantsdict

def print_common_descendants(descendantsdict):
    """
    Función auxiliar para ir editando a mano el descendantsdict y así alcanzar
    un buen category_mapping para la función enrich_mapping
    """
    nodes = [node for descendants in descendantsdict.values()
                      for node in descendants]
    for node in nodes:
        ancestors = [k for k, v in descendantsdict.items() if node in v]
        if len(ancestors) > 1:
            print(node, 'tiene como ancestros a')
            for ancestor in ancestors:
                print('\t', ancestor)

#### Funciones para enriquecer grafos de networkx con info de categorías ####

def enrich_interestingcats(g, snapshot_data, interesting_cats): 
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

def enrich_visitedcats(g, snapshot_data, childrendict):
    subcats = get_visited_subcats(childrendict)
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

def enrich_mapping(g, snapshot_data, category_mapping):
    names = snapshot_data['names']
    categories = snapshot_data['categories']
    cat_dict = {name : cat for name, cat in zip(names, categories)}
    for nodo, dict_nodo in dict(g.nodes).items():
        # Notar que no todos los nodos aparecen en names
        if nodo in names:
            for cat, descendants in category_mapping.items():
                if any(d in cat_dict[nodo] for d in descendants):
                    dict_nodo['category'] = cat
                    break
            else: # nodo no corresponde a ningún cat
                dict_nodo['category'] = 'General'
        else:
            dict_nodo['category'] = '<<EXTERNAL>>'

def enrich_history(graphs, data, category_info, method='mapping'):
    enrichment_function = {
        'interestingcats' : enrich_interestingcats,
        'visitedcats' : enrich_visitedcats,
        'mapping' : enrich_mapping
    }
    for date, g in graphs.items():
        enrichment_function[method](g, data[date], category_info)