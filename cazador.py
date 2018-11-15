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
    def __init__(self, language='en', fmt='json', data_limit='max',
                 generator_limit=50):
        self.language = language
        self.format = fmt
        self.data_limit = data_limit
        self.generator_limit = generator_limit
        # actiondict es el dict con parámetros que se usan siempre
        self.actiondict = self.set_actiondict()

    def set_actiondict(self):
        actiondict = {'action': 'query',
                      'format': self.format,
                      'redirects': ''}
        # Para que el formato sea el correcto:
        if actiondict['format'] in ['json', 'php']:
            actiondict['formatversion'] = '2'
        return actiondict

    def set_limits(self, pedido):
        if 'cmtitle' in pedido.keys():
            pedido['cmlimit'] = self.data_limit
        if 'generator' in pedido.keys():
            if pedido['generator'] == 'links':
                pedido['gpllimit'] = self.generator_limit
            if pedido['generator'] == 'categorymembers':
                pedido['gcmlimit'] = self.generator_limit
        if 'prop' in pedido.keys():
            if 'links' in pedido['prop']:
                pedido['pllimit'] = self.data_limit
            if 'categories' in pedido['prop']:
                pedido['cllimit'] = self.data_limit
        return pedido

    def query(self, pedido, continuar=True):
        pedido = pedido.copy()
        pedido.update(self.actiondict)
        # Seteamos los límites
        pedido = self.set_limits(pedido)
        # Comenzamos las llamadas a la API
        if continuar:
            lastContinue = {}
            acc = 0
            while True:
                acc += 1
                # Clone original request
                pedido2 = pedido.copy()
                # Modify it with the values returned in the 'continue' section of the last result.
                pedido2.update(lastContinue)
                # Call API
                result = requests.get('https://{}.wikipedia.org/w/api.php'.format(self.language),
                                    params=pedido2).json()
                if 'error' in result:
                    # Mepa que no queremos que se eleve un error porque eso
                    # interrumpe la ejecución
                    # raise Exception(result['error'])
                    print('ERROR:', result['error'])
                if 'warnings' in result:
                    print(result['warnings'])
                if 'query' in result:
                    r = result['query']
                    if 'pages' in r.keys():
                        print('# de páginas adquiridas: ', len(r['pages']))
                        print('# de links adquiridos:', count_items(r)[1])
                    yield r
                if 'batchcomplete' in result and result['batchcomplete']==True:
                    print('Batch completo!')
                if 'continue' not in result:
                    break
                lastContinue = result['continue']
            print('# de llamadas a la API:', acc)
        else:
            result = requests.get('https://{}.wikipedia.org/w/api.php'.format(self.language),
                                    params=pedido).json()
            if 'error' in result:
                # raise Exception(result['error'])
                print('ERROR:', result['error'])
            if 'warnings' in result:
                print(result['warnings'])
            if 'query' in result:
                return result['query']
            if 'batchcomplete' in result and result['batchcomplete']==True:
                print('Batch completo!')
    
    def get_data_pagesincat(self, category_name):
        """Obtiene todos los links y categorías correspondientes
        a todas las páginas que pertenecen a la categoría `category_name`.
        No obtiene nada relacionado con las subcategorías.
        """
        pedido = {'generator': 'categorymembers',
                  'gcmtitle': category_name,
                  'gcmtype': 'page',
                  'prop': 'links|categories'}
        data = {}
        set_of_cats = set()
        for result in self.query(pedido):
            pages = result['pages']
            n_pages_temp = len(pages)
            for i in range(n_pages_temp):
                title = pages[i]['title']
                if title not in data.keys():
                    # Si nunca pasamos por esta página, le creo
                    # un dict para que guarde allí los links luego
                    data[title] = {'links': [], 'categories': []}
                if 'links' in pages[i].keys():
                    # Si hay links para agregar, los agrego
                    linknames = [d['title'] for d in pages[i]['links']]
                    data[title]['links'] += linknames
                if 'categories' in pages[i].keys():
                    catnames = [d['title'] for d in pages[i]['categories']]
                    data[title]['categories'] += catnames
                    set_of_cats.update(set(catnames))
        print('# de páginas visitadas:', len(data.keys()))
        n_links = sum(len(data[title]['links']) for title in data.keys())
        print('# de links obtenidos en total:', n_links)
        return data, set_of_cats
                

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

if __name__ == '__main__':
    caza = CazadorDeDatos()
    # res1 = caza.query({'list': 'categorymembers', 'cmtype': 'page', 'cmtitle': 'Category:Physics'})
    # res2 = caza.query({'titles': 'Main page'})

    # res3 = caza.query({'titles': 'Physics', 'prop': 'links'}, continuar=False)
    # links_res3 = res3['pages'][0]['links']
    # nombres_links = [links_res3[i]['title'] for i in range(len(links_res3))]

    # res4 = caza.query({'titles': 'Physics', 'prop': 'links', 'generator': 'links'}, continuar=False)

    # res5 = caza.query({'gcmtitle': 'Category:Physics',
    #                    'prop': 'links',
    #                    'generator': 'categorymembers',
    #                    'gcmtype': 'page'
    #                    }, continuar=True)
    
    # res6 = caza.query({'gcmtitle': 'Category:Physics',
    #                    'generator': 'categorymembers',
    #                    'gcmtype': 'subcat'
    #                    }, continuar=False)

    # pedido = {'action':'query',
    #           'titles': 'Category:Physics',              
    #           'generator': 'links',
    #           'prop':'links|categories',
    #           'pllimit': '500',
    #           'redirects': '',
    #           }
    # resu = caza.query(pedido)

    data, cats = caza.get_data_pagesincat('Category:Interaction')
    data = curate_links(data)