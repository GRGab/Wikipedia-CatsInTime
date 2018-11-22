from cazador import CazadorDeDatos

caza = CazadorDeDatos()
caza.get_cat_data('Category:Physics',
                  ['2015-10-01T12:00:00Z',
                   '2016-10-01T12:00:00Z',
                   '2017-10-01T12:00:00Z',
                   '2018-10-01T12:00:00Z'],
                  save_folder=r'C:\Users\Gabo\Documents\Facultad\datos_wikipedia\physics')