## Predicciones Taxis
---

El objetivo es entrenar un modelo para realizar predicciones sobre las medidas principales de los viajes en taxis amarillos en los diferentes barrios de NY. A continuación se muestra la lectura y procesamiento del archivo de taxis amarillos.

<p align="center">
<img src="../../Imagenes/1.png"  >
</p>



NOTA: De la misma forma se importaron
y procesaron los registros de taxis verdes

Los datos se procesan eliminando las columnas innecesarias
y registros que no corresponden.

<p align="center">
<img src="../Informe/Imagenes/2.png"  >
</p>


<p align="center">
<img src="../Informe/Imagenes/3.png"  >
</p>

## Creación de tabla pivote
--- 

Para los datos de los taxis amarillos (y verdes), se transformarán los datos usando una tabla pivote, donde el índice
Serán las fechas, y las columnas serán combinaciones de las medidas a predecir (cantidad de registros, suma y promedio
Del costo total y suma de la distancia recorrida), utilizando un fill_value de 0 y agregando los registros por suma, excepto
para los promedios que se calcularán en base a las sumas de total y las cantidades de registros.

<p align="center">
<img src="../Informe/Imagenes/4.png"  >
</p>

<p align="center">
<img src="../Informe/Imagenes/5.png"  >
</p>

<p align="center">
<img src="../Informe/Imagenes/6.png"  >
</p>



Debido a la cantidad de columnas, se planteó trabajar cada medida (cantidad de registros, suma de distancia, suma de costo, promedio de costo) en modelos separados, entrenando cada modelo sobre las series correspondientes a las medidas en cada uno de los barrios, tanto para los taxis amarillos como los verdes. Por tanto, se tienen 8 modelos con cinco series de datos cada uno.



## Diagramas de autocorrelación y autocorrelación parcial
---

Los diagramas ACF y PACF son utilizados para analizar la cantidad de lags adecuada para el entrenamiento de
la serie temporal. Los lags son los valores anteriores de la variable a considerar. En el caso de las predicciones
multiserie, los lags aplican para cada una de las variables como posible variable de entrada.


<p align="center">
<img src="../Informe/Imagenes/7.png"  >
</p>

<p align="center">
<img src="../Informe/Imagenes/8.png"  >
</p>

<p align="center">
<img src="../Informe/Imagenes/9.png"  >
</p>

<p align="center">
<img src="../Informe/Imagenes/10.png"  >
</p>

<p align="center">
<img src="../Informe/Imagenes/11.png"  >
</p>

<p align="center">
<img src="../Informe/Imagenes/12.png"  >
</p>


## Entrenamiento del modelo
---

Información acerca de los registros a utilizar.

<p align="center">
<img src="../Informe/Imagenes/13.png"  >
</p>

Para evaluar el modelo, se utilizará la métrica U de Theil,
que evalúa la bondad del ajuste del modelo a los datos
temporales en una escala de 0 a 1, donde menor es mejor.


<p align="center">
<img src="../Informe/Imagenes/14.png"  >
</p>


Finalmente, se comprueba que el índice esté en formato de tiempo.

<p align="center">
<img src="../Informe/Imagenes/15.png"  >
</p>

El modelo utilizado será un ForecasterAutoregMultiSeries, de la librería skforecast, que ajustará un
RandomForestRegressor a los datos temporales. La ventaja de este modelo es que permite automatizar la configuración de los lags necesarios para que el modelo aprenda la tendencia de los datos temporales, así como realizar una búsqueda en grid de las mejores combinaciones hiperparámetros y cantidad de lags, aprovechando la versatilidad y robustez del modelo de bosque aleatorio en este caso. Además, un forecaster multiserie permite entrenar el modelo para aprender distintas series temporales y sus posibles relaciones, por lo que en este caso se separarán las distintas medidas, entrenando un predictor multiserie para cada medida en los cinco barrios.

