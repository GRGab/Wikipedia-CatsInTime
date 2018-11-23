from cazador import CazadorDeDatos
import matplotlib.pyplot as plt
plt.ion()
from generar_grafos import data_to_graphs, plot_graphs

caza = CazadorDeDatos()
carpeta = r'C:\Users\Gabo\Documents\Facultad\datos_wikipedia\machine_learning'
data, children = caza.cargar_datos(carpeta)

graphs = data_to_graphs(data)#, title='machine_learning', savefolder=carpeta)
dates = list(graphs.keys())
plot_graphs(graphs)