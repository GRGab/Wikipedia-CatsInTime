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
##### Renombrar infomaps y categories, agregar "existe"
###############################################################################

def renombrar_atributo(g, viejo, nuevo):
    for nodo, dictattr in dict(g.nodes).items():
        dictattr[nuevo] = dictattr[viejo]
        del dictattr[viejo]

def agregar_atributo_true_nodos(g, nombre):
    for nodo, dictattr in dict(g.nodes).items():
        dictattr[nombre] = True

def agregar_atributo_true_edges(g, nombre):
    for edge, dictattr in dict(g.edges).items():
        dictattr[nombre] = True


for gs in [gs_hip, gs_lsa]:
    for g, date in zip(gs, dates):
        for viejo in ['infomap', 'category']:
            renombrar_atributo(g, viejo, viejo + '_{}'.format(date))
            agregar_atributo_true_nodos(g, 'Existe_{}'.format(date))
            agregar_atributo_true_edges(g, 'Existe_{}'.format(date))

###############################################################################
##### Componer grafos y rellenar con false
###############################################################################

g_hip = nx.compose_all(gs_hip)
g_lsa = nx.compose_all(gs_lsa)

def rellenar_con_false(g, attrs_nodos, attrs_edges):
    for nodo, dictattr in dict(g.nodes).items():
        for attr in attrs_nodos:
            if attr not in dictattr.keys():
                dictattr[attr] = False
    for edge, dictattr in dict(g.edges).items():
        for attr in attrs_edges:
            if attr not in dictattr.keys():
                dictattr[attr] = False
attrs_nodos = (['Existe_{}'.format(date) for date in dates]
               +['infomap_{}'.format(date) for date in dates]
               +['category_{}'.format(date) for date in dates])
attrs_edges = ['Existe_{}'.format(date) for date in dates]

rellenar_con_false(g_hip, attrs_nodos, attrs_edges)
rellenar_con_false(g_lsa, attrs_nodos, attrs_edges)

###############################################################################
##### agregar nacimiento
###############################################################################


def agregar_nacimiento(g, dates):
    for nodo, dictattr in dict(g.nodes).items():
        dictattr['nacimiento_{}'.format(dates[0])] = False
        for i in range(1, len(dates)):
            if (dictattr['Existe_{}'.format(dates[i-1])] == False
            and dictattr['Existe_{}'.format(dates[i])] == True):
                dictattr['nacimiento_{}'.format(dates[i])] = True
            else:
                dictattr['nacimiento_{}'.format(dates[i])] = False

for g in [g_hip, g_lsa]:
    agregar_nacimiento(g, dates)


###############################################################################
##### Exportar
###############################################################################

nx.write_gexf(g_hip, osjoin(path_git, 'Grafos_guardados', 'g_hip_mergeado.gexf'))
nx.write_gexf(g_lsa, osjoin(path_git, 'Grafos_guardados', 'g_lsa_mergeado.gexf'))