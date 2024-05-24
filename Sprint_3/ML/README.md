# Modelos de Machine Learning a entrenar

- Predicción de cantidad de viajes, suma de distancia, suma de costo total y promedio de costo total para cada barrio en taxis amarillos.
- Predicción de cantidad de viajes, suma de distancia, suma de costo total y promedio de costo total para cada barrio en taxis verdes.
- Predicción de niveles de CO2.

# Selección de características

En los casos de los modelos de taxis, se realizó una tabla pivote sobre las diferentes medidas a estudiar (cantidad de registros, suma de distancia, suma de costo total, promedio de costo total) para cada uno de los barrios (Bronx, Brooklyn, Manhattan, Queens, Staten Island), versus los días. De esta forma, tanto el dataframe de los taxis amarillos como de taxis verdes quedaron con las siguientes columnas:

- Cantidad de registros en Bronx.
- Cantidad de registros en Brooklyn.
- Cantidad de registros en Manhattan.
- Cantidad de registros en Queens.
- Cantidad de registros en Staten Island.
- Suma de distancia recorrida en Bronx.
- Suma de distancia recorrida en Brooklyn.
- Suma de distancia recorrida en Manhattan.
- Suma de distancia recorrida en Queens.
- Suma de distancia recorrida en Staten Island.
- Suma de costo total en Bronx.
- Suma de costo total en Brooklyn.
- Suma de costo total en Manhattan.
- Suma de costo total en Queens.
- Suma de costo total en Staten Island.
- Promedio de costo total en Bronx.
- Promedio de costo total en Brooklyn.
- Promedio de costo total en Manhattan.
- Promedio de costo total en Queens.
- Promedio de costo total en Staten Island.



En cuanto al dataframe de CO2, solamente tenía las columnas correspondientes al año y al total de emisiones, por lo que no se hizo ningún procesamiento.

![output](https://github.com/eremohn/huella_de_carbono_en_NYC/assets/51429745/7ced95ef-f784-45c9-81a2-cdbaa965d25b)

# Selección del modelo

## Modelos de taxis
<p>Para los modelos, se utilizó la librería skforecast, que permite adaptar modelos de regresión de Scikit-Learn, redes neuronales y otros, a datos en series temporales. Esta adaptación es necesaria porque en estas series de datos, los valores de un momento determinado son dependientes de los valores de la variable de estudio en momentos anteriores (lags). Esta librería se escogió por las siguientes razones: </p>

- Permite realizar una optimización de parámetros basada en búsqueda por grid, sobre los parámetros del modelo planteado y sobre la cantidad de lags a considerar.
- Permite, como en este caso, entrenar el modelo con más de una serie de valores relacionados. Esto es útil dado que en algunos casos, la variable estudiada es influenciada no sólo por sus propios valores en el tiempo, sino también por los valores de otra u otras variables. Esta característica se aprovechará para estudiar las medidas estadísticas entre los diferentes barrios.
- Dado a que puede utilizar modelos que normalmente no responden adecuadamente a parámetros temporales complejos, aprovecha las ventajas de los mismos en series temporales. En este caso, se escogió el modelo RandomForest por su robustez y versatilidad, al poder entrenar varios subconjuntos de columnas para elegir la mejor adaptación posible.

<br>Dado que entrenar un único modelo para todas las series sería demasiado costoso, se entrenará un modelo por cada conjunto de medidas en los diferentes barrios. Por último, cabe mencionar que se utilizaron los diagramas de autocorrelación y autocorrelación parcial para estudiar y determinar las mejores posibles cantidades de lags:</p>

- Para los taxis amarillos, se entrenaron modelos con 5, 7, 8, 10, 14 y 15 lags.
- Para los taxis verdes, se entrenaron modelos con 5, 7, 8, 9, 11 y 14 lags.

Aparte del número de lags, los modelos se entrenaron con profundidades de los árboles de entre 4 y 15 niveles y con números de estimadores de 5, 10, 20, 50 y 100. Los resultados obtenidos fueron:

- Para cantidad de viajes en taxis amarillos: 14 lags, 5 estimadores, profundidad máxima de 8.
- Para suma de distancia en taxis amarillos: 14 lags, 50 estimadores, profundidad máxima de 9.
- Para suma de total en taxis amarillos: 14 lags, 9 estimadores, profundidad máxima de 12.
- Para promedio de total en taxis amarillos: 10 lags, 5 estimadores, profundidad máxima de 15.
- Para cantidad de viajes en taxis verdes: 14 lags, 20 estimadores, profundidad máxima de 8.
- Para suma de distancia en taxis verdes: 14 lags, 10 estimadores, profundidad máxima de 12.
- Para suma de total en taxis verdes: 7 lags, 5 estimadores, profundidad máxima de 10.
- Para promedio de total en taxis verdes: 7 lags, 100 estimadores, profundidad máxima de 15.

Para más detalle, ver notebooks de entrenamiento: [Taxis amarillos](EntrenamientoModelosBoroughY.ipynb), [Taxis verdes](EntrenamientoModelosBoroughG.ipynb).

## Modelo de CO2
Se utilizó skforecast para evaluar predictores basados en la regresión Ridge y en un árbol de decisión. Las gráficas ACF y PACF sugieren que los mejores lags en su mayoría son de 9 o menos, 14 y 20. Considerando que 20 lags podrían sobreajustar el modelo, solo se exploraron hasta 14 lags.
<p>La búsqueda en grid para la regresión Ridge arrojó que el mejor resultado se logra con 9 lags, un alpha de 0.01, intercepto en 0 y solver sparse_cg.
<p>Por otra parte, la búsqueda en grid para el árbol de decisión arrojó que el mejor resultado se logra con 2 lags, una profundidad máxima de 10, un mínimo de muestras en hoja de 1 y un mínimo de muestras para split de 3.
<p>Comparando los resultados, vemos que las predicciones del modelo Ridge, aunque por poco, se acercan más a los datos reales y tienen mejores métricas de evaluación.
  
![image](https://github.com/eremohn/huella_de_carbono_en_NYC/assets/51429745/715b8f2a-33f1-4dea-950a-0dccd0523b58)
![image](https://github.com/eremohn/huella_de_carbono_en_NYC/assets/51429745/92395c5a-bdb2-4b3d-a432-8fa28eef9618)

# Automatización
Se instanció una imagen de Docker con el código a ejecutar y las librerías necesarias en EC2. El código es el presentado en los notebooks, con algunos cambios necesarios para la automatización del proceso y la conexión a S3, donde se guardan los archivos a usar. En el [Dockerfile](Dockerfile) se configuran los comandos CRON para ejecutar los archivos los días 7 de cada mes, con ventanas de 3 horas, y en el archivo [requirements](requirements.txt) se especifican las librerías a ejecutar.

![image](https://github.com/eremohn/huella_de_carbono_en_NYC/assets/51429745/160835e1-c79c-4ea3-9865-1ec64ec75b26)
![image](https://github.com/eremohn/huella_de_carbono_en_NYC/assets/51429745/27095f92-bcec-4a2d-b796-e7381216ed45)
