import pandas as pd
import psycopg2
import os

# Configuración de la conexión a PostgreSQL
db_config = {
    'host': '192.168.1.180',
    'user': 'postgres',
    'port': '5431',
    'password': 'Ns6705K5',
    'dbname': 'test_db'
}

conn = psycopg2.connect(**db_config)
cursor = conn.cursor()

# ruta del documento
sgf_conv_cta = 'C:\\migrar\\sgf_conv_cta.xlsx'
sheet_name = 'Hoja1'

df = pd.read_excel(sgf_conv_cta, sheet_name= sheet_name)


val_numeric= ['cod_dep', 'cod_usrmod', 'cod_cargo', 'val_sueldo']
df[val_numeric] = df[val_numeric].fillna(0)

for index, row in df.iterrows():

    instert_query = f"INSERT INTO sgf_conv_cta (cod_cuenta, cod_socio, sts_conv_cta, cod_dep, sts_tipo_rol, txt_referencia, cod_usrmod, fec_usrmod, sts_socio,  cod_cargo, fec_ingreso, val_sueldo)"

    fec_usrmod = row['fec_usrmod'].strftime('%Y-%m-%d') if not pd.isnull(row['fec_usrmod']) else None
    fec_ingreso = row['fec_ingreso'].strftime('%Y-%m-%d') if not pd.isnull(row['fec_ingreso']) else None

    sts_conv_cta= str(row['sts_conv_cta'])
    sts_tipo_rol = str(row['sts_tipo_rol'])
    sts_socio = str(row['sts_socio'])



    data = (row['cod_cuenta'], row['cod_socio'], sts_conv_cta[0], row['cod_dep'], sts_tipo_rol[0], row['txt_referencia'], row['cod_usrmod'], fec_usrmod, sts_socio[0], row['cod_cargo'], fec_ingreso, row['val_sueldo'])

    cursor.execute(instert_query, data)
    conn.commit

print("Datos insertados correctamente :)...")