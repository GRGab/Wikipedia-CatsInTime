import numpy as np
from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt
plt.ion()

from cazador import CazadorDeDatos
from utilities import unixtime, curate_links


def childrendict_to_edgelist(childrendict):
    """
    Función apta para generar grafos dirigidos que representen relaciones
    entre categorías.
    INPUT
        childrendict : dict
            Contiene pares padre : hijos, donde padre es un string
            e hijos es una lista de strings
    OUTPUT
        edgelist : list
            Contiene duplas (padre, hijo)
    """
    edgelist = []
    for parent, children in childrendict.items():
        partial_edgelist = [(parent, child) for child in children]
        edgelist.append(partial_edgelist)
    return edgelist

def links_to_edgelist(names, links):
    """
    Dadas listas 'names' y 'links' para un cierto snapshot, devuelve un edgelist
    para networkx.
    """
    edgelist = []
    for name, ls in zip(names, links):
        for link in ls:
            edgelist.append((name, link))
    return edgelist

def edgelists(data):
    """
    Generar una edgelist por snapshot para networkx a partir de la estructura generada por
    CazadorDeDatos.
    """
    edges = {}
    for fecha in data:
        names = data[fecha]['names']
        links = data[fecha]['links']
        edges[fecha] = links_to_edgelist(names, links)
    return edges

def data_to_graphs(data, directed=True, title=None, savefolder=None):
    graphs = {}
    edges = edgelists(data)
    # Creamos los grafos
    for date in edges:
        if directed:
            graphs[date] = nx.DiGraph(edges[date])
        else:
            graphs[date] = nx.Graph(edges[date])
    # Guardar los grafos en formato .gexf
    if savefolder is not None:
        assert title is not None
        for date, g in graphs.items():
            date = datetime.strptime(date, '%Y-%m-%dT%XZ')
            date = '{}-{}-{}'.format(date.year, date.month, date.day)
            nx.write_gexf(g,'{}_{}.gexf'.format(title, date))
    return graphs

def plot_graphs(graphs):
    """
    graphs debe ser un dict de pares fecha : grafo
    """
    # Elijo el posicionamiento según la red más reciente
    dates = list(graphs.keys())
    last_date = max(dates, key=lambda x: unixtime(x))
    pos = nx.drawing.layout.spring_layout(graphs[last_date])
    # Grafico
    nrows = np.floor(np.sqrt(len(graphs)))
    ncols = np.ceil(len(graphs) / nrows)
    fig, axs = plt.subplots(nrows, ncols, figsize=(12, 8))
    axs = np.ravel(axs)
    for i, (date, g) in enumerate(graphs.items()):
        nx.draw(g, pos=pos, ax=axs[i])
        axs[i].annotate(date,
                    (.8, .8), xycoords='axes fraction',
                    backgroundcolor='w', fontsize=14)



# DEPRECATED
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

# DEPRECATED ???
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
    test_get_cat_tree = False
    if test_get_cat_tree:
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