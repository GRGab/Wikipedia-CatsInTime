from cazador import CazadorDeDatos

carpeta=r'C:\Users\chagu\Desktop\Matias\Redes\wikipedia-proyecto\neuroscience'
caza = CazadorDeDatos()
caza.get_cat_data('Category:Neuroscience',
                  ['2015-10-01T12:00:00Z',
                   '2016-10-01T12:00:00Z',
                   '2017-10-01T12:00:00Z',
                   '2018-10-01T12:00:00Z'],
                   save_folder=carpeta,
                   retomar=caza.retomar(carpeta))