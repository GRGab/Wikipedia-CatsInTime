from pc_path import definir_path
path_git, path_datos_global = definir_path()
from os.path import join as osjoin
from time import time

import networkx as nx
from collections import Counter
import json

from cazador import CazadorDeDatos
from generar_grafos import data_to_graphs, save_graphs

from utilities import (curate_links, get_setofcats, curate_categories)
from funciones_analisis import graph_summary
from category_enrichment import (get_visited_subcats,
                                get_descendantsdict,
                                get_ancestordict,
                                category_mapping_helper,
                                enrich_history)
from clustering import calculate_infomap

########### Funciones secundarias #####################

def cargar_datos():
    caza = CazadorDeDatos()
    carpeta_ml = osjoin(path_datos_global, 'machine_learning')
    carpeta_st = osjoin(path_datos_global, 'statistics')
    data_ml, children_ml = caza.cargar_datos(carpeta_ml)
    data_st, children_st = caza.cargar_datos(carpeta_st)
    # Eliminamos links con prefijos malos
    data_ml = curate_links(data_ml)
    data_st = curate_links(data_st)
    return data_ml, children_ml, data_st, children_st

def aglomerar_snapshot(ml_snapshot, st_snapshot):
    # Insight importante: si una página fue adquirida dos veces, las dos veces
    # se le asignó la misma información.
    snapshot_data = {}
    # Concatenamos las listas
    for key in ml_snapshot:
        snapshot_data[key] = ml_snapshot[key] + st_snapshot[key]
    # Eliminamos repetidos
    namelist = snapshot_data['names']
    for name, count in Counter(namelist).items():
        if count > 1:
            indexes = [i for i, n in enumerate(namelist) if n == name]
            indexes = indexes[1:]
            for key in snapshot_data:
                snapshot_data[key] = [x for i, x in enumerate(snapshot_data[key])
                                        if i not in indexes]
    return snapshot_data                                        
                                        
def aglomerar_data(data_ml, data_st, save=False):
    data = {}
    for date in data:
        ml_snapshot = data_ml[date]
        st_snapshot = data_st[date]
        data[date] = aglomerar_snapshot(ml_snapshot, st_snapshot)
    if save:
        # OJO: esto sobreescribe
        json.dump(data, open(osjoin(path_datos_global, 'data_MLyStats.json'),
                             'w'), indent=4)
    return data

def aglomerar_children(children_ml, children_st, save=False):
    # Si una misma categoría aparece en ambos 'children', combinamos
    # sus dos listas de descendientes en una sola
    children = {}
    shared_keys = set(children_ml.keys()).intersection(set(children_st.keys()))
    only_in_ml = set(children_ml.keys()).difference(set(children_st.keys()))
    only_in_st = set(children_st.keys()).difference(set(children_ml.keys()))
    for key in shared_keys:
        concatenation = children_ml[key] + children_st[key]
        children[key] = list(set(concatenation))
    for key in only_in_ml:
        children[key] = children_ml[key]
    for key in only_in_st:
        children[key] = children_st[key]
    if save:
        # OJO: esto sobreescribe
        json.dump(children, open(osjoin(path_datos_global, 'children_MLyStats.json'),
                             'w'), indent=4)
    return children

############# Funciones primarias ###################

# Ejecutamos esto una vez y ya está
def aglomerar_crudo():
    ti = time()
    # Cargamos datos crudos
    data_ml, children_ml, data_st, children_st = cargar_datos()
    # Listas de páginas
    dates = list(data_ml.keys()) # iguales para los dos 
    names_ml = data_ml[dates[3]]['names']
    names_st = data_st[dates[3]]['names']
    json.dump(names_ml, open(osjoin(path_datos_global, 'names_ml.json'),
                             'w'), indent=4)
    json.dump(names_st, open(osjoin(path_datos_global, 'names_st.json'),
                             'w'), indent=4)
    # Aglomeramos estructuras 'data' y 'children'
    aglomerar_data(data_ml, data_st, save=True)
    aglomerar_children(children_ml, children_st, save=True)
    print('Aglomeración terminada! Tiempo transcurrido:', int(time() - ti), 's')

# Luego importamos con esto
def importar_MLyStats():
    with open(osjoin(path_datos_global, 'names_ml.json'), 'r') as fp:
        names_ml = json.load(fp)
    with open(osjoin(path_datos_global, 'names_st.json'), 'r') as fp:
        names_st = json.load(fp)
    with open(osjoin(path_datos_global, 'data_MLyStats.json'), 'r') as fp:
        data = json.load(fp)
    with open(osjoin(path_datos_global, 'children_MLyStats.json'), 'r') as fp:
        children = json.load(fp)
    return names_ml, names_st, data, children


if __name__ == '__main__':
    names_ml, names_st, data, children = importar_MLyStats()

    # Creamos graphs
    dates = list(data.keys())
    graphs = data_to_graphs(data)
    # Nos quedamos solo con los grafos de las categorías visitadas
    graphs = {date : graphs[date].subgraph(data[date]['names']) for date in dates}

    ### Enriquecimiento por categorías

    ## Creación del category_mapping
    ## Como es un proceso manual, se hace una vez y se guarda
    # category_mapping = get_descendantsdict(children, 1)
    # category_mapping = category_mapping_helper(category_mapping)
    # with open(osjoin(path_datos_global, 'category_mapping_MLyStats.json'), 'w') as fp:
    #     json.dump(cat_map_4, fp, indent=4)
    ## Importamos
    with open(osjoin(path_datos_global, 'category_mapping_MLyStats.json'), 'r') as fp:
        category_mapping = json.load(fp)

    ### Enriquecemos
    category_info = (category_mapping, names_ml, names_st)
    enrich_history(graphs, data, category_info, method='mapping_MLyStats')

    # Guardamos los grafos
    save_graphs(graphs, 'MLyStats', osjoin(path_git, 'Grafos_guardados'))

    ### Agregamos clustering por infomap
    graphs_infomap = {}
    for date, g in graphs:
        h = g.subgraph(max(nx.connected_components(nx.Graph(g)), key=len))
        calculate_infomap(h, directed=True)
        graphs_infomap[date] = h

    save_graphs(graphs_infomap, 'MLyStats_infomap_cg', osjoin(path_git, 'Grafos_guardados'))