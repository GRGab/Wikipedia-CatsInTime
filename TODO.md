# Adquisición

- Función que toma una lista de fechas 'fechas', los revids y los timestamps correspondientes a una única página y selecciona una cantidad len(fechas) de pares (revid, timestamp) sobre los cuales se harán posteriores llamadas a la API.

- Mejoras en get_cat:
    - Separar procesamiento de cada nodo en un nuevo método
    - Guardar periódicamente en un json, guardando allí un parámetro 'continue' que permite continuar con la ejecución de la búsqueda desde el último lote guardado luego de una interrupción cualquiera del código (ctrl+C o alguna otra excepción.)
    - El json debe tener nombre|timestamp|links|categories|text para cada revid de cada página. Y además los valores continue.

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