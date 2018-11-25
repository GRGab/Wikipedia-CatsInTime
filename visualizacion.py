import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from utilities import unixtime

def plot_graphs(graphs):
    """
    graphs debe ser un dict de pares fecha : grafo
    """
    # Elijo el posicionamiento según la red más reciente
    dates = list(graphs.keys())
    last_date = max(dates, key=lambda x: unixtime(x))
    pos = nx.drawing.layout.spring_layout(graphs[last_date])
    # Grafico
    nrows = np.floor(np.sqrt(len(graphs)))
    ncols = np.ceil(len(graphs) / nrows)
    fig, axs = plt.subplots(nrows, ncols, figsize=(12, 8))
    axs = np.ravel(axs)
    for i, (date, g) in enumerate(graphs.items()):
        nx.draw(g, pos=pos, ax=axs[i])
        axs[i].annotate(date,
                    (.8, .8), xycoords='axes fraction',
                    backgroundcolor='w', fontsize=14)