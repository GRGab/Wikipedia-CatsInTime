from collections import deque

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

def get_roots(childrendict):
    """Devuelve una lista con los nombres de los nodos raíz de la estructura.
    Si no tiene ninguno tira un ValueError."""
    children_of_someone = [node for children in childrendict.values()
                                    for node in children]
    roots = []
    for node in childrendict.keys():
        if node not in children_of_someone:
            roots.append(node)
    if len(roots) == 0:
        raise ValueError('El diccionario childrendict no corresponde a una \
                          estructura con un nodo raíz.')
    return roots

def get_tree_level(childrendict, depth):
    """
    Devuelve el conjunto de nodos de un árbol que se encuentran en el nivel
    dado por 'depth'. Las raíz del árbol están en el nivel 0. El árbol se
    representa por el diccionario childrendict y puede no ser realmente un árbol.

    También funciona cuando no hay un solo nodo raíz (se trataría de un bosque
    si la estructura mencionada anteriormente fuera realmente un árbol, pero
    no es el caso). En ese caso, todas las raíces están en el nivel 0 y todos
    los nodos hijos de cualquier raíz están en el nivel 1.
    """
    # Determinamos cuáles son los nodos raíz
    roots = get_roots(childrendict)
    # Comenzamos la búsqueda en anchura
    visited = []
    output = []
    queue = deque()
    for root in roots:
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
    ser descendiente de más de un nodo en el nivel analizado. Para resolver
    esto usamos las funciones get_ancestordict y category_mapping_helper.
    """
    target_level = get_tree_level(childrendict, depth)
    descendantsdict = {}
    for node in target_level:
        formated_node = format_catstrings(node)
        formated_descendants = format_catstrings(flatten_subtree(node, childrendict))
        descendantsdict[formated_node] = formated_descendants     
    return descendantsdict

def get_ancestordict(descendantsdict, silent=False):
    """
    Función auxiliar para reconocer qué ediciones hay que hacer al
    descendantsdict y así alcanzar un buen category_mapping para la
    función enrich_mapping
    """
    nodes = [node for descendants in descendantsdict.values()
                      for node in descendants]
    ancestordict = {}
    for node in nodes:
        ancestors = [k for k, v in descendantsdict.items() if node in v]
        if len(ancestors) > 1:
            ancestordict[node] = ancestors
            if not silent:
                print(node, 'tiene como ancestros a')
                for ancestor in ancestors:
                    print('\t', ancestor)
    return ancestordict

def category_mapping_helper(descendantsdict):
    problematic_nodes = list(get_ancestordict(descendantsdict, silent=True).keys())
    descendantsdict2 = descendantsdict.copy()
    print('Comenzando proceso de desambiguar ancestros')
    print('Número de nodos con múltiples ancestros:', len(problematic_nodes))
    for node in problematic_nodes:
        try:
            # En cada paso, regeneramos el ancestordict debido a la posibilidad
            # de que se haya visto modificado en pasos anteriores
            ancestordict = get_ancestordict(descendantsdict2, silent=True)
            if node in ancestordict.keys():
                ancestors = ancestordict[node]
            else: # El problema ya se resolvió solo, vamos al siguiente nodo
                continue
            # Texto que mostramos al usuario para que pueda elegir
            in_to_anc = {i+1 : anc for i, anc in enumerate(ancestors)}
            print('Elegir ancestro para "{}"'.format(node))
            for i, ancestor in in_to_anc.items():
                print('\t{}. "{}"'.format(i, ancestor))
            # Pedimos la respuesta
            a = None
            while a is None:
                try:
                    a = int(input("Respuesta: "))
                    if a not in in_to_anc.keys():
                        a = None
                        raise ValueError
                except ValueError:
                    print("No es una respuesta válida...")
            # Actuamos la respuesta
            for i, ancestor in in_to_anc.items():
                if a != i:
                    if node == ancestor:
                        # El nodo pertence él mismo al nivel de la estructura
                        # bajo análisis. Tenemos que borrar a 'node' de los keys del
                        # descendantsdict
                        # Pero ojo: Puede que ahora queden nodos huérfanos!
                        possible_orphans = descendantsdict2[node]
                        del descendantsdict2[node]
                        not_orphans = [node for descendants in
                                                descendantsdict2.values()
                                            for node in descendants]
                        true_orphans = [x for x in possible_orphans if x
                                        not in not_orphans]
                        print('Los siguientes nodos quedaron huérfanos:')
                        for orphan in true_orphans:
                            print('\t', orphan)
                        print('Son reasignados como descendientes de "{}"'.format(in_to_anc[a]))
                        # Los huérfanos deben ser reacomodados como descendientes
                        # del nodo que "adoptó" a 'node'
                        old_list = descendantsdict2[in_to_anc[a]]
                        new_list = list(set(old_list + true_orphans))
                        descendantsdict2[in_to_anc[a]] = new_list
                    else:
                        # Borramos a 'node' de la lista de descendientes de 'ancestor'
                        old_list = descendantsdict2[ancestor]
                        descendantsdict2[ancestor] = [x for x in old_list if x != node]
        except KeyboardInterrupt:
            break
    return descendantsdict2

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

def enrich_mapping_MLyStats(g, snapshot_data, category_info):
    # Estas tres cosas vienen en el tercer argumento
    category_mapping, names_ml, names_st = category_info
    names = snapshot_data['names']
    categories = snapshot_data['categories']
    cat_dict = {name : cat for name, cat in zip(names, categories)}
    for nodo, dict_nodo in dict(g.nodes).items():
        # Notar que no todos los nodos aparecen en names
        if nodo in names:
            # Marcamos si partenecen a ML y/o a Stats
            dict_nodo['ML'] = True if nodo in names_ml else False
            dict_nodo['ST'] = True if nodo in names_st else False
            # Decidimos a qué categoría pertenece
            for cat, descendants in category_mapping.items():
                if any(d in cat_dict[nodo] for d in descendants):
                    dict_nodo['category'] = cat
                    break
                    # Importante: acá se asigna el nodo a la primera categoría
                    # que se encuentre. Esto introduce una arbitrariedad en el
                    # método de asignación de categorías que no es capturada
                    # por la función category_mapping_helper().
            else: # nodo no corresponde a ningún cat
                if nodo in names_ml and nodo not in names_st:
                    dict_nodo['category'] = 'GENERAL_ML'
                if nodo in names_st and nodo not in names_ml:
                    dict_nodo['category'] = 'GENERAL_ST'
                else:
                    dict_nodo['category'] = 'GENERAL_SHARED'
                
        else:
            dict_nodo['category'] = '<<EXTERNAL>>'


def enrich_history(graphs, data, category_info, method='mapping_MLyStats'):
    enrichment_function = {
        'interestingcats' : enrich_interestingcats,
        'visitedcats' : enrich_visitedcats,
        'mapping' : enrich_mapping,
        'mapping_MLyStats': enrich_mapping_MLyStats
    }
    for date, g in graphs.items():
        enrichment_function[method](g, data[date], category_info)