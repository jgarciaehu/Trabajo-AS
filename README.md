# Trabajo-AS

_Autor: Jon García Beaskoetxea_

El objetivo principal de este trabajo era poner en práctica los conocimientos teóricos adquiridos durante la asignatura sobre técnicas de gestión y orquestración de contenedores.

En este documento se busca dar instrucciones a comandos relevantes dentro del trabajo. Se recomienda también revisar la documentación, ya que esta contiene puntualizaciones relevantes.

*NOTA*: es posible que los comandos necesiten ser ejecutados con privilegios, esto se consigue añadiendo *sudo* al inicio de ellos.

## Crear imagen del cliente

Estando en el mismo directorio que el fichero _Dockerfile_ se ejecuta el siguiente comando (importante el '.' al final):

```bash
docker build .
```

Alternativamente se puede crear la imagen especificando un nombre.

```bash
docker build . -t "<nombre-imagen>"
```

Se suele recomendar agregar el usuario al inicio, separado de una '/' con el nombre de la imagen. Esto es útil para poder subir la imagen a Docker Hub:

```bash
docker build . -t "<usuario-docker-hub>/<nombre-imagen>"
```

## Subir la imagen a Docker Hub

Se crea un repositorio en [Docker Hub](https://hub.docker.com) con el mismo nombre que la imagen.

Si no se ha seguido la recomendación del apartado anterior sobre llamar a la imagen con el usuario y el nombre de la imagen, se puede cambiar el nombre de la imagen con:

```bash
docker tag <nombre-imagen>:<tag> <nombre-repositorio>:<tag>
```

Por último se sube la imagen con:

```bash
docker push <nombre-repositorio>:<tag>
```

## Desplegar Docker Compose

Estando en el mismo directorio que el fichero _docker-compose.yml_ se ejecuta el siguiente comando:

```bash
docker compose up
```

Como se indica en la documentación, se puede emplear el parámetro _-d_ para ejecutarlo en segundo plano, pero ver el texto de salida en primer plano es de gran utilidad para ver el estado del script.

### Acceder a OrientDB

Una vez se ha lanzado el Docker Compose y este ha empezado a crear los contenedores, se puede acceder al contenedor de OrientDB para ver los resultados.

Para ser precavidos, conviene esperar a que termine de ejecutarse el script _app.py_ del contenedor del cliente, esto se puede ver en los mensajes de la terminal que crea el cliente.

Los pasos son los siguientes:

1. Abrir otra terminal y ejecutar el siguiente comando para ver los contenedores en ejecución actualmente:

```bash
docker ps
```

2. Fijarse en el contenedor que corresponde al servicio de OrientDB, y copiar su ID de contenedor.

3. Para abrir una terminal dentro del contenedor, ejecutar lo siguiente sustituyendo _ID_ por el ID del contenedor obtenido anteriormente:

```bash
docker exec -it <ID> /bin/sh
```

4. Para abrir la consola de OrientDB, ejecutar:

```bash
./bin/console.sh
```

5. Conectarse a la base de datos con:

```sql
CONNECT remote:localhost root root_passwd
```

6. Ejecutar lo siguiente para ver si se ha podido acceder correctamente:

```sql
LIST DATABASES
```

Si en la salida se ve 'pythonDB' se ha accedido correctamente. Si menciona que faltan permisos, algo ha salido mal :/

7. Conectarse a la base de datos que crea el cliente Python:

```sql
CONNECT remote:localhost/pythonDB root root_passwd
```

8. En este punto se puede probar a listar la clase que ha introducido el cliente, y ver si es correcto:

```sql
SELECT * FROM miClase
```

Si la salida es lo siguiente, ha ido todo bien:

```text
+----+-----+-------+-----------+--------+
|#   |@RID |@CLASS |version    |item    |
+----+-----+-------+-----------+--------+
|0   |#11:0|miClase|3.0        |OrientDB|
|1   |#11:1|miClase|1.5.1      |pyorient|
|2   |#11:2|miClase|3.11-alpine|python  |
+----+-----+-------+-----------+--------+
```

También se puede probar a ir a [localhost](localhost:80) o la dirección de la máquina y el puerto 80 y ver si la página web está disponible.

### Finalizar despliegue

Para terminar la ejecución del despliegue de Docker Compose, en caso de haberlo iniciado con el parámetro _-d_, el comando es:

```bash
docker compose down
```

Alternativamente si se ha seguido el consejo de no ejecutar en segundo plano, vale con pulsar la combinación de teclas 'Ctrl + C' en el terminal, y este hará que todos los contenedores se detengan.

## Desplegar Kubernetes

Para el despliegue en Kubernetes, se describen los comandos a ejecutar.

Estando en el mismo directorio que los ficheros YAML (.yml), se recomienda que el orden de los objetos sea:

1. ClusterIP:

```bash
kubectl apply -f orientdb-cluster-ip-service.yml
```

2. PersistentVolume:

```bash
kubectl apply -f volumen-persistente.yml
```

3. PersistentVolumeClaim:

```bash
kubectl apply -f reclamacion.yml
```

4. Deployment de OrientDB:

```bash
kubectl apply -f deployment-orientdb.yml
```

5. Deployment de Cliente:

```bash
kubectl apply -f deployment-cliente.yml
```

### Finalizar despliegue Kubernetes

Al destruir los objetos creados en el despliegue se puede seguir cualquier orden. Sin embargo, se recomienda seguir el orden inverso al del creación.

En los comandos solo cambia que en lugar de _apply_ es _delete_, el resto queda igual.

Por ejemplo, el primer comando sería:

```bash
kubectl delete -f deployment-cliente.yml
```
