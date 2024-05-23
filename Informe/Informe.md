## Introducción
---

Como empresa especializada en análisis de datos, nos complace presentar nuestro informe para respaldar su decisión de inversión en el sector del transporte urbano. Utilizando datos detallados de servicios de taxis y viajes compartidos en Nueva York, nuestro análisis examina la viabilidad y el impacto ambiental de incorporar vehículos eléctricos a su flota. Con enfoque en la calidad del aire, la contaminación sonora y otros factores clave, nuestro objetivo es proporcionar una evaluación sólida y fundamentada para guiar su estrategia de inversión hacia un futuro más sostenible. 
 

## Metodología de trabajo
---

Para realizar el análisis de los datos relacionados con el transporte de pasajeros, seguimos una metodología estructurada que abarca varias etapas. Comenzamos con la extracción y transformación de datos, seguida de la identificación de posibles anomalías y la preparación del conjunto de datos. Además, creamos un modelo de machine learning que nos permite predecir el crecimiento del transporte de pasajeros en un período determinado, así como la incidencia de la contaminación ambiental y sonora asociada a este medio de transporte. 

### 1. Transformación de la Base de Datos a DataFrames:
- Se procedió a descargar las bases de datos necesarias para el desarrollo del análisis integral
- Se trabajo tanto en forma local, implementado tecnologías como Python para el manejo de las tablas relacionadas con la contaminación acústica, ambiental y el clima, así como la producción de CO2 en la ciudad de New York.
- Para el trabajo en la nube el equipo de científicos e ingenieros de datos procedieron a trabajar con  SQL para el manejo de las tablas, para el almacenamiento y posterior tratamiento de las bases de datos que hacen referencia al transporte de taxis amarillos y taxis verdes.

### 2. Exploración de los Datos
- Se desarrollo un EDA primario con la finalidad de poder entender las respectivas bases de datos que teníamos enfrente, y a partir de este análisis primario empezamos a vislumbrar la calidad de los datos y que bases de datos aportaría mas información valiosa para poder orientar en la toma de decisión a la hora de proponer la inversión a desarrollar.

### 3. Ciclo de vida del dato

imagenes ciclo de vida

## Análisis Exploratorio de Datos
---

Una vez procesado nuestros datos, procedemos a analizarlos con la finalidad de poder extraer conclusiones que nos permitan generar recomendaciones basadas en evidencia que contribuyan a tomar la mejor decisión a la hora de invertir.

### Evolución del costo en función del tiempo

grafica costo en funcion del tiempo

De la presente grafica podemos destacar que, aunque existe una variabilidad el el valor del costo de transporte, esto a lo largo del periodo estudiado se mantiene cuasi constante, esto nos dice que no vemos tendencia alcista al costo del transporte o tendencia a la baja, señalando una gran confiabilidad a la hora de predecir ganancias al largo plazo.

### Viajes en función del tiempo

grafica Viajes en función del tiempo

La cantidad de viajes que se realizan, es un factor importante  a la hora de poder buscar alguna medición que nos permita entender como crece o se expande el negocio del transporte urbano. De lo obtenido por los datos podemos apreciar que el negocio del transporte de pasajeros aunque es un negocio de gran volumen se a mantenido sin cambios significativos en el periodo de dos años, mostrándonos una señal de poco crecimiento, esto mas la poca variabilidad del costo del transporte, son indicios de una inversión que no en primera instancia no vera retribuciones fructíferas en el corto plazo.

### Cantidad de viajes por barrio

grafica Cantidad de viajes por barrio

El siguiente grafico nos sirve para poder entender en mayor profundidad de los cinco barrios mas destacados de la ciudad de New York, cual es el mas congestionado, esto es solo para poder entender y ver si se puede empezar a proyectar un negocio mas local que brinde servicios en una primera instancia en áreas mas reducidas con el fin de poder enfocarnos en aquellas zonas mas demandadas.


### Distancias en función de tiempo

grafica Distancias en función de tiempo

Una vez mas podemos destacar poca variación en el tipo de negocio del transporte urbano, donde las distancias recorridas a los largo de los años se mantiene prácticamente constante, exceptuando pequeños periodos de tiempos donde se muestra una clase de fluctuación, pero en general estos datos nos sirven para reafirma que es un negocio donde no se correrán riesgos a corto plazo.

### Promedio mensual de presencia de motores

grafica Promedio mensual de presencia de motores

El gráfico de líneas proporciona una visualización clara y concisa del comportamiento de los ruidos emitidos por vehículos en la ciudad de Nueva York a lo largo del tiempo. Observamos que la frecuencia promedio de ocurrencia de los diferentes tipos de motores varía mensualmente, lo que sugiere fluctuaciones en la actividad vehicular y posiblemente en los patrones de tráfico en la ciudad. Este análisis nos ayuda a comprender mejor la dinámica del ruido urbano y puede ser útil para identificar tendencias a lo largo del tiempo y desarrollar estrategias efectivas para la gestión del ruido en áreas urbanas.

### Presencia de contaminante por año

grafica Presencia de contaminante por año

Aunque se observa una tendencia a la disminución de los niveles de contaminantes, con excepción de ozono, estos aún mantienen valores preocupantes para el medio ambiente. Es imperativo buscar soluciones para abordar esta crisis medioambiental. La inversión en vehículos eléctricos emerge como una innovadora y prometedora alternativa para mitigar este problema, ofreciendo una oportunidad tangible para reducir nuestra huella ambiental y avanzar hacia un futuro más sostenible.

### Emisiones de CO2 en New York

grafica Emisiones de CO2 en New York

