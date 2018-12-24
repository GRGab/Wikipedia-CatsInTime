# Wikipedia CatsInTime

Este repositorio fue creado para el proyecto final de la materia "Redes Complejas com aplicaciones a Biología de Sistemas", dictada por Ariel Chernomoretz en el Departamento de Física de la Facultad de Ciencias Exactas y Naturales (FCEN) de la Universidad de Buenos Aires (UBA) durante el segundo cuatrimestre de 2018.

El objetivo del proyecto fue estudiar la estructura de una región relativamente pequeña de la enciclopedia online Wikipedia en inglés, en el cual se buscó caracterizar la evolución en el tiempo de la estructura de categorías. Para esto, se realizó un análisis de clusterización o detección de comunidades mediante el algoritmo [Infomap](http://www.mapequation.org) complementado con un análisis semántico de texto. El cuerpo de datos empleado consistió en información sobre 3667 entradas de la Wikipedia en inglés correspondiente a cuatro instantes de tiempo en el período 2015-2018. La información fue obtenida mediante un proceso de búsqueda en anchura sobre el grafo de categorías de Wikipedia, partiendo de las categorías semilla Machine learning
(Aprendizaje de máquina) y Statistics (Estadística).

El análisis principal se realizó sobre dos representaciones en términos de grafos de la región de Wikipedia bajo estudio: una red dirigida de hipervínculos y un grafo "semántico", no dirigido, obtenido mediante [Latent Semantic Analysis](https://en.wikipedia.org/wiki/Latent_semantic_analysis) (LSA). Ambos grafos fueron construidos para cada instante de tiempo y se analizó su evolución en el tiempo.
