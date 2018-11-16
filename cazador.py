import requests
import numpy as np
import networkx as nx
#%%
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
    def __init__(self, language='en', fmt='json', data_limit=500,
                 generator_limit=5):
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

    def query(self, pedido, continuar=True, verbose=True):
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
                    if verbose and 'pages' in r.keys():
                        print('# de páginas adquiridas: ', len(r['pages']))
                        print('# de links adquiridos:', count_items(r)[1])
                    yield r
                if verbose and 'batchcomplete' in result and result['batchcomplete']==True:
                    print('Batch completo!')
                if 'continue' not in result:
                    break
                lastContinue = result['continue']
            if verbose:
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
            if verbose and 'batchcomplete' in result and result['batchcomplete']==True:
                print('Batch completo!')
    
    def get_data_pagesincat(self, category_name, data=None):
        """Obtiene todos los links y categorías correspondientes
        a todas las páginas que pertenecen a la categoría `category_name`,
        y los agrega a la información provista con el input data.

        El input data permite evitar guardar dos veces los mismos datos.

        No obtiene nada relacionado con las subcategorías.
        """
        pedido = {'generator': 'categorymembers',
                  'gcmtitle': category_name,
                  'gcmtype': 'page',
                  'prop': 'links|categories'}
        # Si se provee el parámetro data, queremos copiar la info
        # para no modificar el input inplace.
        if data is None:
            data = {}
        else:
            data = data.copy()
        # Set de todas las categorías encontradas
        set_of_cats = set()

        # Comienza el pedido de datos
        for result in self.query(pedido):
            pages = result['pages']
            n_pages_temp = len(pages)
            for i in range(n_pages_temp):
                title = pages[i]['title']
                # Si la página ya fue visitada antes, entonces
                # no queremos volver a guardar esa información
                if title not in data.keys():
                    # dict para que guarde allí la info
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

    def get_cat_data(self, category_name, data=None):
        """
        Dada una categoria, devuelve un diccionario anidado y un set de categorias.
        El diccionario continene como keys todas las paginas dentro de la
        categoria y las paginas dentro de las subcategorias que yacen en la 
        categoria en cuestion (category_name). Dentro de cada key existe otro
        diccionario que contiene las categorias a las que pertenece cada
        articulo y los links de las paginas a las que
        direcciona el articulo. El set de categorias lo utilizaremos 
        como atributos de los nodos en el futuro. """
        pedido_subcats = {'generator': 'categorymembers',
                          'gcmtitle': category_name,
                          'gcmtype': 'subcat'}
        
        # Guardamos la info de las páginas que están en category_name
        data, set_of_cats = self.get_data_pagesincat(category_name, data=data)

        # Ahora hacemos la llamada recursiva, pidiendo que se aplique
        # esta misma función sobre cada subcategoría de category_name
        for result in self.query(pedido_subcats, verbose=False):
            pages = result['pages']
            for i in range(len(pages)):
                subcat = pages[i]['title']
                data_rec, set_rec = self.get_cat_data(subcat, data=data)
                data.update(data_rec)
                set_of_cats.update(set_rec)
        return data, set_of_cats
    
   

    def get_cat_tree(self, category_name, verbose=True):
        """
        Función recursiva que intenta obtener el árbol de categorías
        partiendo de una categoría raíz. Las categorías de Wikipedia
        no conforman un árbol. Esto quiere decir que puede haber
        nodos repetidos y podría llegar a fallar la ejecución debido
        a un loop infinito.

        Returns
        -------
        tree : dict
            Diccionarios anidados con la estructura de las categorías
        n_l : int
            Número de llamadas realizadas a la función get_cat_tree
        """
        print('Comienza una llamada')
        pedido = {'generator': 'categorymembers',
                  'gcmtitle': category_name,
                  'gcmtype': 'subcat'}
        tree = {category_name: {}}
        n_l = 1
        for result in self.query(pedido, verbose=False):
            pages = result['pages']
            for i in range(len(pages)):
                subcat = pages[i]['title']
                # Si ya pasamos por esta categoría en este nivel
                # del árbol, entonces no hacemos nada.
                if subcat not in tree.keys():
                    subtree, n_l_rec = self.get_cat_tree(subcat, verbose=verbose)
                    tree[category_name].update(subtree)
                    n_l += n_l_rec
        print('Termina una llamada. # subcats:', len(tree[category_name].keys()))
        return tree, n_l
    
            
            
    def tree2list(self, arbol):
        '''
        OJO: Falta hacer!
        A partir del diccionario anillado de Categorias, creo una lista
        de todas las categorias que aparecen para iterarlas posteriormente.
        '''
        pass
    
    def get_tree_data(self, category_name, data=None):
        '''
        OJO: Antes de usarla tiene que estar andando la funcion tree2list!
        Vamos a utlizar el arbol de categorias como semillero para las funciones
        buscadoras de datos. Devuelve una lista donde cada elemento es el
        diccionario de data para una categoria diferente.
        '''
        pedido_subcats = {'generator': 'categorymembers',
                          'gcmtitle': category_name,
                          'gcmtype': 'subcat'}
        
        arbol, _ = self.get_cat_tree(pedido_subcats)
        lista= self.tree2list(arbol)
        # Ahora hacemos la llamada recursiva, pidiendo que se aplique
        # esta misma función sobre cada subcategoría de category_name
        lista_de_pasadas = []
        for i in lista:
            data = self.get_cat_data(i)
            lista_de_pasadas.append(data)
        return lista_de_pasadas
    
    
                
