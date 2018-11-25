# Análisis Machine Learning

## 2018-11-24

### Grafos recién salidos del horno

- Tamaño de los grafos resultantes: 18762, 20330, 22656, 23839 en orden cronológico.
- Estos grafos son un poco malos por 2 razones:
    - Incluyen páginas que no son tales (templates, etc.)
    - Incluyen a todas las páginas que no son de la categoría inicial pero son
    linkeadas por una que sí lo es. Lo malo de esto es que la conectividad que
    vamos a ver para esas páginas es falsa (simplemente no adquirimos sus enlaces)
- La red va creciendo en el tiempo, en enlaces y en nodos
- De 2017 a 2018 Hay una bajada en el kin y kout máximos, al revés que lo que
pasaba antes
- Ni el clustering medio ni la transitividad tienen una tendencia monótona
- Son débilmente conexos salvo por 2 nodos sueltos.
- No son fuertemente conexos (esto es obvio debido a cómo están construidos)

### Curación de los grafos

- Eliminamos links malos (que empiezan con prefijos malos, onda 'Template:' etc.)
De esta manera se eliminaron 4713, 4984, 5477, 6000 links en orden cronológico.
- Tamaño de los grafos resultantes: 17572, 19036, 21185, 22265 en orden cronológico.
Notar que el "# de links eliminados" no quiere decir "# de enlaces eliminados
en la red".
- Luego de eliminar todas las categorías internas de Wikipedia, los sets_of_cats
pasan de ~2000 categorías a ~1200.
- De todas formas, esto no es de gran interés debido a que no podemos filtrar los
nodos que no queremos a través de una lista negra de categorías: no tenemos
información detallada sobre los nodos que no pertenecen a la categoría original.
- Restringí a hacer grafos solo con las páginas de las categorías que visitamos
(grafos "originalcat"). Obtengo grafos de 1003, 1065, 1125, 1183 nodos y
9023, 11322, 12521, 14793 enlaces. Como consecuencia del podado de nodos externos
a la categoría (los cuales presentan una conectividad artificialmente baja),
los clusterings medios y transitividades aumentan significativamente (más aún
el primero que el segundo, posiblemente debido a cómo se definen en grafos
dirigidos?).
- Ahora la diferencia entre el grafo total y la componente conexa es un poco
más pronunciada, pero se va achicando con el tiempo. En 2018 es de 23 nodos
mientras que en 2015 es de 67.

## Elección de categorías de interés

- Luego de mirar un rato las enormes listas de categorías presentes en el grafo,
me di cuenta de que las categorías que probablemente nos interesen van a ser
las que aparecieron en el árbol de categorías recorrido, es decir las que
aparecen en la estructura 'children'. Siento que tal vez las otras no nos sirvan
de demasiado, al menos en lo referido a las clusterizaciones...
- Lo primero que hice fue asignarle a cada nodo su subcategoría, es decir
la subcategoría en la cual fue encontrado al adquirir los datos de Wikipedia.
Esto es súper interesante para explorar gráficamente con Gephi.
- Una tercera forma, bastante interesante, sería fijar el nivel de profundidad
en el árbol dado por 'children' y particionar a todas las páginas según las
subcats presentes únicamente en ese nivel. Esto queda PENDIENTE.