De la grafica podemos entender el comportamiento de  la emisión de CO2 en la ciudad de New York, de la cual se extrae que año a año por motivos que exceden a este estudio se puede notar un descenso en la producción de este gas de invernadero, aunque los valores van en un decrecimiento no dejan de estar en niveles muy altos dado el contexto actual del calentamiento global y los problemas que derivan de este.

### Variación del clima a lo largo del tiempo

grafica Variación del clima a lo largo del tiempo

Otro análisis a considerar es la temperatura ambiente, la cual de diversas fuentes, como https://www.renault.es/blog/trucos-consejos/calor-coche-electrico.html, aclaran que el rendimiento de la autonomía de los vehículos eléctricos se ve afectada por la temperatura del exterior, que análisis desarrollado por la compañía de autos RENAULT podemos ver que las temperaturas mínimas del invierno, como las máximas del verano son temperaturas no favorables para la vida optima del la batería, estas condiciones podrían ocasionar una baja del rendimiento y en consecuencia menos disponibilidad del vehículo para un día de trabajo.

### Ubicación de cargadores para autos eléctricos

grafica ubicación de cargadores para autos eléctricos

Por ultimo es necesario a la hora de evaluar la adquisición de una flota de vehículos eléctricos la disponibilidad de puestos de carga de estos, es esencial poder invertir en un negocio en el cual estén dadas todas las condiciones para poder brindar un buen servicio. Es por esta razón que la escasa distribución de los cargadores eléctricos en toda la ciudad de New York presenta un problema a la hora de pensar en la logística de viajes largos. Dada esta situación se podría primero plantear en una inversión local solo asignada para el barrio de Manhattan, pensando en un una posible expansión a medida que mas cargadores eléctricos sean distribuido a otras localidades, asegurando la continuidad del servicio.

## Indicadores Clave de Rendimiento (KPIs): Herramientas para Medir y lograr una buena inversión
---

Un Indicador Clave de Rendimiento (KPI), es una métrica cuantitativa utilizada para evaluar el rendimiento en relación con objetivos específicos. En nuestro caso, buscamos analizar la oportunidad de invertir en el negocio del transporte urbano, con la finalidad de poder estimar la implementación de vehículos eléctricos a la flota en cuestión. Los KPIs son herramientas esenciales en la gestión, ya que proporcionan una medida clara y objetiva del progreso hacia el logro de los objetivos y nos permiten tomar decisiones informadas y estratégicas.

### KPI 1: Incremento de Viajes en Taxis
El número de viajes en taxis realizados aumenta en un 5% respecto al mes anterior, reflejando un crecimiento en la demanda de transporte urbano.

imagen KPI 1

### KPI 2: Variación de CO2 en Estados Unidos 
Se observa un incremento del 5% en los niveles de dióxido de carbono (CO2) en la ciudad de New York con respecto al año anterior, lo que sugiere un posible impacto en la calidad del aire y destaca la necesidad de soluciones más sostenibles.

imagen KPI 2

### KPI 3: Adopción de Taxis Verdes
La proporción de taxis eléctricos o 'verdes' en la flota de vehículos de transporte urbano cumple con el 5% de incremento establecido en un periodo de 1 mes, demostrando una transición hacia opciones más ecológicas y sostenibles en el transporte de pasajeros.


imagen KPI 3


## Conclusiones
El análisis exhaustivo en de los datos sobre contaminación acústica y ambiental, ademas del análisis sobre el clima y las consecuencias directas sobre la flota de vehículos eléctricos, ademas del análisis sobre el transporte de taxis en la ciudad de New York, revelan una serie de hallazgos cruciales a la hora de abordar la toma de decisiones sobre una inversión en la flota de vehículos eléctricos para el transporte urbano. 
Dada la complejidad del problema se plantean en lineas generales ver si el negocio es lo suficientemente rentable como para cubrir la cobertura total del servicio. Las graficas sobre costo  en función del tiempo y viajes función del tiempo nos muestran un escenario no muy alentador a la hora de esperar un modelo de negocio que crezca permanentemente, es mas se muestra una muy leve fluctuación, por el negocio es estacionario,  siempre acotado.
Por otro lado se analiza la fiabilidad del servicio considerando los punto de recarga de los vehículos como su desempeño a lo largo de un año enfrentando las adversidades del clima, estos dos factores son determinantes porque se presentan una concentración de cargadores solo en el barrio de Manhattan, no así en el resto de barrios, y las temperaturas bajas que presentan en invierno hacen que la implementación de vehículos eléctricos se vea muy mermada a la hora de elegirlos como principal fuente de transporte, teniendo en cuenta de la grafica de distancias recorridas en función del tiempo nos muestra distancias de entre 40 a 80 millas en promedio dependiendo el barrio y en la actualidad los vehículos eléctricos no tiene mayor autonomía de 200 millas, esto se traduce que solo haciendo viajes cortos en un día solo se podrían hacer no mas de 4 viajes entre cargas, considerando que la carga promedio es de 6 horas, dependiendo del vehículo y cargador. 
Por ultimo tomando en cuenta nuestros indicadores, podemos notar que ninguno de los tres cumple con las condiciones esperadas, esto es fácil de explicar debido a que año tras año hay un descenso de las emisiones de gases de invernadero en la ciudad de New York. Por otro lado el modelo de negocio analizado anteriormente muestra que tanto el aumento de viajes como los costos se mantiene siempre acotados, esto se refleja en el poco aumento de los viajes en taxis, también afectando a los ya existentes taxis eléctricos.
Por todo lo mencionado anteriormente como equipo de asesores recomendamos no invertir en la ampliación de la flota hacia vehículos eléctricos para el transporte urbano en la ciudad de New York.
