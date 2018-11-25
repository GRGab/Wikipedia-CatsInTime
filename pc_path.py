import socket
def definir_path(): 
    if socket.gethostname() == 'Gabo-Spectre':
        path_git = r'C:\Users\Gabo\Documents\Facultad\wikipedia-proyecto'
        path_datos_global = r'C:\Users\Gabo\Documents\Facultad\datos_wikipedia'
    elif socket.gethostname() == 'gabo-desktop':
        path_git = '/home/gabo/Documents/Facultad-local/wikipedia-proyecto/'
        path_datos_global = '/home/gabo/Documents/Facultad-local/datos_wikipedia'
    elif socket.gethostname() == 'matias-Satellite-A665':
        pass
    elif socket.gethostname() == 'DESKTOP-URTP413':
        pass
    return path_git, path_datos_global