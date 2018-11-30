from pc_path import definir_path
path_git, path_datos_global = definir_path()
from os.path import join as osjoin

import networkx as nx
from cazador import CazadorDeDatos
<<<<<<< HEAD
from funciones_analisis import (graph_summary, enrich_interestingcats_history,
                                enrich_visitedcats_history, get_visited_subcats)
from generar_grafos import data_to_graphs, save_graphs
from utilities import (curate_links, get_setofcats, curate_categories)
=======
from generar_grafos import data_to_graphs, save_graphs

from utilities import (curate_links, get_setofcats, curate_categories)
from funciones_analisis import graph_summary
from category_enrichment import (get_visited_subcats,
                                get_descendantsdict,
                                print_common_descendants,
                                enrich_history)

>>>>>>> 58d1b9c001e5170453238d60cf8aed63317e8e62

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
subcats = get_visited_subcats(children)

# Eliminamos links con prefijos malos
data = curate_links(data_raw)
graphs = data_to_graphs(data)

# Enriquecemos con información sobre las categorías (esto puede tardar un poco)

### Esta forma de enriquecer está buena pero no es la que más interesa ahora
# interesting_cats = ['Statistics', 'Machine_learning']
# enrich_history(graphs, data, interesting_cats, method='interestingcats')

### A cada página le asignamos la subcat a la que pertenecía al ser adquirida
### No nos sirve tampoco
# enrich_history(graphs, data, children, method='visitedcats')


### Fijar el nivel de profundidad en el árbol dado por 'children' y particionar
### a todas las páginas según las subcats presentes únicamente en ese nivel.
"""
Comenzamos con el mapeo que realiza get_descendantsdict con depth=1:

category_mapping = get_descendantsdict(children, 1)

Pero tenemos que resolver el problema de que hay subcats que tienen más de
un ancestro en el nivel depth=1.
Para ir viendo qué ediciones manuales hacer sobre el category_mapping,
ejecutar lo siguiente:

print_common_descendants(category_mapping)

Eliminamos las apariciones de las subcategorías de una manera sensata
pero subjetiva. Una vez encontrados los cambios necesarios, los encapsulamos
en la función ajustar_mapping_machinelearning
"""

def category_mapping_machinelearning(children):
    category_mapping = get_descendantsdict(children, 1)
    del category_mapping['Bayesian_networks']
    category_mapping['Classification_algorithms'] = ['Classification_algorithms',
                                                    'Decision_trees']
    category_mapping['Machine_learning_algorithms'] = ['Machine_learning_algorithms']
    del category_mapping['Genetic_programming']
    category_mapping['Latent_variable_models'] = ['Latent_variable_models',
                                                'Structural_equation_models']
    del category_mapping['Support_vector_machines']
    category_mapping['Structured_prediction'] = ['Graphical_models',
                                                'Causal_inference',
                                                'Structured_prediction',
                                                'Bayesian_networks']
    return category_mapping

category_mapping = category_mapping_machinelearning(children)
enrich_history(graphs, data, category_mapping, method='mapping')

# Subgrafos correspondientes a la categoría recorrida únicamente
graphs_originalcat = {date : graphs[date].subgraph(data[date]['names'])
                      for date in dates}

save_graphs(graphs, 'machine_learning', osjoin(path_datos_global, 'machine_learning'))
save_graphs(graphs_originalcat, 'machine_learning_orcat', osjoin(path_datos_global, 'machine_learning'))
#Mati :Esto es lo tuyo, lo comento
# Exportamos
#save_graphs(graphs_originalcat, 'Machine_learning',
#            osjoin(path_git, 'Grafos_guardados'))

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
