import sqlite3
import os

# Pistas 
# 1. Conectarse a la base de datos donde están las tablas Silver 
# 2. Guarda los queries realizados en el trabajo pasado como un string => Gold

def transform_data():
    db_path = '/opt/airflow/dags/data/ecommerce.db'
    # Conexión a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print("🚀 Ejecutando queries para crear tablas Gold...")

    # Query 1: Top 10 estados con mayor ingreso
    query1 = """
    DROP TABLE IF EXISTS gold_top_states;
    CREATE TABLE gold_top_states AS
    SELECT state, SUM(total_amount) AS total_income
    FROM silver_orders
    GROUP BY state
    ORDER BY total_income DESC
    LIMIT 10;
    """

    # Query 2: Comparación de tiempos reales vs estimados por mes y año
    query2 = """
    DROP TABLE IF EXISTS gold_delivery_comparison;
    CREATE TABLE gold_delivery_comparison AS
    SELECT 
        strftime('%Y-%m', delivery_date) AS month_year,
        AVG(actual_delivery_days) AS avg_actual_days,
        AVG(estimated_delivery_days) AS avg_estimated_days
    FROM silver_orders
    GROUP BY month_year
    ORDER BY month_year;
    """
    
    #TODO ELiminar la tabla si existe gold_top_states, gold_delivery_comparison
    


    print("🚀 Ejecutando queries para crear tablas Gold...")
    cursor.executescript(query1)
    cursor.executescript(query2)

    conn.commit()
    conn.close()
    print("✅ Tablas Gold creadas en ecommerce.db: 'gold_top_states' y 'gold_delivery_comparison'")
