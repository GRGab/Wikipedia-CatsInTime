import numpy as np                                  #for large and multi-dimensional arrays
import matplotlib.pyplot as plt
plt.ion()

from sklearn.feature_extraction.text import CountVectorizer          #For Bag of words
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer #For TF-IDF
from sklearn.decomposition import TruncatedSVD as LSA

from pc_path import definir_path
path_git, path_datos_global = definir_path()
from os.path import join as osjoin
from cazador import CazadorDeDatos
from utilities import curate_links

from bs4 import BeautifulSoup as bs
from nltk import word_tokenize, sent_tokenize # útil para ver resultados intermedios

# ??
import warnings
warnings.filterwarnings("ignore")                     #Ignoring unnecessory warnings

### Imports no empleados
# import nltk                                         #Natural language processing tool-kit
# from nltk.corpus import stopwords                   #Stopwords corpus
# from nltk.stem import PorterStemmer                 # Stemmer

# from gensim import corpora, models, similarities, matutils
# from gensim.models.word2vec import Word2Vec
# from gensim.models import Word2Vec                                   #For Word2Vec
# from gensim.models import KeyedVectors
# from gensim.matutils import cossim
# from gensim.utils import deaccent
# from tqdm import tqdm
# from sklearn import manifold
# from collections import defaultdict

caza = CazadorDeDatos()
carpeta = osjoin(path_datos_global, 'machine_learning')
data_raw, children = caza.cargar_datos(carpeta)
data = curate_links(data_raw)
dates = list(data.keys())

# Elegimos un snapshot para bosquejar el análisis
data = data[dates[3]]
corpus = data['texts']
# Limpiamos todo lo que es HTML y nos quedamos con el texto (se podría hacer
# algo mejor, eliminando secciones bizarras de la página, pero bueno)
corpus = [bs(html_text).get_text().replace('\n', ' ') for html_text in corpus]

# Convertir a vectores (esto puede tardar)
# El resultado es una matriz esparsa
vectorizer = CountVectorizer(input='content',ngram_range = (1,2), stop_words = "english")
X = vectorizer.fit_transform(corpus)

# Aplicar transformación TF IDF
tfidf_transformer = TfidfTransformer(norm = 'l2')
x_tfidf = tfidf_transformer.fit_transform(X)

# Aplicar LSA
lsa = LSA(n_components = 20, n_iter = 10, random_state = 0)
lsa_data = lsa.fit(x_tfidf.T)

# Visualizar proyecciones sobre un espacio 3d
from mpl_toolkits.mplot3d import Axes3D 
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i, punto in enumerate(lsa_data.components_.T):
    ax.scatter(punto[0],punto[1],punto[2])
plt.show()

# Funcion para calcular distancias
from scipy.spatial.distance import pdist, squareform
embedding = lsa_data.components_.T
distancias = pdist(embedding, metric = 'cosine')
# distancias_2 = pdist(embedding, metric ='cityblock')
# distancias_3 = pdist(embedding, metric = 'euclidean')
matrix_distancias = squareform(distancias)

# Elijo un umbral, mirando el hist de distancias entre páginas,
# y obtengo la matriz de adyacencia
umbral = 0.4
adjacency_lsa = np.array(matrix_distancias <= umbral, dtype=int)

# Genero grafo no dirigido
import networkx as nx
graph_lsa = nx.from_numpy_matrix(adjacency_lsa, create_using=nx.Graph())
# Asignamos nombres a los nodos
label_mapping = {i : name for i, name in enumerate(data['names'])}
graph_lsa = nx.relabel_nodes(graph_lsa, label_mapping)
# Asignamos categorías de subcats
from funciones_analisis import enrich_visitedcats_snapshot
enrich_visitedcats_snapshot(graph_lsa, data, children)

nx.write_gexf(graph_lsa, osjoin(path_git, 'Grafos_guardados', 'prueba_lsa.gexf'))