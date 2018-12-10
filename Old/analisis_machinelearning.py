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

from clustering import calculate_infomap
from lsa import semantic_analysis, tune_LSA_dimension

import numpy as np
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

# Exportamos
save_graphs(graphs_originalcat, 'Machine_learning',
           osjoin(path_git, 'Grafos_guardados'))

# Para importar
g = nx.read_gexf(osjoin(path_git, 'Grafos_guardados', 'Machine_learning_2018-10-1.gexf'))

# Infomap para la componente gigante
g_cg = g.subgraph(max(nx.connected_components(nx.Graph(g)), key=len))
infomap_communities = calculate_infomap(g_cg)
nx.write_gexf(g_cg, osjoin(path_git, 'Grafos_guardados', 'Machine_learning_2018-10-1_infomap.gexf'))

# Afinar parámetro de LSA mediante comparación de clusterizaciones

# CÓDIGO QUE CORRÍ PARA GENERAR LOS RESULTADOS
# dimensions = np.arange(6, 32, 2)
# scores = tune_LSA_dimension(data[dates[3]], dimensions)
# dimensions_2 = np.array([13, 15, 17])
# scores_2 = tune_LSA_dimension(data[dates[3]], dimensions_2)
# xs, ys = [], []
# for i in range(40):
#     if i in dimensions:
#         index = np.where(dimensions == i)[0][0]
#         xs.append(i)
#         ys.append(scores[index])
#     if i in dimensions_2:
#         index = np.where(dimensions_2 == i)[0][0]
#         xs.append(i)
#         ys.append(scores_2[index])

# RESULTADOS OBTENIDOS
xs = [6, 8, 10, 12, 13, 14, 15, 16, 17, 18, 20, 22, 24, 26, 28, 30]
ys = [0.07687256926517101, 0.13142089534393475, 0.14301108292376694, 0.15403164311384546,
      0.15249932009546188, 0.1219241186506174, 0.1573626000536737, 0.16783365439202375,
      0.13498181053171332, 0.11621528270202362, 0.06934339612671694, 0.06511799509882962,
      0.05948172648134499, 0.05141303428985522, 0.06878146029203254, 0.0560939878096464]

# Graficamos
with plt.style.context(('seaborn')):
    fig, ax = plt.subplots()
ax.plot(xs, ys, '--.', color='deeppink', ms=20)
ax.set_xlabel('Dimensión LSA', fontsize=18)
ax.set_ylabel('Score', fontsize=18)
ax.tick_params(labelsize=16)
fig.tight_layout()


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
