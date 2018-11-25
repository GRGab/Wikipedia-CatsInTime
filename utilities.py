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