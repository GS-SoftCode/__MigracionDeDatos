
import pandas as pd
import psycopg2
import os

# Configuración de conexión a PostgreSQL --------------------------------------------------------------------------
db_config = {
    'host': 'localhost', # Dirección del servidor PostgreSQL
    'port': '5431',  # Puerto de PostgreSQL
    'user': 'postgres', # Usuario
    'password': 'Ns6705K5', # Contraseña del servidor PostgreSQL
    'dbname': 'TEST_DB' # Nombre de la BD
}

conn = psycopg2.connect(**db_config)
cursor = conn.cursor()

# Ruta del documento por leer -------------------------------------------------------------------------------------
dep_plazo_tabla = 'C:\\migrar\\plant_dep_plazo_tabla.xlsx'
sheet_name = 'Hoja1'  # Cambia esto al nombre de la hoja que deseas importar

df = pd.read_excel(dep_plazo_tabla, sheet_name=sheet_name)

# Reemplazar NaN por 0 en dataframe -------------------------------------------------------------------------------
val_numeric= ['val_capital', 'val_interes', 'val_tasa_interes', 'val_impuesto', 'cod_oficina_pago',
              'num_transaccion_pago', 'val_saldo_deposito', 'val_saldo_interes', 'val_saldo_impuesto'
              ]
df[val_numeric] = df[val_numeric].fillna(0)

# Reemplazar NaN por '' en dataframe ------------------------------------------------------------------------------
val_string= ['sts_dep_plazo_tabla', 'txt_referencia']
df[val_string] = df[val_string].fillna('')

# Corregir fechas -------------------------------------------------------------------------------------------------
df['fec_inicio'] = pd.to_datetime(df['fec_inicio'], errors='coerce')
df['fec_vencimiento'] = pd.to_datetime(df['fec_vencimiento'], errors='coerce')
df['fec_pago'] = pd.to_datetime(df['fec_pago'], errors='coerce')

# Obtener primer carácter seguro (devuelve '' si NaN o cadena vacía) ----------------------------------------------
def first_char(val):
    if pd.isnull(val):
        return ''
    s = str(val)
    return s[0] if s else ''

# Insertar dataframe en BD ----------------------------------------------------------------------------------------
for index, row in df.iterrows():

    # Transformar fechas.
    fec_inicio = row['fec_inicio'].strftime('%Y-%m-%d') if not pd.isnull(row['fec_inicio']) else None
    fec_vencimiento = row['fec_vencimiento'].strftime('%Y-%m-%d') if not pd.isnull(row['fec_vencimiento']) else None
    fec_pago = row['fec_pago'].strftime('%Y-%m-%d') if not pd.isnull(row['fec_pago']) else None

    sts_dep_plazo_tabla = first_char(row['sts_dep_plazo_tabla'])

    data = (row['cod_producto'], row['cod_cuenta'], row['num_cuota'], row['val_capital'], row['val_interes'], row['val_tasa_interes'],
            row['val_impuesto'], sts_dep_plazo_tabla, fec_inicio, fec_vencimiento, row['txt_referencia'], fec_pago,
            row['cod_oficina_pago'], row['cod_transaccion_pago'], row['num_transaccion_pago'], row['val_saldo_deposito'],
            row['val_saldo_interes'], row['val_saldo_impuesto']
            )
    
    columnas = ['cod_producto', 'cod_cuenta', 'num_cuota', 'val_capital', 'val_interes', 'val_tasa_interes', 'val_impuesto',
                'sts_dep_plazo_tabla', 'fec_inicio', 'fec_vencimiento', 'txt_referencia', 'fec_pago', 'cod_oficina_pago',
                'cod_transaccion_pago', 'num_transaccion_pago', 'val_saldo_deposito', 'val_saldo_interes', 'val_saldo_impuesto'
                ]
    
    # El query para insertar, usando las columnas y aplicandole el valor %s por cada columna. 
    insert_query = f"INSERT INTO sgf_dep_plazo_tabla ({', '.join(columnas)}) VALUES ({', '.join(['%s']*len(columnas))})"

    cursor.execute(insert_query, data)
    conn.commit()

cursor.close()
conn.close()

# Confirmación en Consola ----------------------------------------------------------------------------------------
print("✅ Datos insertados exitosamente.")