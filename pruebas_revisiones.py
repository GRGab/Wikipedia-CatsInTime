import requests
from cazador import CazadorDeDatos

def query_simple(pedido, language='en'):
    result = requests.get('https://{}.wikipedia.org/w/api.php'.format(language),
                    params=pedido)
    return result

# ### Pruebas sobre revisiones
caza = CazadorDeDatos()


pedido_antiguos = {'action':'query',
                   'format':'json',
                   'formatversion':2,
                   'redirects':'',

                #    'generator': 'categorymembers',
                #    'gcmtitle': 'Category:Ions',
                #    'gcmtype': 'page',

                #    'prop':'revisions',
                #    'rvprop': 'ids|timestamp',
                #    'rvlimit':'100',

                    #   'list': 'categorymembers',
                    # 'cmtype': 'page', 
                    #   'cmtitle': 'Category:Physics',
                    # 'prop':'revisions',
                    # 'rvprop':'ids|timestamp',

                    'titles': 'Machine learning',
                    'prop':'revisions',
                    'rvprop':'ids|timestamp',
                    'rvlimit':'100'

                    # 'rvlimit':'100',
                    # 'rvstart':'2009-01-01T12:00:00Z',
                    # 'rvend':'2009-01-31T23:59:00Z',
                    # 'rvdir':'newer'
                    }

res_antiguos = query_simple(pedido_antiguos)
print(res_antiguos)
# res_antiguos = caza.query(pedido_antiguos)
# for result in res_antiguos:
#     print(result)

pedido_oldid = {'action': 'parse',
                'format': 'json',
                'formatversion': 2,
                'oldid': 452653273,
                'prop': 'links|categories|text'}
res_oldid = query_simple(pedido_oldid).json()
print(res_oldid)