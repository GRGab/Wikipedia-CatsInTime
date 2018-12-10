import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
plt.ion()
import json

from pc_path import definir_path
path_git, path_datos_global = definir_path()
from os.path import join as osjoin

from sklearn.metrics import (normalized_mutual_info_score,
                            mutual_info_score,
                            adjusted_mutual_info_score)

###############################################################################
##### Importar grafos
###############################################################################

dates = [2015, 2016, 2017, 2018]
gs_hip = []
names_hip = ['MLyStats_{}-10-1.gexf'.format(i) for i in dates]
paths_hip = [osjoin(path_git, 'Grafos_guardados', name) for name in names_hip]
for path in paths_hip:
    gs_hip.append(nx.read_gexf(path))
gs_lsa = []
names_lsa = ['MLyStats_LSA_26dim_q0.005_{}-10-1.gexf'.format(i) for i in dates]
paths_lsa = [osjoin(path_git, 'Grafos_guardados', name) for name in names_lsa]
for path in paths_lsa:
    gs_lsa.append(nx.read_gexf(path))

###############################################################################
##### Calcular info mutua entre 'infomap' y 'category'
###############################################################################

def calcular_ims(grafos, mutual_info='normal'):
    mi_function = {'normal': mutual_info_score,
                   'normalized': normalized_mutual_info_score,
                   'adjusted': adjusted_mutual_info_score}
    ims = []
    for g in grafos:
        g = max(nx.connected_component_subgraphs(nx.Graph(g)), key=len)
        infomap_dict = nx.get_node_attributes(g, 'infomap')
        category_dict = nx.get_node_attributes(g, 'category')
        infomaps, categories = [], []
        for name in infomap_dict.keys():
            infomaps.append(infomap_dict[name])
            categories.append(category_dict[name])
        im = mi_function[mutual_info](infomaps, categories)
        ims.append(im)
    return ims

# im_hip1 = calcular_ims(gs_hip, 'normal')
# print(im_hip1)
im_hip2 = calcular_ims(gs_hip, 'normalized')
print(im_hip2)
# im_hip3 = calcular_ims(gs_hip, 'adjusted')
# print(im_hip3)

# im_lsa1 = calcular_ims(gs_lsa, 'normal')
# print(im_lsa1)
im_lsa2 = calcular_ims(gs_lsa, 'normalized')
print(im_lsa2)
# im_lsa3 = calcular_ims(gs_lsa, 'adjusted')
# print(im_lsa3)


# Resultados para normalized info score
## IM entre 'infomap' y 'category' para Hip
## [0.4201, 0.4298, 0.4314, 0.4348]
## IM entre 'infomap' y 'category' para LSA
## [0.4411, 0.4547, 0.4662, 0.4829]