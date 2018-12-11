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

def rellenar_con_numero(g, attrs_nodos, attrs_edges, numero):
    for nodo, dictattr in dict(g.nodes).items():
        for attr in attrs_nodos:
            if attr not in dictattr.keys():
                dictattr[attr] = numero
    for edge, dictattr in dict(g.edges).items():
        for attr in attrs_edges:
            if attr not in dictattr.keys():
                dictattr[attr] = numero

attrs_nodos = (['Existe_{}'.format(date) for date in dates]
               +['category_{}'.format(date) for date in dates])
attrs_edges = ['Existe_{}'.format(date) for date in dates]

rellenar_con_false(g_hip, attrs_nodos, attrs_edges)
rellenar_con_false(g_lsa, attrs_nodos, attrs_edges)

atributos_infomap = ['infomap_{}'.format(date) for date in dates]
rellenar_con_numero(g_hip, atributos_infomap, [], -2)
rellenar_con_numero(g_lsa, atributos_infomap, [], -2)

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
                
    for edge, dictattr in dict(g.edges).items():
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
##### Agregar colores
###############################################################################

def agregar_colores(g, attribute, palette):
    """palette debe ser una lista de dicts, cada uno de los cuales tiene 4 keys:
    'r', 'g', 'b' y 'a' (los 3 colores RGB, con valores que van entre 0 y 255,
    y el valor "alfa" de transparencia que va entre 0 y1.)
    """
    # Creo lista de clusters (particion) ordenada de mayor a menor tamaño
    attr_dict = nx.get_node_attributes(g, attribute)
    cluster_names = set(attr_dict.values())
    partition = []
    for cluster in cluster_names:
        partition.append([x for x,v in attr_dict.items() if v == cluster])
    partition = sorted(partition, key=len, reverse=True)
    # Asigno los colores de la paleta a los clusters más grandes
    for cluster, rgba_dict in zip(partition, palette):
        for node in cluster:
            g.nodes[node]['viz'] = {'color': rgba_dict}

### Prueba rápida / Ejemplo de cómo usar
# g_hip = nx.read_gexf(osjoin(path_git, 'Grafos_guardados', 'g_hip_mergeado.gexf'))
# paleta = [
#     {'r': 255, 'g': 0, 'b': 0, 'a': 1},
#     {'r': 0, 'g': 255, 'b': 0, 'a': 1},
#     {'r': 0, 'g': 0, 'b': 255, 'a': 1}
# ]
# g_hip_coloreado = g_hip.copy()
# agregar_colores(g_hip_coloreado, 'infomap_2018', paleta)
# nx.write_gexf(g_hip_coloreado, osjoin(path_git, 'Grafos_guardados', 'g_hip_mergeado_coloreado.gexf'))

###############################################################################
###############################################################################
###############################################################################
#~#~#~# ACÁ DEFINIR LA PALETA, APLICARLA A g_hip, g_lsa Y LUEGO EXPORTAR CON EL
#~#~#~# CÓDIGO DE LA SECCIÓN DE ABAJO
###############################################################################
###############################################################################
###############################################################################

###############################################################################
##### Exportar
###############################################################################

nx.write_gexf(g_hip, osjoin(path_git, 'Grafos_guardados', 'g_hip_mergeado.gexf'))
nx.write_gexf(g_lsa, osjoin(path_git, 'Grafos_guardados', 'g_lsa_mergeado.gexf'))