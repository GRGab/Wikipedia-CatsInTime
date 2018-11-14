import requests as req

def queryurl(lang, fmt, cmlimit, lst, cmtype, cmtitle):
    url = 'https://{}.wikipedia.org/w/api.php?action=query'.format(lang)
    url += '&format={}'.format(fmt)
    url += '&cmlimit={}'.format(cmlimit)
    url += '&list={}'.format(lst)
    url += '&cmtype={}'.format(cmtype)
    url += '&cmtitle={}'.format(cmtitle)
    return url

class CazadorDeDatos():
    def __init__(self, language='en', fmt='json', cmlimit=500):
        self.language = language
        self.format = fmt
        self.cmlimit = cmlimit

    def get_subcats(self, nombre, ids=False):
        cmtitle = 'Category:{}'.format(nombre)
        url = queryurl(self.language, self.format, self.cmlimit,
                       'categorymembers', 'subcat', cmtitle)
        el_json = req.get(url).json()
        if ids:
            subcats = [elem['pageid'] for elem in el_json['query']['categorymembers']]
        else:
            subcats = [elem['title'] for elem in el_json['query']['categorymembers']]
        return subcats

    def get_pages(self, nombre):
        pass
    


if __name__ == '__main__':
    # pruebas a manopla

    resp = req.get('https://en.wikipedia.org/w/api.php?action=query&format=json&list=categorymembers&cmtype=page&cmtitle=Category:Physics')
    # un_json = resp.json()
    # pages = req.get('https://en.wikipedia.org/w/api.php?action=query&format=json&cmlimit=500&list=categorymembers&cmtype=page&cmtitle=Category:Physics').json()
    # subcats = req.get('https://en.wikipedia.org/w/api.php?action=query&format=json&cmlimit=500&list=categorymembers&cmtype=subcat&cmtitle=Category:Physics').json()
    # subcats = subcats['query']['categorymembers']
    # algo = req.get('https://en.wikipedia.org/w/api.php?action=query&format=json&cmlimit=500&list=categorymembers&cmtype=file&cmtitle=Category:Physics').json()

    # Pruebas de la clase

    una_url = queryurl('en', 'json', 500, 'categorymembers', 'subcat', 'Category:Physics')
    caza = CazadorDeDatos()
    subcats_physics = caza.get_subcats('Physics')
    subcats_physics_ids = caza.get_subcats('Physics', ids=True)