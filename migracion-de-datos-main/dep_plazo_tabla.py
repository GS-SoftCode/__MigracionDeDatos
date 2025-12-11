import pandas as pd
import psycopg2
import os

# Configuración de la conexión a PostgreSQL
db_config = {
    'host': 'localhost',
    'port': '5432',  # Puerto de PostgreSQL
    'user': 'postgres',
    'password': 'dba',
    'dbname': 'C_Megia'
}

conn = psycopg2.connect(**db_config)
cursor = conn.cursor()


# ruta del documento
dep_plazo_tabla = 'C:\\migrar\\plant_dep_plazo_tabla.xlsx'
sheet_name = 'Hoja1'  # Cambia esto al nombre de la hoja que deseas importar

df = pd.read_excel(dep_plazo_tabla, sheet_name=sheet_name)

val_numeric= ['val_capital', 'val_interes', 'val_tasa_interes', 'val_impuesto', 'cod_oficina_pago', 'num_transaccion_pago', 'val_saldo_deposito', 'val_saldo_interes', 'val_saldo_impuesto']
df[val_numeric] = df[val_numeric].fillna(0)

# ----------------------------------------------------------------------------------------
val_string= [ 'sts_prestamo', 'sts_tipo_cuota', 'sts_tipo_tasa', 'txt_referencia', 'sts_encaje',
             'sts_certificado', 'sts_ahorro', 'sts_seguro', 'sts_tipo_credito', 'cod_cuenta_contable',
             'cod_tipo_operacion', 'cod_obj_fideicomiso', 'cod_linea_credito', 'cod_clase_credito',
             'sts_operacion', 'cod_situacion_operacion', 'cod_destino_financiero', 'cod_forma_cancelacion'
             ]
df[val_string] = df[val_string].fillna('')
# ----------------------------------------------------------------------------------------


for index, row in df.iterrows():
    insert_query = f"INSERT INTO sgf_dep_plazo_tabla (cod_producto, cod_cuenta, num_cuota, val_capital, val_interes, val_tasa_interes, val_impuesto, sts_dep_plazo_tabla, fec_inicio, fec_vencimiento, txt_referencia, fec_pago, cod_oficina_pago, cod_transaccion_pago, num_transaccion_pago, val_saldo_deposito, val_saldo_interes, val_saldo_impuesto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    # transformar fechas
    fec_inicio = row['fec_inicio'].strftime('%Y-%m-%d') if not pd.isnull(row['fec_inicio']) else None
    fec_vencimiento = row['fec_vencimiento'].strftime('%Y-%m-%d') if not pd.isnull(row['fec_vencimiento']) else None
    fec_pago = row['fec_pago'].strftime('%Y-%m-%d') if not pd.isnull(row['fec_pago']) else None

    sts_dep_plazo_tabla = str(row['sts_dep_plazo_tabla'])


    data = (row['cod_producto'], row['cod_cuenta'], row['num_cuota'], row['val_capital'], row['val_interes'], row['val_tasa_interes'], row['val_impuesto'], sts_dep_plazo_tabla[0], fec_inicio, fec_vencimiento, row['txt_referencia'], fec_pago, row['cod_oficina_pago'], row['cod_transaccion_pago'], row['num_transaccion_pago'], row['val_saldo_deposito'], row['val_saldo_interes'], row['val_saldo_impuesto'])

    cursor.execute(insert_query, data)
    conn.commit()

cursor.close()
conn.close()

print("Datos insertados correctamente :)...")