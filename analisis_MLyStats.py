import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.ion()
import json

from pc_path import definir_path
path_git, path_datos_global = definir_path()
from os.path import join as osjoin

from funciones_analisis import graph_summary
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
##### Overlap entre ML y ST
###############################################################################

