EXAMEN FINAL - Aplicaciones Distribuidas
Red social PowerESFOT: MySQL + Spring Boot + NGINX + MapReduce
=================================================================

ESTRUCTURA
----------
proyecto/
├── docker-compose.yml
├── db/
│   └── redes.sql              (tabla "redes" + 260 interacciones de prueba)
├── app/                       (Spring Boot - se usa para server1 y server2)
│   ├── Dockerfile
│   ├── pom.xml
│   └── src/main/java/com/poweresfot/demo/
│       ├── DemoApplication.java
│       ├── model/Interaccion.java
│       ├── repository/InteraccionRepository.java
│       └── controller/DatosController.java
├── nginx/
│   └── nginx.conf             (balanceo round-robin server1/server2)
└── mapreduce/
    ├── Dockerfile
    ├── preparador.sh          (descarga datos + fragmenta)
    ├── mapper.py               (fase Map)
    └── reducer.py              (fase Reduce, calcula las 6 metricas)


PASO 1 - Levantar todo
-----------------------
docker compose up --build -d

Esto ejecuta EN ORDEN automaticamente:
  1. mysql (carga redes.sql como volumen)
  2. server1 y server2 (esperan a que mysql este "healthy")
  3. nginx (balanceador, espera a server1 y server2)
  4. preparador (descarga /datos vía nginx y los fragmenta en 4 partes)
  5. mapper1, mapper2, mapper3, mapper4 (procesan cada fragmento EN PARALELO)
  6. reducer (junta todo y calcula las metricas finales)

Espera unos 60-90 segundos (la primera vez tarda mas por el build de Maven).


PASO 2 - Verificar que MySQL cargo los datos
----------------------------------------------
docker exec -it mysql-redes mysql -u root -ppassword -e "USE redes_db; SELECT COUNT(*) FROM redes;"

Debe mostrar 260.


PASO 3 - Verificar el endpoint /datos y el balanceo
------------------------------------------------------
curl -i http://localhost:8080/datos | head -5

Repite el comando varias veces y observa el header "X-Servidor":
curl -s -D - http://localhost:8080/servidor -o /dev/null | grep -i servidor

Debe alternar entre "server1" y "server2".


PASO 4 - Verificar el pipeline MapReduce
--------------------------------------------
Ver logs de cada etapa:
docker logs preparador
docker logs mapper1
docker logs reducer

El resultado final queda en mapreduce/resultado.txt (en tu carpeta local,
porque el volumen esta montado). Tambien se imprime en:
docker logs reducer


PASO 5 - Metricas que debe mostrar el resultado.txt
--------------------------------------------------------
1. Video mas visto
2. Video con mas likes
3. Video mas comentado
4. Usuario mas recurrente
5. Hora con mas interaccion
6. Video con mayor Ratio de Interaccion = (likes+comments+shares)/views


PASO 6 - Volver a correr el MapReduce (sin reconstruir todo)
------------------------------------------------------------------
Si quieres volver a ejecutar solo el pipeline de MapReduce:

docker compose run --rm preparador bash preparador.sh
docker compose run --rm mapreduce python mapper.py splits/part_00.txt
docker compose run --rm mapreduce python mapper.py splits/part_01.txt
docker compose run --rm mapreduce python mapper.py splits/part_02.txt
docker compose run --rm mapreduce python mapper.py splits/part_03.txt
docker compose run --rm mapreduce python reducer.py


COMANDOS UTILES
----------------
docker ps                     ver contenedores activos
docker compose down -v        apagar todo y borrar volumenes (reset total)
docker compose up --build -d  levantar todo de nuevo
docker logs nombre_contenedor ver logs de cualquier servicio


PARA EL INFORME (segun la rubrica)
----------------------------------------
1. Descripcion general del sistema (usa el diagrama del examen: MySQL -> Spring
   Boot -> Load Balancer -> server1/server2 -> Hadoop/MapReduce -> Resultados)
2. Capturas de:
   - docker ps mostrando los 9 contenedores corriendo
   - curl al endpoint /datos mostrando texto plano
   - curl repetido mostrando el header X-Servidor alternando
   - docker logs reducer mostrando las 6 metricas
   - contenido de resultado.txt
3. Conclusiones: interpretar que dice el ratio de interaccion (un video con
   pocas vistas pero muchos likes/comments/shares tiene un ratio alto, lo que
   indica alta calidad de contenido relativa a su alcance) y recomendaciones
   (ej. promocionar mas los videos con ratio alto pero pocas vistas).
