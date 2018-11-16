
import networkx as nx
import matplotlib.pyplot as plt
plt.ion()
from cazador import CazadorDeDatos, curate_links
import numpy as np

def nestdict_to_edgelist(nestdict):
    """
    Función recursiva.
    Dada una estructura de diccionarios anidados, devolver la lista de enlaces
    dirigidos que señalan qué nodos son hijos de quién.
    """
    edgelist = []
    # Debería haber un solo nodo en nestdict, pero aún así la sintaxis del loop
    # me resulta cómoda
    assert len(nestdict) == 1
    root = list(nestdict.keys())[0]
    children = nestdict[root].keys()
    child_dicts = nestdict[root].values()
    edgelist += [(root, child) for child in children]
    subtrees = [{child: child_dict} for child, child_dict in zip(children, child_dicts)]
    for subtree in subtrees:
        edgelist += nestdict_to_edgelist(subtree)
    return edgelist



def lista_de_enlaces(data):
    pares_nodos = []
    nodos_1 = list(data.keys())
    for nodos in nodos_1:
        
        nodos_2 = data[nodos]['links']
        
        for nodoss in nodos_2:
            par = []
            par.append(nodos)
            par.append(nodoss)
            pares_nodos.append(par)
    return pares_nodos



if __name__ == '__main__':
    # Inicializamos objeto
    caza = CazadorDeDatos()
    # Estructura de categorías no tan chica
    arbol, n_l = caza.get_cat_tree('Category:Ions')

    # Construimos el grafo
    edges = nestdict_to_edgelist(arbol)
    g = nx.DiGraph()
    g.add_edges_from(edges)
    plt.figure()
    nx.draw(g, with_labels = False, node_size=20)

    # Qué categorías pertenecen a más de una categoría madre?
    # Estas categorías rompen la estructura de árbol
    especiales = [cat for cat, in_deg in g.in_degree if in_deg >= 2]
    
#%%  
    data, cats = caza.get_data_pagesincat('Category:Interaction')
    data = curate_links(data)
    
    #%%
    a = lista_de_enlaces(data)
    b = nx.Graph()
    b.add_edges_from(a)
#    nx.draw(b, node_size=6)
    nx.write_gexf(b,'Grafos_guardados/test_z.gexf')

    