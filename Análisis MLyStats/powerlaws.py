import plfit
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from time import time
plt.ion()

from pc_path import definir_path
path_git, path_datos_global = definir_path()
from os.path import join as osjoin
# Ejemplo de uso de la librería plfit (https://github.com/keflavich/plfit)
## X = np.random.rand(1000)
## myplfit = plfit.plfit(X)
## plt.figure()
## myplfit.plotpdf()
## ti = time()
## myplfit.test_pl(niter=100)
## print(time() - ti, 's')

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
##### Generar gráficos y p-valores
###############################################################################

# Guardar data sobre los ajustes por powerlaw via método Shalizi-Newman-Clauset

# Para niter = 100, tarda 14 segundos en hacer un test_pl
# Para niter = 1000, debería tardar 30 min en total
niter = 1000

plfits = []
kmins = np.zeros((2, 4))
alphas = np.zeros((2, 4))
pvals = np.zeros((2, 4))
ks_statistics = np.zeros((2, 4, niter))
for i, (gs, tipo_grafo) in enumerate(zip([gs_hip, gs_lsa], ['Hipervínculos', 'LSA'])):
    for j, (g, date) in enumerate(zip(gs, dates)):
        grados = list(dict(g.degree).values())
        grados = [k for k in grados if k > 0]
        myplfit = plfit.plfit(grados, discrete=True)
        plfits.append(myplfit)
        kmins[i, j], alphas[i, j] = myplfit.plfit()
        pvals[i, j], ks_statistics[i, j, :] = myplfit.test_pl(niter=niter)

# p(1000) = 0.000
# p(1000) = 0.000
# p(1000) = 0.000
# p(1000) = 0.000
# /home/gabo/anaconda3/lib/python3.6/site-packages/plfit/plfit.py:940: RuntimeWarning: divide by zero encountered in log
#   L_of_alpha = -1*nn*log(zeta) - alpha * sum_log_data
# p(1000) = 0.000
# p(1000) = 0.001
# p(1000) = 0.000
# p(1000) = 0.000
#
# In [131]: alphas
# Out[131]:
# array([[1.6286124 , 1.65879103, 1.65317903, 1.66561344],
#        [3.51027474, 3.15907756, 2.80589358, 2.28956824]])
# In [132]: kmins
# Out[132]:
# array([[ 4.,  5.,  5.,  5.],
#        [35., 34., 31., 22.]])
# In [133]: pvals
# Out[133]:
# array([[0.   , 0.   , 0.   , 0.   ],
#        [0.   , 0.001, 0.   , 0.   ]])


# Realizar gráficos
with plt.style.context(('seaborn')):
    fig, ax = plt.subplots(2, 4, figsize=(14, 8))
for i, (gs, tipo_grafo) in enumerate(zip([gs_hip, gs_lsa], ['Hipervínculos', 'LSA'])):
    for j, (g, date) in enumerate(zip(gs, dates)):
        grados = list(dict(g.degree).values())
        grados = [k for k in grados if k > 0]
        myplfit = plfit.plfit(grados, discrete=True)
        plt.sca(ax[i, j])
        # myplfit.plotpdf()
        # myplfit.plotcdf()
        # myplfit.plotppf()
        # myplfit.xminvsks()
        # myplfit.alphavsks()
fig.tight_layout()