import requests

def queryurl(lang, fmt, cmlimit, lst, cmtype, cmtitle):
    url = 'https://{}.wikipedia.org/w/api.php?action=query'.format(lang)
    url += '&format={}'.format(fmt)
    # Según https://www.mediawiki.org/wiki/API:Query, si el formato es
    # json o php entonces es mejor pedir formatversion=2
    if fmt == 'json':
        url += '&formatversion=2'
    url += '&cmlimit={}'.format(cmlimit)
    url += '&list={}'.format(lst)
    url += '&cmtype={}'.format(cmtype)
    url += '&cmtitle={}'.format(cmtitle)
    return url

def get_subcats(nombre, language='en', fmt='json', cmlimit=500, ids=False, continuar=True):
        cmtitle = 'Category:{}'.format(nombre)
        url = queryurl(language, fmt, cmlimit, 'categorymembers', 'subcat', cmtitle)
        el_json = requests.get(url).json()
        if continuar:
            pass
        if ids:
            subcats = [elem['pageid'] for elem in el_json['query']['categorymembers']]
        else:
            subcats = [elem['title'] for elem in el_json['query']['categorymembers']]
        return subcats

if __name__ == '__main__':
    # pruebas a manopla
    # resp = requests.get('https://en.wikipedia.org/w/api.php?action=query&format=json&list=categorymembers&cmtype=page&cmtitle=Category:Physics')
    # un_json = resp.json()
    # pages = requests.get('https://en.wikipedia.org/w/api.php?action=query&format=json&cmlimit=500&list=categorymembers&cmtype=page&cmtitle=Category:Physics').json()
    # subcats = requests.get('https://en.wikipedia.org/w/api.php?action=query&format=json&cmlimit=500&list=categorymembers&cmtype=subcat&cmtitle=Category:Physics').json()
    # subcats = subcats['query']['categorymembers']
    # algo = requests.get('https://en.wikipedia.org/w/api.php?action=query&format=json&cmlimit=500&list=categorymembers&cmtype=file&cmtitle=Category:Physics').json()
    una_url = queryurl('en', 'json', 500, 'categorymembers', 'subcat', 'Category:Physics')
    subcats_physics = get_subcats('Physics')
    subcats_physics_ids = get_subcats('Physics', ids=True)