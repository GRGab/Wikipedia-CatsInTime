from datetime import datetime
import time

def unixtime(dates):
    unix_dates =  [time.mktime(datetime.strptime(date, '%Y-%m-%dT%XZ').timetuple())
                   for date in dates]

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
    data = data.copy()
    n_eliminated = 0
    for title in data.keys():
        linklist = data[title]['links']
        n_i = len(linklist)
        # Los links no deben comenzar con uno de estos prefijos.
        bad_prefixes = ["Wikipedia:", "Category:", "Template:",
                        "Template talk:", "Help:", "Portal:", "Book:"] 
        # Chequeamos dicha condición mediante una función
        condition = lambda l: all(not l.startswith(pref) for pref in bad_prefixes)
        # Aplicamos la función como filtro
        linklist = [l for l in linklist if condition(l)]
        n_f = len(linklist)
        data[title]['links'] = linklist
        n_eliminated += n_i - n_f
    print('# de links malos eliminados:', n_eliminated)
    return data