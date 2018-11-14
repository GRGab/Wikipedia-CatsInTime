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
    def __init__(self, language='en', fmt='json', cmlimit=500):
        self.language = language
        self.format = fmt
        self.cmlimit = cmlimit

    def query(self, pedido):
        pedido['action'] = 'query'
        pedido['format'] = self.format
        pedido['cmlimit'] = self.cmlimit
        lastContinue = {}
        query_results = {}
        while True:
            # Clone original request
            pedido2 = pedido.copy()
            # Modify it with the values returned in the 'continue' section of the last result.
            pedido2.update(lastContinue)
            # Call API
            result = requests.get('https://{}.wikipedia.org/w/api.php'.format(self.language),
                                  params=pedido2).json()
            if 'error' in result:
                raise Exception(result['error'])
            if 'warnings' in result:
                print(result['warnings'])
            if 'query' in result:
                query_results.update(result['query'])
            if 'continue' not in result:
                break
            lastContinue = result['continue']
        return query_results
    


if __name__ == '__main__':
    caza = CazadorDeDatos()
    pedido = {'list': 'categorymembers', 'cmtype': 'page', 'cmtitle': 'Category:Physics'}
    resultado = caza.query(pedido)
