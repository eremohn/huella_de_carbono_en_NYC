<p align="center">
<img src="Imagenes_2/banner_2_sprint.png" width="996" height="344""  >
</p>

### Proceso ETL
---

<p align="center">
<img src="Imagenes_2/ETL-Trips.gif"  >
</p>

### Ciclo de vida del dato
---

<p align="center">
<img src="Imagenes_2/Ciclo_del_dato.jpg"  >
</p>

- Buckets: Utiliza buckets de almacenamiento de objetos en AWS S3 para almacenar conjuntos de datos y archivos necesarios para el análisis.
- AWS Glue ETL: Emplea AWS Glue para realizar tareas de extracción, transformación y carga (ETL) de datos, lo que le permite preparar los datos para su análisis.
- AWS Athena: Realiza consultas a través de AWS Athena para acceder y analizar los datos almacenados en el catálogo de AWS Glue, lo que le brinda capacidades de consulta SQL en datos estructurados y no estructurados.
- AWS QuickSight: Utiliza AWS QuickSight como una herramienta de visualización de datos para crear y compartir paneles interactivos y visualizaciones que ayudan en el análisis y la toma de decisiones.

<p align="center">
<img src="Imagenes_2/Ciclo_del_dato_BigData.jpg"  >
</p>

- Docker: Crea contenedores para almacenar la información y las aplicaciones necesarias para el análisis de datos. Docker proporciona un entorno consistente y portátil para ejecutar aplicaciones.
- ECR (Elastic Container Registry): Utiliza ECR para almacenar y gestionar imágenes de contenedor Docker. ECR actúa como un repositorio privado seguro para las imágenes de contenedor.
- Fargate: Despliega las imágenes de contenedor registradas en ECR utilizando AWS Fargate, un servicio de computación sin servidor que permite ejecutar contenedores Docker sin necesidad de aprovisionar o administrar servidores.
- ALB (Application Load Balancer): Utiliza un ALB para controlar el tráfico de red hacia las aplicaciones desplegadas en Fargate, asegurando que el acceso a las aplicaciones sea seguro y confiable y protegiendo contra posibles amenazas de seguridad.



### Diseño modelo de datos
---

<p align="center">
<img src="Imagenes_2/modelo_ER.jpeg"  >
</p>

### Infraestructura de datos
---

<p align="center">
<img src="Imagenes_2/Architecture_01.jpg"  >
</p>

### Automatización y carga incremental
---
