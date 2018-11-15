import requests

class CazadorDeDatos():
    """
    COSAS IMPORTANTES A IMPLEMENTAR
    -------------------------------
        - Implementar función que agarra toda la data de una página dada
            - Los hipervínculos
            - El texto
            - Las etiquetas
            - Revisiones de distintas versiones
                - Determinar si podemos agarrar hipervínculos y etiquetas
                viejas además del texto.
        - Implementar pedir data de varias páginas simultáneamente.
        Esto es importante! Del manual de la API: 
            Do not ask for one page at a time – this is very inefficient,
            and consumes lots of extra resources and bandwidth. Instead
            you should request information about multiple pages by
            combining their titles or ids with the '|' pipe symbol:
            titles=PageA|PageB|PageC
        - Implementar función que realice el "crawl", agarrando
        hipervínculos de páginas previas y siguiéndolos. Antes de pedir
        la data de una nueva página, chequear que no haya sido adquirida
        antes.
    """
    def __init__(self, language='en', fmt='json', limit=500):
        self.language = language
        self.format = fmt
        self.limit = limit

    def query(self, pedido, continuar=True):
        pedido = pedido.copy()
        pedido.update({'action': 'query', 'format': self.format, 'redirects': ''})
        
        # Para que el formato sea el correcto
        if pedido['format'] in ['json', 'php']:
            pedido['formatversion'] = '2'
        # Seteamos los límites de elementos a sus valores máximos
        if 'cmtitle' in pedido.keys():
            pedido['cmlimit'] = self.limit
        if 'generator' in pedido.keys():
            if pedido['generator'] == 'links':
                pedido['gpllimit'] = self.limit
            if pedido['generator'] == 'categorymembers':
                pedido['gcmlimit'] = self.limit
        if 'prop' in pedido.keys():
            if 'links' in pedido['prop']:
                pedido['pllimit'] = self.limit
            if 'categories' in pedido['prop']:
                pedido['cllimit'] = self.limit
        # Comenzamos las llamadas a la API
        query_results = {}
        if continuar:
            lastContinue = {}
            while True:
                # Clone original request
                pedido2 = pedido.copy()
                # Modify it with the values returned in the 'continue' section of the last result.
                pedido2.update(lastContinue)
                # Call API
                result = requests.get('https://{}.wikipedia.org/w/api.php'.format(self.language),
                                    params=pedido2).json()
                if 'batchcomplete' in result and result['batchcomplete']==True:
                    # hacer algo
                    pass
                if 'error' in result:
                    raise Exception(result['error'])
                if 'warnings' in result:
                    print(result['warnings'])
                if 'query' in result:
                    query_results.update(result['query'])
                if 'continue' not in result:
                    break
                lastContinue = result['continue']
        else:
            result = requests.get('https://{}.wikipedia.org/w/api.php'.format(self.language),
                                    params=pedido).json()
            if 'batchcomplete' in result and result['batchcomplete']==True:
                # hacer algo
                pass
            if 'error' in result:
                raise Exception(result['error'])
            if 'warnings' in result:
                print(result['warnings'])
            if 'query' in result:
                query_results = result['query']
        return query_results

if __name__ == '__main__':
    caza = CazadorDeDatos()
    # res1 = caza.query({'list': 'categorymembers', 'cmtype': 'page', 'cmtitle': 'Category:Physics'})
    # res2 = caza.query({'titles': 'Main page'})

    # res3 = caza.query({'titles': 'Physics', 'prop': 'links'}, continuar=False)
    # links_res3 = res3['pages'][0]['links']
    # nombres_links = [links_res3[i]['title'] for i in range(len(links_res3))]

    # res4 = caza.query({'titles': 'Physics', 'prop': 'links', 'generator': 'links'}, continuar=False)

    res5 = caza.query({'gcmtitle': 'Category:Physics',
                       'prop': 'links',
                       'generator': 'categorymembers',
                       'gcmtype': 'page'
                       }, continuar=False)
    
    res6 = caza.query({'gcmtitle': 'Category:Physics',
                       'generator': 'categorymembers',
                       'gcmtype': 'subcat'
                       }, continuar=False)


    # pedido = {'action':'query',
    #           'titles': 'Category:Physics',              
    #           'generator': 'links',
    #           'prop':'links|categories',
    #           'pllimit': '500',
    #           'redirects': '',
    #           }
    # resu = caza.query(pedido)