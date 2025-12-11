import pandas as pd
import psycopg2
import os

# Configuración de la conexión a PostgreSQL
db_config = {
    'host': '192.168.1.71',
    'user': 'postgres',
    'password': 'dba',
    'dbname': 'Wauki'
}

conn = psycopg2.connect(**db_config)
cursor = conn.cursor()

# ruta del documento
sgf_conv_cta = 'C:\\migrar\\sgf_credito_garante.xlsx'
sheet_name = 'Hoja1'

df = pd.read_excel(sgf_conv_cta, sheet_name= sheet_name)

val_numeric= ['cod_socio', 'cod_usrmod',]
df[val_numeric] = df[val_numeric].fillna(0)

for index, row in df.iterrows():

    instert_query = f"INSERT INTO sgf_conv_cta (cod_producto, cod_cuenta, num_sec_garante, cod_tipo_garante, cod_socio, txt_referencia, fec_usrmod, cod_usrmod, sts_credito_garante, cod_tipo_deudor, fec_eliminacion, cod_causa_eliminacion)"

    fec_usrmod = row['fec_usrmod'].strftime('%Y-%m-%d') if not pd.isnull(row['fec_usrmod']) else None
    fec_eliminacion = row['fec_eliminacion'].strftime('%Y-%m-%d') if not pd.isnull(row['fec_eliminacion']) else None


    cod_tipo_garante= str(row['cod_tipo_garante'])
    sts_credito_garante = str(row['sts_credito_garante'])
    cod_tipo_deudor = str(row['cod_tipo_deudor'])
    cod_causa_eliminacion = str(row['cod_causa_eliminacion'])


    data = (row['cod_producto'], row['cod_cuenta'], row['num_sec_garante'], cod_tipo_garante[0], row['cod_socio'], row['txt_referencia'], row['fec_usrmod'], row['cod_usrmod'], sts_credito_garante[0], cod_tipo_deudor[0], row['fec_eliminacion'], cod_causa_eliminacion[0])

    cursor.execute(instert_query, data)
    conn.commit

print("Datos insertados correctamente :)...")