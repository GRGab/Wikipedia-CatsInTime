import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.ion()
import json

from pc_path import definir_path
path_git, path_datos_global = definir_path()
from os.path import join as osjoin

from generar_grafos import childrendict_to_edgelist
from funciones_analisis import graph_summary
from modularity import calcular_modularidad



###############################################################################
##### Gráfico de categorías
###############################################################################

with open(osjoin(path_datos_global, 'children_MLyStats.json'), 'r') as fp:
    children = json.load(fp)
edges = childrendict_to_edgelist(children)
edges = [(e1[9:].replace('_', ''), e2[9:].replace('_', ' '))
         for e1, e2 in edges]
g = nx.DiGraph(edges)

nx.write_gexf(g, osjoin(path_git, 'Grafos_guardados', 'grafo_cats.gexf'))

from networkx.drawing.nx_agraph import write_dot, graphviz_layout
plt.title('draw_networkx')
pos = graphviz_layout(g, prog='dot')
nx.draw(g, pos, with_labels=False, arrows=True)
plt.savefig('nx_test.png')

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
##### Información básica
###############################################################################

print('===============================')
print('Redes de hipervínculos (dirigidas)')
print('===============================')
for g, date in zip(gs_hip, dates):
    print('-------------------------------')
    print(date)
    print('-------------------------------')
    graph_summary(g)
print('===============================')
print('Redes de LSA (no dirigidas)')
print('===============================')
for g, date in zip(gs_lsa, dates):
    print('-------------------------------')
    print(date)
    print('-------------------------------')
    graph_summary(g)

# Resultado guardado en datos_sumarios_MLyStats.txt
# (no puedo correr graph_summary en mi laptop)

###############################################################################
##### Overlap entre ML y ST y modularidad de "xor" en función del tiempo 
###############################################################################

def calc_overlap(g, attr1, attr2):
    numer = 0
    for node, d in dict(g.nodes).items():
        if d[attr1] and d[attr2]:
            numer += 1
    denom = g.order()
    return numer / denom

def calc_modularidad_xor(g, attr1, attr2):
    s1, s2 = [], []
    for node, d in dict(g.nodes).items():
        if d[attr1] and not d[attr2]:
            s1.append(node)
        elif d[attr2] and not d[attr1]:
            s2.append(node)
    s_tot = s1 + s2
    mod = calcular_modularidad(g.subgraph(s_tot), [s1, s2])
    return len(s1), len(s2), mod

# Overlap y mod xor para Hip
for g, date in zip(gs_hip, dates):
    print(date)
    overlap = calc_overlap(g, 'ML', 'ST')
    print('Overlap:', overlap)
    n1, n2, mod_xor = calc_modularidad_xor(g, 'ML', 'ST')
    print('Modularidad xor:', mod_xor)

## 2015
## Overlap: 0.10369181380417336
## Modularidad xor: 0.1580505348608351
## 2016
## Overlap: 0.10503685503685503
## Modularidad xor: 0.18081630531416892
## 2017
## Overlap: 0.10649658854939187
## Modularidad xor: 0.18278690906671952
## 2018
## Overlap: 0.10144532315244069
## Modularidad xor: 0.19557614045912403

# Solo mod xor para LSA (el overlap es el mismo)
for g, date in zip(gs_lsa, dates):
    print(date)
    n1, n2, mod_xor = calc_modularidad_xor(g, 'ML', 'ST')
    print('Modularidad xor:', mod_xor)

## 2015 Modularidad xor: 0.19682165893209122
## 2016 Modularidad xor: 0.19711720217735018
## 2017 Modularidad xor: 0.2110208731028174
## 2018 Modularidad xor: 0.17521316609178939

# Baja de 2017 a 2018 también...
# Si se me permite inferir causalidad a partir de correlación entre esto y el overlap...
# Diría que de 2017 a 2018, páginas que eran muy claramente o bien ST o bien
# ML, fueron marcadas como tales y no como pertenecientes a ambas.
# Donde una página "muy claramente" ST es una muy cercana semánticamente
# a muchas páginas ST, y lo mismo con ML
# Por lo tanto, suponiendo que era páginas ST que estaban marcadas
# como ST y ML a la vez y ahora están marcadas solo como ST, aumenta la
# conectividad intracluster para las páginas ST y eso disminuye el valor de la modularidad
# Es una hipótesis