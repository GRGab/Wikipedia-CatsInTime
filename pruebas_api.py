import requests as req

#%%
resp = req.get('https://en.wikipedia.org/w/api.php?action=query&format=json&list=categorymembers&cmtype=page&cmtitle=Category:Physics')
un_json = resp.json()

#%%
pages = req.get('https://en.wikipedia.org/w/api.php?action=query&format=json&cmlimit=500&list=categorymembers&cmtype=page&cmtitle=Category:Physics').json()
subcats = req.get('https://en.wikipedia.org/w/api.php?action=query&format=json&cmlimit=500&list=categorymembers&cmtype=subcat&cmtitle=Category:Physics').json()
subcats = subcats['query']['categorymembers']
algo = req.get('https://en.wikipedia.org/w/api.php?action=query&format=json&cmlimit=500&list=categorymembers&cmtype=file&cmtitle=Category:Physics').json()

#%%
def get_subcats(nombre, ids=False):
    url = 'https://en.wikipedia.org/w/api.php?action=query&format=json&cmlimit=500&list=categorymembers&cmtype=subcat&cmtitle=Category:'
    url = url + nombre
    el_json = req.get(url).json()
    if ids:
        subcats = [elem['pageid'] for elem in el_json['query']['categorymembers']]
    else:
        subcats = [elem['title'] for elem in el_json['query']['categorymembers']]
    return subcats
    
subcats_physics = get_subcats('Physics')
subcats_physics_ids = get_subcats('Physics', ids=True)