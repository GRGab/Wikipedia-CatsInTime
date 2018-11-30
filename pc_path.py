import socket
def definir_path(): 
    if socket.gethostname() == 'Gabo-Spectre':
        path_git = r'C:\Users\Gabo\Documents\Facultad\wikipedia-proyecto'
        path_datos_global = r'C:\Users\Gabo\Documents\Facultad\datos_wikipedia'
    elif socket.gethostname() == 'gabo-desktop':
        path_git = '/home/gabo/Documents/Facultad-local/wikipedia-proyecto/'
        path_datos_global = '/home/gabo/Documents/Facultad-local/datos_wikipedia'
    elif socket.gethostname() == 'matias-Satellite-A665':
        path_git = '/home/matias/Documentos/Facultad/Redes/wikipedia-proyecto/'
        path_datos_global = '/home/matias/Documentos/Facultad/Redes/datos_wikipedia'
    elif socket.gethostname() == 'DESKTOP-URTP413':
        path_git = r'C:\Users\chagu\Desktop\Matias\Redes\wikipedia-proyecto'
        path_datos_global = r'C:\Users\chagu\Desktop\Matias\Redes\datos_wikipedia'
    return path_git, path_datos_global
