import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
plt.ion()
import json

from pc_path import definir_path
path_git, path_datos_global = definir_path()
from os.path import join as osjoin

from crear_grafos_MLyStats import importar_MLyStats
from category_enrichment import enrich_history
from generar_grafos import save_graphs

from clustering import calculate_infomap
from lsa import semantic_analysis, tune_LSA_dimension

names_ml, names_st, data, children = importar_MLyStats()
dates = list(data.keys())

###############################################################################
##### Ajustar parámetro de LSA ########
###############################################################################

# CÓDIGO QUE CORRÍ PARA GENERAR LOS RESULTADOS
# La densidad de MLyStats_2018-10-1.gexf es 0.004599492591880131
quantile = 0.005
d1 = [1, 5, 10, 15, 20, 25, 30, 35, 45]
s1 = tune_LSA_dimension(data[dates[3]], quantile, d1)
d2 = [26, 27, 28, 29, 31, 32, 33, 34]
s2 = tune_LSA_dimension(data[dates[3]], quantile, d2)
d3 = [36, 37, 38, 39, 40]
s3 = tune_LSA_dimension(data[dates[3]], quantile, d3)
xs, ys = [], []
for i in range(50):
    if i in d1:
        index = d1.index(i)
        xs.append(i)
        ys.append(s1[index])
    if i in d2:
        index = d2.index(i)
        xs.append(i)
        ys.append(s2[index])
    if i in d3:
        index = d3.index(i)
        xs.append(i)
        ys.append(s3[index])    

# RESULTADOS OBTENIDOS PARA QUANTILE = 0.15
#### d1 = [1, 5, 10, 15, 20, 25, 30, 35, 45]
#### s1 = [0.01226514, 0.10327318, 0.13576405, 0.16176961, 0.17080465,
####       0.11075466, 0.02727159, 0.03609246, 0.03779507]
#### d2 = [16, 17, 18, 19, 21, 22, 23, 24]
#### s2 = [0.17493399, 0.17539572, 0.16051905, 0.16740142, 0.09963563,
####        0.10299056, 0.03419775, 0.02677208]
#### xs = [1, 5, 10, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 35]
#### ys = [0.01226514, 0.10327318, 0.13576405, 0.16176961, 0.17493399,
####       0.17539572, 0.16051905, 0.16740142, 0.17080465, 0.09963563,
####       0.10299056, 0.03419775, 0.02677208, 0.11075466, 0.02727159,
####       0.03609246]

# RESULTADOS OBTENIDOS PARA QUANTILE = 0.005
#### d1 = [1, 5, 10, 15, 20, 25, 30, 35, 45]
#### s1 = [0.01471773, 0.20900798, 0.22355368, 0.29589481, 0.33755513,
####       0.36298817, 0.37523046, 0.35302397, 0.33965206]
#### d2 = [26, 27, 28, 29, 31, 32, 33, 34]
#### s2 = [0.38270605, 0.37207904, 0.36357612, 0.35818837, 0.36745252,
####       0.35742521, 0.36241252, 0.36890266]
#### d3 = [36, 37, 38, 39, 40]
#### s3 = [0.34987882, 0.34478591, 0.36063748, 0.35847823, 0.36165492]
xs = [1, 5, 10, 15, 20, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
      36, 37, 38, 39, 40, 45]
ys = [0.01471772559498695, 0.2090079793534772, 0.22355367818702987,
      0.2958948135408995, 0.33755513189104996, 0.36298817423492513,
      0.3827060457154983, 0.37207903941261466, 0.3635761238355246,
      0.35818836766098655, 0.37523046128154813, 0.36745252272206597,
      0.35742520529343275, 0.36241251590141293, 0.36890265734925914,
      0.35302396511739803, 0.3498788164602776, 0.3447859129116282,
      0.3606374815600279, 0.3584782333045342, 0.36165492152955897,
      0.33965205598497417]

# Graficamos
with plt.style.context(('seaborn')):
    fig, ax = plt.subplots()
ax.plot(xs, ys, '--.', color='deeppink', ms=20)
ax.set_xlabel('Dimensión LSA (adim.)', fontsize=18)
ax.set_ylabel('Score (adim.)', fontsize=18)
ax.tick_params(labelsize=16)
fig.tight_layout()

# Con quantile = 0.005, la dimensionalidad que maximiza el score es dim = 26

###############################################################################
##### Generar grafos LSA ########
###############################################################################

def semantic_analysis_MLyStats(data, quantile, n_components,
                               ngram_range=(1,2), n_iter=10, metric='cosine',
                               enrich=True,
                               infomap=False,
                               save=False):
    graphs = {}
    for date, snapshot_data in data.items():
        graphs[date] = semantic_analysis(snapshot_data, quantile, n_components)
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
        # Esto es si calculate_infomap requiere que le pase la compo gig
        # graphs_infomap = {}
        # for date, g in graphs.items():
        #     h = g.subgraph(max(nx.connected_components(nx.Graph(g)), key=len))
        #     calculate_infomap(h, directed=True)
        #     graphs_infomap[date] = h
        for date, g in graphs.items():
            calculate_infomap(g, directed=False)
    if save:
        save_graphs(graphs, 'MLyStats_LSA_{}dim_q{}'.format(n_components, quantile),
                    path_datos_global)
        # Esto es si calculate_infomap requiere que le pase la compo gig
        # if infomap:
        #     save_graphs(graphs_infomap, 'MLyStats_LSA_{}dim_infomap_cg'.format(n_components),
        #                 path_datos_global)
    return graphs

semantic_analysis_MLyStats(data, 0.005, 26, infomap=True, save=True)