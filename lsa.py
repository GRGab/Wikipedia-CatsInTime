import numpy as np
import matplotlib.pyplot as plt
plt.ion()

from bs4 import BeautifulSoup as bs
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from sklearn.decomposition import TruncatedSVD as LSA

from pc_path import definir_path
path_git, path_datos_global = definir_path()
from os.path import join as osjoin
from cazador import CazadorDeDatos
from utilities import curate_links

from scipy.spatial.distance import pdist, squareform

caza = CazadorDeDatos()
carpeta = osjoin(path_datos_global, 'machine_learning')
data_raw, children = caza.cargar_datos(carpeta)
data = curate_links(data_raw)
dates = list(data.keys())

def semantic_analysis_snapshot(snapshot_data, n_components=20, n_iter=10,
                               ngram_range=(1,2), metric='cosine', umbral=1.2):
    corpus = snapshot_data['texts']
    # Limpiamos todo lo que es HTML y nos quedamos con el texto (se podría hacer
    # algo mejor, eliminando secciones bizarras de la página, pero bueno)
    corpus = [bs(html_text).get_text().replace('\n', ' ') for html_text in corpus]
    # Convertir a vectores (esto puede tardar)
    # El resultado es una matriz esparsa
    vectorizer = CountVectorizer(input='content', ngram_range=ngram_range, stop_words = "english")
    X = vectorizer.fit_transform(corpus)
    # Aplicar transformación TF IDF
    tfidf_transformer = TfidfTransformer(norm = 'l2')
    x_tfidf = tfidf_transformer.fit_transform(X)
    # Aplicar LSA
    lsa = LSA(n_components = n_components, n_iter = n_iter, random_state = 0)
    lsa_data = lsa.fit(x_tfidf.T)
    # Calculamos las distancias
    embedding = lsa_data.components_.T
    distancias = pdist(embedding, metric=metric)
    matrix_distancias = squareform(distancias)
    # Matriz de adyacencia
    adjacency_lsa = np.array(matrix_distancias >= umbral, dtype=int)
    # CONTINUAR