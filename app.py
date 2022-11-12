import pyorient

# https://github.com/mogui/pyorient/issues/270
HOST = "orientdb"
PORT = 2424
DATABASE_NAME = "pythonDB"

# !!! Pendiente crear otro usuario
DB_USER = "root"
DB_PWD = "root_passwd"

try:
    print("Intentando conectar a la BD...")
    client = pyorient.OrientDB(HOST, PORT)

    session_id = client.connect(DB_USER, DB_PWD)
    print("SessionID=", session_id)

except:
    print("!!! Conexión a la BD fallida.")


if client.db_exists(DATABASE_NAME, pyorient.STORAGE_TYPE_MEMORY):

    print(f"Ya existía la BD '{DATABASE_NAME}'.")
    client.db_open(DATABASE_NAME, DB_USER, DB_PWD)

else:
    print(f"No existe la BD '{DATABASE_NAME}', intentando crearla...")

    try:
        client.db_create(
            DATABASE_NAME,
            pyorient.DB_TYPE_DOCUMENT,
            pyorient.STORAGE_TYPE_MEMORY,
        )
    except pyorient.PYORIENT_EXCEPTION as err:

        print(f"!!! Error al crear la BD: {err}")
        exit

CLASS_NAME = "ejemplo"
print(f"Crear Clase '{CLASS_NAME}'.")
client.command(f"CREATE CLASS {CLASS_NAME}")

print("Insertar elementos en Clase creada.")
client.command(f'INSERT INTO {CLASS_NAME} SET item="python", version="3.11-alpine"')
client.command(f'INSERT INTO {CLASS_NAME} SET item="OrientDB", version="3.0"')
client.command(f'INSERT INTO {CLASS_NAME} SET item="pyorient", version="1.5.1"')

print("Insertar elementos que sigan estructura distinta.")
client.command(f'INSERT INTO {CLASS_NAME} SET item="python", version="3.11-alpine"')
client.command(f'INSERT INTO {CLASS_NAME} SET item="OrientDB", version="3.0"')
client.command(f'INSERT INTO {CLASS_NAME} SET item="pyorient", version="1.5.1"')

# Cerrar la conexion
# client.shutdown(DB_USER, DB_PWD)
