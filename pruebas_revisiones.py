import requests
from cazador import CazadorDeDatos

def query_simple(pedido, language='en'):
    result = requests.get('https://{}.wikipedia.org/w/api.php'.format(language),
                                    params=pedido)
    return result

# ### Pruebas sobre revisiones
caza = CazadorDeDatos()

pedido_antiguos = {'action':'query',
#                      'list': 'categorymembers',
#                    'cmtype': 'page', 
#                      'cmtitle': 'Category:Physics',
                    'titles': 'Machine Learning',              
#                      'prop':'links'
                    'prop':'revisions',
                    'rvprop':'ids|timestamp',
#                    'rvprop':'ids|flags|timestamp|userid|tags|links',
                    'rvlimit':'100',
                    'rvstart':'2009-01-01T12:00:00Z',
                    'rvend':'2014-12-31T23:59:00Z',
                    'rvdir':'newer'
                    }
# res_antiguos = query_simple(pedido_antiguos)

res_antiguos = caza.query(pedido_antiguos)
for result in res_antiguos:
    print(result)
