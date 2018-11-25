from pc_path import definir_path
path_git, path_datos_global = definir_path()
from os.path import join as osjoin

import networkx as nx
from cazador import CazadorDeDatos
from funciones_analisis import graph_summary
from generar_grafos import data_to_graphs
from utilities import curate_links, get_setofcats, curate_categories

import matplotlib.pyplot as plt
plt.ion()


caza = CazadorDeDatos()
carpeta = osjoin(path_datos_global, 'machine_learning')
data_raw, children = caza.cargar_datos(carpeta)
graphs_raw = data_to_graphs(data_raw)
dates = list(graphs_raw.keys())
# Un conjunto de categorías es el que se extrae directamente de data
# Es un conjunto para cada snapshot
sets_of_cats = curate_categories(get_setofcats(data_raw))
# Otro conjunto es el que se extrae de children
subcats = list(children.keys())
for ls in children.values():
    subcats += ls
subcats = [string[9:].replace(' ', '_') for string in set(subcats)]

# Eliminamos links con prefijos malos
data = curate_links(data_raw)
graphs = data_to_graphs(data)

# Enriquecemos con información sobre las categorías (esto puede tardar un poco)

### Esta forma de enriquecer está buena pero no es la que más interesa ahora
# interesting_cats = ['Statistics', 'Machine_learning']
# for date, g in graphs.items():
#     names = data[date]['names']
#     categories = data[date]['categories']
#     cat_dict = {name : cat for name, cat in zip(names, categories)}
#     for nodo, dict_nodo in dict(g.nodes).items():
#         # Notar que no todos los nodos aparecen en names
#         for cat in interesting_cats:
#             if nodo in names:
#                 dict_nodo[cat] = True if cat in cat_dict[nodo] else False
#                 dict_nodo['<<EXTERNAL>>'] = False
#             else:
#                 dict_nodo[cat] = False
#                 dict_nodo['<<EXTERNAL>>'] = True

### A cada página le asignamos la subcat a la que pertenecía al ser adquirida
for date, g in graphs.items():
    names = data[date]['names']
    categories = data[date]['categories']
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

### Una tercera forma, bastante interesante, sería fijar el nivel de profundidad
### en el árbol dado por 'children' y particionar a todas las páginas según las
### subcats presentes únicamente en ese nivel. PENDIENTE


# Subgrafos correspondientes a la categoría recorrida únicamente
graphs_originalcat = {date : graphs[date].subgraph(data[date]['names'])
                      for date in dates}

#%%
print('===========================================')
print('Análisis de la categoría Machine Learning')
print('===========================================')
for date, g in graphs_originalcat.items():
    print('===============================')
    print('Red del', date)
    print('===============================')
    graph_summary(g)
    assert nx.is_directed(g), "Asumimos que nuestros grafos de entrada son dirigidos"
    g_undir = nx.Graph(g)
    print('-------------------------------')
    if nx.is_connected(g_undir):
        print('El grafo es (débilmente) conexo')
    else:
        print('El grafo no es conexo. Analizando componente gigante.')
        # Notar que nx.connected_component_subgraphs no está implementado
        # para grafos dirigidos
        # Consideramos como componente gigante la componente débilmente
        # conexa más grande
        g_cg_undir = max(nx.connected_component_subgraphs(g_undir), key=len)
        g_cg = g.subgraph(g_cg_undir.nodes)
        graph_summary(g_cg)
