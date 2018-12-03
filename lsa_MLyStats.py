import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
plt.ion()
import json

from pc_path import definir_path
path_git, path_datos_global = definir_path()
from os.path import join as osjoin

from crear_grafos_MLyStats import importar_MLyStats
from lsa import semantic_analysis, tune_LSA_dimension
from category_enrichment import enrich_history
from generar_grafos import save_graphs
from clustering import calculate_infomap


names_ml, names_st, data, children = importar_MLyStats()
dates = list(data.keys())

###############################################################################
##### Ajustar parámetro de LSA ########
###############################################################################

# CÓDIGO QUE CORRÍ PARA GENERAR LOS RESULTADOS
# d1 = [1, 5, 10, 15, 20, 25, 30, 35, 45]
# s1 = tune_LSA_dimension(data[dates[3]], d1)
# #### s1 = [0.01226514, 0.10327318, 0.13576405, 0.16176961, 0.17080465,
# ####       0.11075466, 0.02727159, 0.03609246, 0.03779507]
# d2 = [16, 17, 18, 19, 21, 22, 23, 24]
# s2 = tune_LSA_dimension(data[dates[3]], d2)
# #### s2 = [0.17493399, 0.17539572, 0.16051905, 0.16740142, 0.09963563,
# ####        0.10299056, 0.03419775, 0.02677208]
# xs, ys = [], []
# for i in range(40):
#     if i in d1:
#         index = d1.index(i)
#         xs.append(i)
#         ys.append(s1[index])
#     if i in d2:
#         index = d2.index(i)
#         xs.append(i)
#         ys.append(s2[index])

# RESULTADOS OBTENIDOS
xs = [1, 5, 10, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 35]
ys = [0.01226514, 0.10327318, 0.13576405, 0.16176961, 0.17493399,
      0.17539572, 0.16051905, 0.16740142, 0.17080465, 0.09963563,
      0.10299056, 0.03419775, 0.02677208, 0.11075466, 0.02727159,
      0.03609246]

# Graficamos
with plt.style.context(('seaborn')):
    fig, ax = plt.subplots()
ax.plot(xs, ys, '--.', color='deeppink', ms=20)
ax.set_xlabel('Dimensión LSA', fontsize=18)
ax.set_ylabel('Score', fontsize=18)
ax.tick_params(labelsize=16)
fig.tight_layout()

###############################################################################
##### Generar grafos LSA ########
###############################################################################

def semantic_analysis_MLyStats(data, n_components=17, n_iter=10,
                              ngram_range=(1,2), metric='cosine',
                              quantile=0.15,
                              enrich=True,
                              infomap=False,
                              save=False):
    graphs = {}
    for date, snapshot_data in data.items():
        graphs[date] = semantic_analysis(snapshot_data, n_components=17)
    if enrich:
        with open(osjoin(path_datos_global, 'category_mapping_MLyStats.json'),'r') as fp:
            category_mapping = json.load(fp)
        with open(osjoin(path_datos_global, 'names_ml.json'), 'r') as fp:
            names_ml = json.load(fp)
        with open(osjoin(path_datos_global, 'names_st.json'), 'r') as fp:
            names_st = json.load(fp)
        category_info = category_mapping, names_ml, names_st
        enrich_history(graphs, data, category_info, method='mapping_MLyStats')
    if infomap:
        graphs_infomap = {}
        for date, g in graphs:
            h = g.subgraph(max(nx.connected_components(nx.Graph(g)), key=len))
            calculate_infomap(h, directed=True)
            graphs_infomap[date] = h
    if save:
        save_graphs(graphs, 'MLyStats_LSA_{}dim'.format(n_components),
                    path_datos_global)
        if infomap:
            save_graphs(graphs_infomap, 'MLyStats_LSA_{}dim_infomap_cg'.format(n_components),
                        path_datos_global)
    return graphs

semantic_analysis_MLyStats(data, n_components=17, infomap=True, save=True)