import pyorient
from datetime import datetime
import os

HOST = "orientdb"
PORT = 2424
DATABASE_NAME = "pythonDB"
DB_USER = "root"  # !!! Pendiente crear otro usuario
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
client.command(f'INSERT INTO {CLASS_NAME} SET item="OrientDB", version="3.0"')
client.command(f'INSERT INTO {CLASS_NAME} SET item="pyorient", version="1.5.1"')

print("Insertar elementos que sigan estructura distinta.")
client.command(f'INSERT INTO {CLASS_NAME} SET lenguaje="java", usado=False')
client.command(
    f'INSERT INTO {CLASS_NAME} SET lenguaje="python", usado=True, version="3.11-alpine"'
)

print(f'Exportando una copia de la base de datos "{DATABASE_NAME}"')
path = f"/files/export/{DATABASE_NAME}"
if not os.path.exists(path):
    os.makedirs(path)
fechaHora = datetime.now().strftime("%d-%m_%H:%M")
client.command(f"EXPORT DATABASE /files/export/{DATABASE_NAME}/{fechaHora}.export")

# Cerrar la conexion
# client.shutdown(DB_USER, DB_PWD)
