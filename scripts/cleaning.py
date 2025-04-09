import sqlite3

#Pistas
# En este paso la idea sería quitar duplicados, manejar nulos, pero como no es el objetivo, 
# Vamos a hacer una copia espejo de los datos, simulando que los datos ya están limpios.
# 1.Conectarse a la base de datos ecommerce.db ubicada en /opt/airflow/dags/data
# 2: Elimine la tabla Silver si ya existe, cree una tabla nueva Silver copiando 
#    todo el contenido de su tabla Bronze correspondiente
#    Cada bloque debe hacer una copia de la tabla Bronze a una nueva tabla Silver
# 3: Guardar los cambios y cerrar la conexión
# 4: Usa print() para mostrar el estado del proceso

def cleaning_data():
    db_path = '/opt/airflow/dags/data/ecommerce.db'
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("🔄 Iniciando proceso de limpieza (Silver)...")

        # Tablas a copiar de Bronze a Silver
        tables = ["orders", "customers", "products"]

        for table in tables:
            bronze_table = f"bronze_{table}"
            silver_table = f"silver_{table}"

            # Eliminar la tabla Silver si ya existe
            cursor.execute(f"DROP TABLE IF EXISTS {silver_table}")

            # Crear la tabla Silver como copia de la Bronze
            cursor.execute(f"CREATE TABLE {silver_table} AS SELECT * FROM {bronze_table}")

            print(f"✅ Tabla {silver_table} creada a partir de {bronze_table}")

        # Guardar cambios
        conn.commit()
        print("✅ Proceso de limpieza completado con éxito.")

    except Exception as e:
        print(f"❌ Error en cleaning_data: {e}")

    finally:
        if conn:
            conn.close()
            print("🔚 Conexión cerrada.")

