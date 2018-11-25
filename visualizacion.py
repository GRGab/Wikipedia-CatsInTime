import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from utilities import unixtime

def plot_graphs(graphs, color_cat=None):
    """
    graphs debe ser un dict de pares fecha : grafo
    """
    # Elijo el posicionamiento según la red más reciente
    dates = list(graphs.keys())
    last_date = max(dates, key=lambda x: unixtime(x))
    pos = nx.drawing.layout.spring_layout(graphs[last_date])
    # Grafico
    nrows = int(np.floor(np.sqrt(len(graphs))))
    ncols = int(np.ceil(len(graphs) / nrows))
    fig, axs = plt.subplots(nrows, ncols, figsize=(12, 8))
    axs = np.ravel(axs)
    for i, (date, g) in enumerate(graphs.items()):
        if color_cat is not None:
            colors = ['dodgerblue' if color_cat in nodo['categories'] else 'black'
                    for nodo in g.nodes]
            nx.draw(g, pos=pos, ax=axs[i], node_size=10, node_color=colors)
        else:
            nx.draw(g, pos=pos, ax=axs[i])
        axs[i].set_title(date)
    plt.show()