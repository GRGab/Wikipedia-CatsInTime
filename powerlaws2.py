
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from networkx.readwrite.gml import read_gml
from histograma import histograma
plt.ion()

from pc_path import definir_path
path_git, path_datos_global = definir_path()
from os.path import join as osjoin
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
##### DEFINICIONES PARA AJUSTAR
###############################################################################

# Vamos a llamar a R desde Python usando la librería rpy2
import rpy2.robjects as ro # Al hacer esto se inicializa un subproceso de R
from rpy2.robjects.packages import importr
# Usando importr, importamos paquetes de R que van a funcionar algo 
# así como módulos de Python

## EJECUTAR ESTO si no tienen instalado el paquete igraph (para instalarlo)
## import rpy2's package module
## select a mirror for R packages
utils = importr('utils')
utils.chooseCRANmirror(ind=2) # elijo de dónde descargar el paquete
## Instalo
from rpy2.robjects.vectors import StrVector
utils.install_packages(StrVector(['igraph']))

igraph = importr('igraph')
def ajustar_powerlaw(degrees):
    # Realizo el ajuste de la powerlaw
    # Creamos un vector de R pasándole los degrees
    degrees_r = ro.FloatVector(degrees)
    # Documentación de fit_power_law:
    # https://rdrr.io/cran/igraph/man/fit_power_law.html
    resultado = igraph.fit_power_law(degrees_r, implementation='plfit')
    print(resultado.r_repr())
    kmin = resultado.rx2('xmin')[0]
    gamma = resultado.rx2('alpha')[0]
    ksp = resultado.rx2('KS.p')[0]
    return kmin, gamma, ksp

###############################################################################
##### DEFINICIONES PARA GRAFICAR
###############################################################################

# Graficamos histograma + ajuste
from scipy.special import zeta
def f_powerlaw(x, gamma, kmin):
    # Como nuestro ajuste fue sobre una distribución de probabilidad discreta,
    # la cte de normalización es 1 sobre la función zeta de Riemann generalizada
    return x**(-gamma) / zeta(gamma, kmin)

def graficar_ajuste(degrees, gamma, kmin, ksp, ax=None):
    # ACLARACION IMPORTANTE
    # Para que se grafique bien la ley de potencias, es necesario llamar
    # a la función f_powerlaw poniendo kmin=1. Esto se debe a que el histograma
    # de grados está normalizado arrancando desde k=1, y no desde el kmin que
    # elige la función fit_power_law.
    if ax is None:
        fig, ax = plt.subplots(figsize=(8,6))
    else:
        fig = ax.get_figure()
    histograma(degrees, logbins=True, ax=ax, logx=True, logy=True,
            xlabel='k (adim.)', ylabel=True, ecolor='k', errbars=False, 
            labelsize=18, ticksize=16, bins=(1, max(degrees) + 2, 50))
    xs = np.linspace(1, max(degrees) + 2, 1000)
    # ax.plot(xs, f_powerlaw(xs, gamma, 1), '--', color='deeppink',
    #         label=r'$p(k) \propto k^{-\gamma}$')
    #xs = np.arange(1, max(degrees) + 2)
    ax.plot(xs, f_powerlaw(xs, gamma, 1), '--', color='deeppink',
           label=r'$p(k) \propto k^{-\gamma}$')
    ax.plot([], [], ' ', label=r'$\gamma = $' + '{:.4g}'.format(gamma))
    ax.plot([], [], ' ', label=r'$K_{min} = $' + '{:.0f}'.format(kmin))
    ax.plot([], [], ' ', label='p-value (KS) = {:.2g}'.format(ksp))
    ax.legend()
    ax.axvline(kmin, color='deeppink')

###############################################################################
##### AJUSTES
###############################################################################

## kmins = np.zeros((2, 4))
## gammas = np.zeros((2, 4))
## pvals = np.zeros((2, 4))
## for i, (gs, tipo_grafo) in enumerate(zip([gs_hip, gs_lsa], ['Hipervínculos', 'LSA'])):
##     for j, (g, date) in enumerate(zip(gs, dates)):
##         grados = list(dict(g.degree).values())
##         grados = [k for k in grados if k > 0]
##         kmins[i,j], gammas[i,j], pvals[i,j] = ajustar_powerlaw(grados)
kmins = np.array([[ 6.,  8.,  6.,  6.], [35., 34., 32., 22.]])
gammas = np.array([[1.66971403, 1.67993953, 1.66934817, 1.68027287],
                   [3.51156661, 3.15998797, 2.82922482, 2.28972772]])
pvals = np.array([[2.69136309e-09, 3.48774812e-09, 3.93905385e-07, 1.37205979e-07],
                  [1.49424463e-02, 1.25776734e-01, 4.05131993e-02, 6.55488472e-04]])

with plt.style.context(('seaborn')):
    fig, ax = plt.subplots(2, 4, figsize=(14, 8))
for i, (gs, tipo_grafo) in enumerate(zip([gs_hip, gs_lsa], ['Hipervínculos', 'LSA'])):
    for j, (g, date) in enumerate(zip(gs, dates)):
        grados = list(dict(g.degree).values())
        grados = [k for k in grados if k > 0]
        graficar_ajuste(grados, gammas[i,j], kmins[i,j], pvals[i,j], ax=ax[i,j])
fig.tight_layout()
