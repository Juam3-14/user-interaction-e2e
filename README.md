-----README------
Dependencias instaladas definidas en requirements.txt
Pasos de instalación:
1) Crear venv para instalación de dependencias:
python3 -m venv venv

2) Levantar venv para utilizar como entorno de desarrollo
source venv/scripts/activate

3) Instalar dependencias
pip install -r requirements.txt

4) Ejecutar aplicación con fastAPI
fastapi dev main.py

5) Acceder a swaggerUI para una interfaz visual de prueba de los endpoints:
http://127.0.0.1:8000/docs#/ => O la dirección IP que esté configurada como default


Documentación de la api realizada utilizando FasAPI framework para documentación automática (ver en SwaggerUI)

sda
Decisiones de Diseño:
Las principales decisiones fueron las siguientes:
- Distribución de la lógica: Estructurar las 3 etapas de procesamiento de datos reflejadas en los 3 endpoints (Procesar Evento, Procesar User Story, Generar Test) con clases, implementando como herramienta para validar tipos y formatos tanto en los endpoints como en las clases, de pydantic heredando de la clase BaseModel. De esta forma la asignación de responsabilidades se realiza de manera cohesiva. Hay cosas para mejorar aún, tanto en asignación de responsabilidades como en la manera de ejecutar código. Así, la estructura del proyecto queda separado en la carpeta models, que separa por módulos estas 3 "áreas" de implementación, "events_module", "stories_module" y "test_module"; la carpeta resources, que funciona como medio de almacenamiento de los recursos estáticos del proyecto, ya que opté por guardar la info de eventos en archivos json en local, debido a que es más facil que armar otro tipo de estructura de almacenamiento y permite ir liberando memoria en caso de ser necesario al tener levantada la app, consumiendo estos datos a demanda; carpeta routers que contiene un archivo routers_v1 que incluye los endpoints de esta implementación (la idea es separar en archivos, por responsabilidad de dominio/negocio todos los endpoints que sean necesarios, escalando horizontalmente); la carpeta tests que tiene un objetivo similar a resources, pero contiene archivos ejecutables .py generados dinámicamente a partir de los eventos/US, y los demás archivos del proyecto (gitignore, main, readme, requirements)
- Elegir que campos eran importantes para elaborar las US a partir de los eventos: Basándome en el ejemplo de US de la documentación, interpreté que la información más importante a obtener a partir del evento es la relacionada al accionar del usuario y la identificación del elemento/componente con el que el usuario interactúa, permitiendo así tener info que permita no solo diferenciar una US de otra, sino un paso dentro de esa US de los demás pasos que la componen.
- Elegir el criterio que define el alcance de una US. Para esta implementación encontré que podía realizarse con los campos "current_url" y validando con el timestamp, asumiendo que no deberían llegar eventos de la misma US con más de un minuto de diferencia.

Trade-offs considerados:
En toda solución de software los principales recursos a someter a un proceso de priorización son Tiempo de Ejecución, Recursos Computacionales (memoria) y Complejidad en el Código. En este caso, para una implementación sencilla, intenté reducir los tiempos de ejecución al mínimo, con iteraciones de complejidad O(n) en el peor de los casos ya que tampoco era necesario más, y mantener la memoria de ejecución también en lo mínimo posible, utilizando generadores e iteradores para analizar un elemento a la vez dentro de una lista, evitando llenar la memoria con datos que no van a estar utilizándose en ese instante. Con respecto a la complejidad del código, intenté mantener un código simple y fácilmente entendible, aunque me llevara más tiempo de escritura, ya que el objetivo es que sea legible y comprensible con poco esfuerzo (esta también es una razón por la que implementé el POO al momento de estructurar los elementos de información en clases)

Áreas de Mejora:
- Administración de lógica dentro de los métodos de cada endpoint: Pueden escribirse mejor las implementaciónes de la lógica dentro de cada uno de estos endpoints, abstrayendo el comportamiento en clases/métodos y de esta forma restringir únicamente al método ejecutado en el endpoint a las funciones dentro de la lógica https y nada de lógica de dominio/autenticación.
- Método de Generación de Test-Cases: Este método está hecho muy "hardcode", armando dinámicamente el test-case pero directamente como un string concatenado. Podría mejorarse manejando el código generado con funciones que reciban args y kwargs, complejizando el código pero simplificando la lógica. Además, al no haber ejecutado el código obtenido, no tengo certezas de que sean totalmente ejecutables, pero si comparten el formato de la documentación que he revisado, por lo que para esta implementación lo considero "suficiente", y más al haber sido generados a partir de un dataset de prueba.