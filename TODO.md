# Adquisición

- Modificar update_data y get_pages_incat para que puedan levantar revids y timestamps de distintas
revisiones para cada página
- Hacer función que, partiendo de una lista de revids, obtenga links|categories|text para cada uno.
Que los vaya almacenando en disco (formato json?)
- Adquirir y almacenar nombre|timestamp|links|categories|text para cada revid.

# Análisis

## Preliminar
- Caracterizar y visualizar grafo de hipervínculos en función del tiempo-

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


## Clustering
- Definir los clusters según categorías
- Elegir algoritmo de clustering automático según algún criterio
- POSIBLE: aplicar algoritmo de clustering tanto sobre red de hipervínculos como sobre
red generada por LSA.
- Aplicar clusterings, guardar etiquetas, comparar
- Estudiar evolución en el tiempo