from pc_path import definir_path
path_git, path_datos_global = definir_path()
from os.path import join as osjoin

import networkx as nx
from cazador import CazadorDeDatos
from generar_grafos import data_to_graphs, save_graphs

from utilities import (curate_links, get_setofcats, curate_categories)
from funciones_analisis import graph_summary
from category_enrichment import (get_visited_subcats,
                                get_descendantsdict,
                                print_common_descendants,
                                enrich_history)

import matplotlib.pyplot as plt
plt.ion()

#%%

caza = CazadorDeDatos()
carpeta = osjoin(path_datos_global, 'statistics')
data_raw, children = caza.cargar_datos(carpeta)
graphs_raw = data_to_graphs(data_raw)
dates = list(graphs_raw.keys())
# Un conjunto de categorías es el que se extrae directamente de data
# Es un conjunto para cada snapshot
sets_of_cats = curate_categories(get_setofcats(data_raw))
# Otro conjunto es el que se extrae de children
subcats = get_visited_subcats(children)

# Eliminamos links con prefijos malos
data = curate_links(data_raw)
graphs = data_to_graphs(data)

# Enriquecemos con información sobre las categorías (esto puede tardar un poco)

### Esta forma de enriquecer está buena pero no es la que más interesa ahora
# interesting_cats = ['Statistics', 'Machine_learning']
# enrich_interestingcats_history(graphs, data, interesting_cats)

### A cada página le asignamos la subcat a la que pertenecía al ser adquirida
#enrich_visitedcats_history(graphs, data, children)

### Una tercera forma, bastante interesante, sería fijar el nivel de profundidad
### en el árbol dado por 'children' y particionar a todas las páginas según las
### subcats presentes únicamente en ese nivel. PENDIENTE

# Subgrafos correspondientes a la categoría recorrida únicamente
graphs_originalcat = {date : graphs[date].subgraph(data[date]['names'])
                      for date in dates}

#g = graphs['2018-10-01T12:00:00Z']
save_graphs(graphs, 'statistics', osjoin(path_datos_global, 'statistics'))
save_graphs(graphs_originalcat, 'statistics_orcat', osjoin(path_datos_global, 'statistics'))
