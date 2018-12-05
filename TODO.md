# Adquisición

- Terminar de adquirir Statistics, Neuroscience, Physics

# Análisis

## Preliminar
- Caracterizar y visualizar grafo de hipervínculos en función del tiempo.
- Hacer distribuciones de grado (¿O no?)

## Clustering
- Definir los clusters según categorías
- Elegir algoritmo de clustering automático según algún criterio
- POSIBLE: aplicar algoritmo de clustering tanto sobre red de hipervínculos como sobre
red generada por LSA.
- Aplicar clusterings, guardar etiquetas, comparar
- Estudiar evolución en el tiempo

## Texto
- Función que parsee el texto de las cosas que nos devuelve action=parse con módulo oldid
(asegurarse de que es HTML, por ejemplo)
- Preprocesamiento para LSA, copiándose un poco del grupo de Marian
    - Eliminar stopwords
    - ID-RFS o como se llame
    - Etcétera
- LSA propiamente dicho
- Aplicar medida de distancia (e.g. distancia coseno) y convertir a similaridad
- Definir grafo mediante umbral de similaridad. Visualizar, caracterizar

# 02/12/18 19:02
- Optimizar dim LSA para quantile=0.005
- Generar grafos LSA para quantile=0.005

# 05/12/18 11:32
Ya está todo lo de antes. Solo queda mirar los grafos, generarlos bien lindos
y analizar los resultados!