import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
plt.ion()
from time import time

from bs4 import BeautifulSoup as bs
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from sklearn.decomposition import TruncatedSVD as LSA
from scipy.spatial.distance import pdist, squareform

from sklearn.metrics import adjusted_mutual_info_score

from pc_path import definir_path
path_git, path_datos_global = definir_path()
from os.path import join as osjoin

from cazador import CazadorDeDatos
from utilities import curate_links
from generar_grafos import snapshot_to_graph
from clustering import calculate_infomap
from category_enrichment import enrich_mapping


def corpus_to_embedding(snapshot_data, ngram_range=(1,2)):
    ti = time()
    corpus = snapshot_data['texts']
    # Limpiamos todo lo que es HTML y nos quedamos con el texto (se podría hacer
    # algo mejor, eliminando secciones bizarras de la página, pero bueno)
    corpus = [bs(html_text, features="lxml").get_text().replace('\n', ' ')
              for html_text in corpus]
    # Convertir a vectores (esto puede tardar)
    # El resultado es una matriz esparsa
    print('Preprocesamiento:', int(time()-ti), 's'); ti = time()
    vectorizer = CountVectorizer(input='content', ngram_range=ngram_range,
                                 stop_words = "english")
    X = vectorizer.fit_transform(corpus)
    print('Vectorización:', int(time()-ti), 's'); ti = time()
    # Aplicar transformación TF IDF
    tfidf_transformer = TfidfTransformer(norm = 'l2')
    x_tfidf = tfidf_transformer.fit_transform(X)
    print('TF IDF:', int(time()-ti), 's')
    return x_tfidf

def embedding_to_graph(x_tfidf, snapshot_data, quantile, n_components,
                       n_iter=10, metric='cosine'):
    # Aplicar LSA
    ti = time()
    lsa = LSA(n_components = n_components, n_iter = n_iter, random_state = 0)
    lsa_data = lsa.fit(x_tfidf.T)
    print('LSA:', int(time()-ti), 's'); ti = time()
    # Calculamos las distancias
    embedding = lsa_data.components_.T
    distancias = pdist(embedding, metric=metric)
    matrix_distancias = squareform(distancias)
    # Matriz de adyacencia
    umbral = np.quantile(distancias, quantile)
    adjacency_lsa = np.array(matrix_distancias <= umbral, dtype=int)
    # Grafo
    graph_lsa = nx.from_numpy_matrix(adjacency_lsa, create_using=nx.Graph())
    label_mapping = {i : name for i, name in enumerate(snapshot_data['names'])}
    graph_lsa = nx.relabel_nodes(graph_lsa, label_mapping)
    print('Grafo creado:', int(time()-ti), 's')
    return graph_lsa

def semantic_analysis(snapshot_data, quantile, n_components, ngram_range=(1,2),
                      n_iter=10, metric='cosine'):
    # Limpieza de HTML + Vectorización + tf-idf
    x_tfidf = corpus_to_embedding(snapshot_data, ngram_range=ngram_range)
    # LSA + Cálculo de distancias + construcción del grafo
    graph_lsa = embedding_to_graph(x_tfidf, snapshot_data, quantile,
                                   n_components, n_iter=n_iter, metric=metric)
    return graph_lsa


def tune_LSA_dimension(snapshot_data, quantile, dimensions):
    # Se asume que snapshot_data ya ha sido curado y todo
    graph_ref = snapshot_to_graph(snapshot_data)
    graph_ref = graph_ref.subgraph(snapshot_data['names'])
    # Por motivos comparativos, nos quedamos con la compo gigante
    graph_ref = graph_ref.subgraph(max(nx.connected_components(nx.Graph(graph_ref)),
                               key=len))
    # Clusterizamos la referencia
    clusters_ref = calculate_infomap(graph_ref)
    # Realizamos el embedding de los textos
    embedding = corpus_to_embedding(snapshot_data)
    # Comparamos la clusterización de ref. con la realizada sobre grafos LSA
    n_dimvalues = len(dimensions)
    scores = np.zeros(n_dimvalues)
    for i in range(n_dimvalues):
        print('dim =', dimensions[i])
        # Construimos grafo LSA
        graph_lsa = embedding_to_graph(embedding, snapshot_data, quantile,
                                       dimensions[i])
        # Por motivos comparativos, nos quedamos con la compo gigante
        graph_lsa = graph_lsa.subgraph(max(nx.connected_components(nx.Graph(graph_lsa)),
                                   key=len))
        # Clusterizar el grafo
        clusters_lsa = calculate_infomap(graph_lsa)
        # Para comparar clusters, me quedo con los nodos compartidos
        common_nodes = set(graph_ref.nodes).intersection(set(graph_lsa.nodes))
        labels_ref, labels_lsa = [], []
        for node in common_nodes:
            labels_ref.append(graph_ref.nodes[node]['infomap'])
            labels_lsa.append(graph_lsa.nodes[node]['infomap'])
        # Obtener info mutua normalizada y ajustada
        score = adjusted_mutual_info_score(labels_ref, labels_lsa)
        scores[i] = score
    i_max = np.argmax(scores)
    print('El valor de dimensión con score más alto fue dim =', dimensions[i_max])
    return scores