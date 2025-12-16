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
credito_tabla = 'C:\\migrar\\credito_tabla.xlsx'
sheet_name = 'Hoja1'  # Cambia esto al nombre de la hoja que deseas importar

df = pd.read_excel(credito_tabla, sheet_name=sheet_name)

# Reemplazar NaN por 0 en dataframe -------------------------------------------------------------------------------
val_numeric= ['cod_producto', 'cod_cuenta', 'num_cuota', 'val_capital', 'val_interes', 'val_tasa_interes',
              'val_gastos', 'val_gestion_cobro', 'val_ahorro', 'val_certificado', 'val_otros', 'val_impuesto',
              'val_seguro', 'val_notificacion', 'val_multa', 'val_saldo_capital', 'val_saldo_interes',
              'val_saldo_gestion_cobro', 'val_saldo_ahorro', 'val_saldo_certificado', 'val_saldo_otros',
              'val_saldo_impuesto', 'val_saldo_seguro', 'val_saldo_notificacion', 'val_saldo_multa',
              'val_capital_mora', 'num_dias_mora', 'val_saldo_mora', 'val_edificio', 'val_saldo_edificio',
              'val_fondo', 'val_saldo_fondo', 'cod_usrmod', 'val_capital_vencido'
              ]
df[val_numeric] = df[val_numeric].fillna(0)

# Reemplazar NaN por '' en dataframe ------------------------------------------------------------------------------
val_string= ['sts_credito_tabla', 'txt_referencia', 'cod_cuenta_contable']
df[val_string] = df[val_string].fillna('')

# Corregir fechas -------------------------------------------------------------------------------------------------
df['fec_inicio'] = pd.to_datetime(df['fec_inicio'], errors='coerce')
df['fec_vencimiento'] = pd.to_datetime(df['fec_vencimiento'], errors='coerce')
df['fec_usrmod'] = pd.to_datetime(df['fec_usrmod'], errors='coerce')
df['fec_ult_pago'] = pd.to_datetime(df['fec_ult_pago'], errors='coerce')

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
    fec_usrmod = row['fec_usrmod'].strftime('%Y-%m-%d') if not pd.isnull(row['fec_usrmod']) else None
    fec_ult_pago = row['fec_ult_pago'].strftime('%Y-%m-%d') if not pd.isnull(row['fec_ult_pago']) else None

    sts_credito_tabla = first_char(row['sts_credito_tabla'])
    txt_referencia = row['txt_referencia'] if not pd.isnull(row['txt_referencia']) else ''
    cod_cuenta_contable = row['cod_cuenta_contable'] if not pd.isnull(row['cod_cuenta_contable']) else ''

    data = (row['cod_producto'], row['cod_cuenta'], row['num_cuota'], row['val_capital'], row['val_interes'],
            row['val_tasa_interes'], row['val_gastos'], row['val_gestion_cobro'], row['val_ahorro'], row['val_certificado'],
            row['val_otros'], row['val_impuesto'], row['val_seguro'], row['val_notificacion'], row['val_multa'],
            row['val_saldo_capital'], row['val_saldo_interes'], row['val_saldo_gestion_cobro'], row['val_saldo_ahorro'], row['val_saldo_certificado'],
            row['val_saldo_otros'], row['val_saldo_impuesto'], row['val_saldo_seguro'], row['val_saldo_notificacion'], row['val_saldo_multa'],
            row['val_capital_mora'], row['num_dias_mora'], row['val_saldo_mora'], row['val_edificio'], row['val_saldo_edificio'],
            row['val_fondo'], row['val_saldo_fondo'], row['cod_usrmod'], row['val_capital_vencido'], sts_credito_tabla,
            fec_inicio, fec_vencimiento, fec_usrmod, fec_ult_pago, txt_referencia,
            cod_cuenta_contable
            )
    
    columnas = ['cod_producto', 'cod_cuenta', 'num_cuota', 'val_capital', 'val_interes',
                'val_tasa_interes', 'val_gastos', 'val_gestion_cobro', 'val_ahorro', 'val_certificado',
                'val_otros', 'val_impuesto', 'val_seguro', 'val_notificacion', 'val_multa',
                'val_saldo_capital', 'val_saldo_interes', 'val_saldo_gestion_cobro', 'val_saldo_ahorro', 'val_saldo_certificado',
                'val_saldo_otros', 'val_saldo_impuesto', 'val_saldo_seguro', 'val_saldo_notificacion', 'val_saldo_multa',
                'val_capital_mora', 'num_dias_mora', 'val_saldo_mora', 'val_edificio', 'val_saldo_edificio',
                'val_fondo', 'val_saldo_fondo', 'cod_usrmod', 'val_capital_vencido', 'sts_credito_tabla',
                'fec_inicio', 'fec_vencimiento', 'fec_usrmod', 'fec_ult_pago', 'txt_referencia',
                'cod_cuenta_contable'
                ]
    
    # El query para insertar, usando las columnas y aplicandole el valor %s por cada columna. 
    insert_query = f"INSERT INTO sgf_credito_tabla ({', '.join(columnas)}) VALUES ({', '.join(['%s']*len(columnas))})"

    cursor.execute(insert_query, data)
    conn.commit()

cursor.close()
conn.close()

# Confirmación en Consola ----------------------------------------------------------------------------------------
print("✅ Datos insertados exitosamente.")