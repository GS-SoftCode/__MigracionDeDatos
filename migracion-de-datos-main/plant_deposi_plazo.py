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
dep_plazo_tabla = 'C:\\migrar\\plant_deposi_plazo.xlsx'
sheet_name = 'Hoja1'  # Cambia esto al nombre de la hoja que deseas importar

df = pd.read_excel(dep_plazo_tabla, sheet_name=sheet_name)

# Reemplazar NaN por 0 en dataframe -------------------------------------------------------------------------------
val_numeric= ['cod_socio', 'num_documento', 'val_deposito', 'val_efectivo', 'val_cheques',
              'val_tasa_interes', 'val_impuesto', 'num_plazo', 'num_cuotas_pago_interes', 'cod_usrmod',
              'val_interes', 'val_tasa_impuesto', 'cod_oficina', 'cod_producto_socio', 'cod_cuenta_socio',
              'val_saldo_impuesto', 'val_saldo_deposito', 'val_saldo_interes', 'val_tir', 'val_tea'
              ]
df[val_numeric] = df[val_numeric].fillna(0)

# Reemplazar NaN por '' en dataframe ------------------------------------------------------------------------------
val_string= ['sts_deposito', 'txt_referencia', 'nom_beneficiario', 'ape_beneficiario', 'cod_tipo_id_ben',
             'num_id_ben', 'cod_cuenta_contable', 'sts_forma_pago_interes'
             ]
df[val_string] = df[val_string].fillna('')

# Insertar dataframe en BD ----------------------------------------------------------------------------------------
for index, row in df.iterrows():

    # Transformar fechas.
    fec_deposito = row['fec_deposito'].strftime('%Y-%m-%d') if not pd.isnull(row['fec_deposito']) else None
    fec_vencimiento = row['fec_vencimiento'].strftime('%Y-%m-%d') if not pd.isnull(row['fec_vencimiento']) else None
    fec_usrmod = row['fec_usrmod'].strftime('%Y-%m-%d') if not pd.isnull(row['fec_usrmod']) else None

    sts_deposito= str(row['sts_deposito'])
    cod_tipo_id_ben= str(row['cod_tipo_id_ben'])
    sts_forma_pago_interes= str(row['sts_forma_pago_interes'])

    cod_tipo_char = cod_tipo_id_ben[0] if cod_tipo_id_ben else ''
    sts_forma_char = sts_forma_pago_interes[0] if sts_forma_pago_interes else ''

    data = (row['cod_producto'], row['cod_cuenta'], row['cod_socio'], row['num_documento'], row['val_deposito'], row['val_efectivo'],
            row['val_cheques'], row['val_tasa_interes'], row['val_impuesto'], sts_deposito[:2], fec_deposito,
            row['num_plazo'], row['num_cuotas_pago_interes'], fec_vencimiento, row['txt_referencia'], row['nom_beneficiario'],
            row['ape_beneficiario'], cod_tipo_char, row['num_id_ben'], row['cod_usrmod'],fec_usrmod,
            row['val_interes'], row['val_tasa_impuesto'], row['cod_oficina'], row['cod_cuenta_contable'], row['cod_producto_socio'],
            row['cod_cuenta_socio'], sts_forma_char, row['val_saldo_impuesto'], row['val_saldo_deposito'], row['val_saldo_interes'],
            row['val_tir'], row['val_tea']
            )
    
    columnas = ['cod_producto', 'cod_cuenta', 'cod_socio', 'num_documento', 'val_deposito', 'val_efectivo',
                'val_cheques', 'val_tasa_interes', 'val_impuesto', 'sts_deposito', 'fec_deposito',
                'num_plazo', 'num_cuotas_pago_interes', 'fec_vencimiento', 'txt_referencia', 'nom_beneficiario',
                'ape_beneficiario', 'cod_tipo_id_ben', 'num_id_ben', 'cod_usrmod', 'fec_usrmod',
                'val_interes', 'val_tasa_impuesto', 'cod_oficina', 'cod_cuenta_contable', 'cod_producto_socio',
                'cod_cuenta_socio', 'sts_forma_pago_interes', 'val_saldo_impuesto', 'val_saldo_deposito', 'val_saldo_interes',
                'val_tir', 'val_tea'
                ]
    
    # El query para insertar, usando las columnas y aplicandole el valor %s por cada columna. 
    insert_query = f"INSERT INTO sgf_dep_plazo ({', '.join(columnas)}) VALUES ({', '.join(['%s']*len(columnas))})"

    cursor.execute(insert_query, data)
    conn.commit()

cursor.close()
conn.close()

# Confirmación en Consola -----------------------------------------------------------------------------------------
print("✅ Datos insertados exitosamente.")