####### Funciones por fuera de la clase
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

#Quiza borrarlo, Gabo ya lo borro
#def nestdict_to_edgelist(nestdict):
#    """
#    Función recursiva.
#    Dada una estructura de diccionarios anidados, devolver la lista de enlaces
#    dirigidos que señalan qué nodos son hijos de quién.
#    """
#    edgelist = []
#    # Debería haber un solo nodo en nestdict, pero aún así la sintaxis del loop
#    # me resulta cómoda
#    assert len(nestdict) == 1
#    root = list(nestdict.keys())[0]
#    children = nestdict[root].keys()
#    child_dicts = nestdict[root].values()
#    edgelist += [(root, child) for child in children]
#    subtrees = [{child: child_dict} for child, child_dict in zip(children, child_dicts)]
#    for subtree in subtrees:
#        edgelist += nestdict_to_edgelist(subtree)
#    return edgelist
#%%
if __name__ == '__main__':
    # Inicializamos objeto
    caza = CazadorDeDatos()
    #%%
    ### Prueba de get_data_pagesincat
    data_1, cats = caza.get_data_pagesincat(
        'Category:Zwitterions'
#        'Category:Ions'
#        'Category:Interaction'
#        'Category:Physics'
            )
    data_1 = curate_links(data_1)
    #%%
    
    ### Prueba de get_cat_data
    data, cats = caza.get_cat_data(
        'Category:Zwitterions'
#         'Category:Ions'
#        'Category:Interaction'
#        'Category:Physics'
        )
    data = curate_links(data)

    # ### Árbol súper chico de categorías
#    arbol, n_l = caza.get_cat_tree('Category:Zwitterions')
    # ### Árbol no tan chico
    arbol, n_l = caza.get_cat_tree('Category:Ions')
    # ### Árbol más grande
    # arbol, n_l = caza.get_cat_tree('Category:Interaction')
    #%%
    lista = caza.get_tree_data(
        'Category:Zwitterions'
#         'Category:Ions'
#        'Category:Interaction'
#        'Category:Physics'
        )
    

#%%
#    # Ejemplos de búsquedas que se pueden realizar mediante el método query
#    # Los objetos resultantes son generadores, i.e. al ejecutar este código,
#    # no se realiza ninguna llamada a la API sino que eso se posterga hasta
#    # que se itere sobre alguno de los objetos.
    res1 = caza.query({'list': 'categorymembers', 'cmtype': 'page', 'cmtitle': 'Category:Physics'})
#    res2 = caza.query({'titles': 'Main page'})
#    res3 = caza.query({'titles': 'Physics', 'prop': 'links'}, continuar=False)
#    res4 = caza.query({'titles': 'Physics', 'prop': 'links', 'generator': 'links'}, continuar=False)
#    res5 = caza.query({'gcmtitle': 'Category:Physics',
#                       'prop': 'links',
#                       'generator': 'categorymembers',
#                       'gcmtype': 'page'
#                       }, continuar=True)
#    res6 = caza.query({'gcmtitle': 'Category:Physics',
#                       'generator': 'categorymembers',
#                       'gcmtype': 'subcat'
#                       }, continuar=False)
