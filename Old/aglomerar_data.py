# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 00:49:16 2018

@author: Laura Gamboa
"""

from pc_path import definir_path
path_git, path_datos_global = definir_path()
from os.path import join as osjoin

from cazador import CazadorDeDatos
from funciones_analisis import (graph_summary, enrich_interestingcats_history,
                                enrich_visitedcats_history, get_visited_subcats)
from generar_grafos import data_to_graphs
from utilities import (curate_links, get_setofcats, curate_categories)


import networkx as nx
import matplotlib.pyplot as plt
plt.ion()

def comparar_grafos(carpeta_1, gexf_1, carpeta_2, gexf_2):
    o_1 = osjoin(path_datos_global,carpeta_1)
    o_2 = osjoin(path_datos_global,carpeta_2)
    graph_1 = nx.read_gexf(o_1, gexf_1)      
    graph_2 = nx.read_gexf(o_2,gexf_2)
    return graph_1,graph_2

graph_1 = nx.read_gexf(osjoin(path_datos_global, 'machine_learning\machine_learning_2018-10-1.gexf'))
graph_2 = nx.read_gexf(osjoin(path_datos_global, 'statistics\statistics_2018-10-1.gexf'))

graph_3 = nx.read_gexf(osjoin(path_datos_global, 'machine_learning\machine_learning_orcat_2018-10-1.gexf'))
graph_4 = nx.read_gexf(osjoin(path_datos_global, 'statistics\statistics_orcat_2018-10-1.gexf'))

n_1 = list(graph_1.nodes())
n_2 = list(graph_2.nodes())
compartidos = set(n_1) & set(n_2)
print(len(n_1), len(n_2),len(compartidos))


n_3 = list(graph_3.nodes())
n_4= list(graph_4.nodes())
compartidos = set(n_3) & set(n_4)
print(len(n_3), len(n_4),len(compartidos))



#g1,g2 = comparar_grafos('machine_learning','machine_learning_2018-10-1',
#                        'statistic','statistics_2018-10-1')

#%%
def aglomerar_data(cat_1, cat_2):
    caza = CazadorDeDatos()
    carpeta_1 = osjoin(path_datos_global, cat_1)
    carpeta_2 = osjoin(path_datos_global, cat_2)
    data_raw_1, children_1 = caza.cargar_datos(carpeta_1)
    
#    
#    graphs_raw = data_to_graphs(data_raw)
#    dates = list(graphs_raw.keys())
#    # Un conjunto de categorías es el que se extrae directamente de data
#    # Es un conjunto para cada snapshot
#    sets_of_cats = curate_categories(get_setofcats(data_raw))
#    # Otro conjunto es el que se extrae de children
#    subcats = get_visited_subcats(children)
#    
#    # Eliminamos links con prefijos malos
#    data = curate_links(data_raw)
#    graphs = data_to_graphs(data)
    return data_raw_1, children_1
aglomerar_data('statistics', 'machine_learning')
#%%