<p align="center">
<img src="../Informe/Imagenes/16.png"  >
</p>

<p align="center">
<img src="../Informe/Imagenes/17.png"  >
</p>

## Resultados de la búsqueda de hiperparámetros.
---

<p align="center">
<img src="../Informe/Imagenes/18.png"  >
</p>

<p align="center">
<img src="../Informe/Imagenes/19.png"  >
</p>

<p align="center">
<img src="../Informe/Imagenes/20.png"  >
</p>

<p align="center">
<img src="../Informe/Imagenes/21.png"  >
</p>

## Grid de resultados para la cantidad de viajes
---

<p align="center">
<img src="../Informe/Imagenes/22.png"  >
</p>

Los resultados se ordenan en base a los mejores puntajes U, es decir, los menores. En este caso, el mejor puntaje
se obtiene con cinco estimadores, una profundidad máxima de 8 y 14 lags

Con estos resultados se entrena el modelo resultante, y se le hacen pruebas con las siguientes métricas: MSE, MAE, Theil’s U. Cabe destacar que en algunos casos, las métricas U relacionadas a Staten Island arrojan resultados más altos que las otras series, debido a la relativamente poca cantidad de registros.

<p align="center">
<img src="../Informe/Imagenes/23.png"  >
</p>


<p align="center">
<img src="../Informe/Imagenes/24.png"  >
</p>

<p align="center">
<img src="../Informe/Imagenes/25.png"  >
</p>

El objetivo es entrenar un modelo para predecir los niveles de CO2 anuales en Nueva York. Debido a la relativamente poca cantidad de registros (datos anuales entre 1970 y 2021), se probarán modelos sencillos (Ridge, Árbol) aplicados a forecasting con skforecast. A continuación se muestra la información general.


<p align="center">
<img src="../Informe/Imagenes/26.png"  >
</p>

<p align="center">
<img src="../Informe/Imagenes/27.png"  >
</p>

<p align="center">
<img src="../Informe/Imagenes/28.png"  >
</p>

<p align="center">
<img src="../Informe/Imagenes/29.png"  >
</p>


## Autocorrelación y autocorrelación parcial
---

<p align="center">
<img src="../Informe/Imagenes/30.png"  >
</p>

<p align="center">
<img src="../Informe/Imagenes/31.png"  >
</p>

## Entrenamiento de los modelos con grid
---

### Para Ridge

<p align="center">
<img src="../Informe/Imagenes/32.png"  >
</p>

<p align="center">
<img src="../Informe/Imagenes/33.png"  >
</p>

<p align="center">
<img src="../Informe/Imagenes/34.png"  >
</p>

Para la regresión Ridge, la mejor combinación de parámetros fue 9 lags, Alpha de 0.01, intercepto en y a cero y solver “sparse_cg”.

### Para árbol

<p align="center">
<img src="../Informe/Imagenes/35.png"  >
</p>

<p align="center">
<img src="../Informe/Imagenes/36.png"  >
</p>

<p align="center">
<img src="../Informe/Imagenes/37.png"  >
</p>

Para el árbol de regresion, la mejor combinación de parámetros fue 2 lags, profundidad máxima de 10, mínimo de muestras por hoja de 1 y mínimo de muestras para split de 3.

### Ridge

<p align="center">
<img src="../Informe/Imagenes/38.png"  >
</p>

### Árbol

<p align="center">
<img src="../Informe/Imagenes/39.png"  >
</p>

Finalmente, al comparar ambos modelos, vemos que el Ridge logra un mejor desempeño entre las métricas de evaluación, así como un mejor acercamiento a los datos de prueba reales

<p align="center">
<img src="../Informe/Imagenes/40.png"  >
</p>

## Almacenamiento de los modelos
---

Los modelos fueron guardados en formato pickle, en una carpeta de un bucket de S3.

<p align="center">
<img src="../Informe/Imagenes/41.png"  >
</p>
