from datetime import datetime
from copy import deepcopy
import time

def unixtime(dates):
    if isinstance(dates, str):
        unix_dates = time.mktime(datetime.strptime(dates, '%Y-%m-%dT%XZ').timetuple())
    else:
        unix_dates =  [time.mktime(datetime.strptime(date, '%Y-%m-%dT%XZ').timetuple())
                       for date in dates]
    return unix_dates

#### Funciones para obtener estructuras a partir de 'data' y 'children' ####

def get_setofcats(data):
    """
    Toma el diccionario data generado por CazadorDeDatos y devuelve el conjunto
    de las categorías a las que pertence por lo menos una de las páginas visitadas.
    """
    sets_of_cats = {}
    for date in data:
        set_of_cats = set()
        for cats in data[date]['categories']:
            set_of_cats.update(cats)
        print('# de categorías:', len(set_of_cats))
        sets_of_cats[date] = set_of_cats
    return sets_of_cats

#### Funciones para curación de links y categorías ####

def curate_links(data):
    """
    Toma el diccionario data generado por CazadorDeDatos y elimina todos los
    links malos encontrados en cada página visitada.
    """
    data = deepcopy(data)
    # Los links no deben comenzar con uno de estos prefijos.
    bad_prefixes = ["Wikipedia:", "Category:", "Template:",
                    "Template talk:", "Help:", "Portal:", "Book:"]
    # Chequeamos dicha condición mediante una función
    condition = lambda l: all(not l.startswith(pref) for pref in bad_prefixes)                    
    for date in data.keys():
        n_eliminated = 0
        for i, linklist in enumerate(data[date]['links']):
            n_initial = len(linklist)
            # Aplicamos la función como filtro
            linklist = [l for l in linklist if condition(l)]
            data[date]['links'][i] = linklist
            n_eliminated += n_initial - len(linklist)
        print('# links malos eliminados:', n_eliminated)
    return data

def curate_categories(sets_of_cats):
    sets_of_cats = deepcopy(sets_of_cats)
    bad_substrings = ['Wikipedia', 'Articles', 'Pages', 'Orphaned', 'People',
                    'CS1', 'articles', 'pages']
    condition = lambda l: all(not substr in l for substr in bad_substrings)
    for date, set_of_cats in sets_of_cats.items():
        good_ones = [x for x in set_of_cats if condition(x)]
        sets_of_cats[date] = set(good_ones)
    return sets_of_cats

# Deprecated
def count_items(query_result):
    """
    Función auxiliar que te tira cuántas páginas y cuántos links hay
    en un dado result
    """
    pages = query_result['pages']
    n_pages = len(pages)
    get_links = lambda dic: dic['links'] if 'links' in dic.keys() else []
    n_links_perpage = [len(get_links(pages[i])) for i in range(n_pages)]
    n_links_tot = sum(n_links_perpage)
    return n_pages, n_links_tot