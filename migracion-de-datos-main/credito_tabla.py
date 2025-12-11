import pandas as pd
import psycopg2
import os

# Configuración de la conexión a PostgreSQL
db_config = {
    'host': 'localhost',
    'port': '5431',  # Puerto de PostgreSQL
    'user': 'postgres',
    'password': 'Ns6705K5',
    'dbname': 'TEST_DB'
}

# Conexión
conn = psycopg2.connect(**db_config)
cursor = conn.cursor()

# Ruta del archivo Excel
socios = r'C:\migrar\credito_tabla.xlsx'
sheet_name = 'Hoja1'  # Nombre de la hoja

# Leer Excel
df = pd.read_excel(socios, sheet_name=sheet_name)

# Columnas numéricas: reemplazar NaN por 0
val_numeric = [
    'val_capital', 'val_interes', 'val_tasa_interes', 'val_gastos', 'val_gestion_cobro', 'val_ahorro',
    'val_certificado', 'val_otros', 'val_impuesto', 'val_seguro', 'val_notificacion', 'val_multa',
    'val_saldo_capital', 'val_saldo_interes', 'val_saldo_gestion_cobro', 'val_saldo_ahorro',
    'val_saldo_certificado', 'val_saldo_gastos', 'val_saldo_otros', 'val_saldo_impuesto', 'val_saldo_seguro',
    'val_saldo_notificacion', 'val_saldo_multa', 'val_capital_mora', 'num_dias_mora', 'val_saldo_mora',
    'val_edificio', 'val_saldo_edificio', 'val_fondo', 'val_saldo_fondo', 'cod_usrmod', 'val_capital_vencido'
]
df[val_numeric] = df[val_numeric].fillna(0)
# ----------------------------------------------------------------------------------------
val_string= [ 'sts_prestamo', 'sts_tipo_cuota', 'sts_tipo_tasa', 'txt_referencia', 'sts_encaje',
             'sts_certificado', 'sts_ahorro', 'sts_seguro', 'sts_tipo_credito', 'cod_cuenta_contable',
             'cod_tipo_operacion', 'cod_obj_fideicomiso', 'cod_linea_credito', 'cod_clase_credito',
             'sts_operacion', 'cod_situacion_operacion', 'cod_destino_financiero', 'cod_forma_cancelacion'
             ]
df[val_string] = df[val_string].fillna('')
# ----------------------------------------------------------------------------------------


# Iterar sobre filas
for index, row in df.iterrows():
    # Transformar fechas a tipo date
    fec_inicio = row['fec_inicio'].date() if not pd.isna(row['fec_inicio']) else None
    fec_vencimiento = row['fec_vencimiento'].date() if not pd.isna(row['fec_vencimiento']) else None
    fec_usrmod = row['fec_usrmod'].date() if not pd.isna(row['fec_usrmod']) else None
    fec_ult_pago = row['fec_ult_pago'].date() if not pd.isna(row['fec_ult_pago']) else None

    sts_credito_tabla = str(row['sts_credito_tabla'])[0]  # solo 1 carácter

    # Query INSERT con 42 columnas
    insert_query = """
    INSERT INTO sgf_credito_tabla (
        cod_producto, cod_cuenta, num_cuota, val_capital, val_interes, val_tasa_interes,
        val_gastos, val_gestion_cobro, val_ahorro, val_certificado, val_otros, val_impuesto,
        sts_credito_tabla, fec_inicio, fec_vencimiento, txt_referencia, fec_usrmod, val_seguro,
        val_notificacion, val_multa, val_saldo_capital, val_saldo_interes, val_saldo_gestion_cobro,
        val_saldo_ahorro, val_saldo_certificado, val_saldo_gastos, val_saldo_otros, val_saldo_impuesto,
        val_saldo_seguro, val_saldo_notificacion, fec_ult_pago, val_saldo_multa, val_capital_mora,
        num_dias_mora, val_saldo_mora, val_edificio, val_saldo_edificio, val_fondo, val_saldo_fondo,
        cod_usrmod, val_capital_vencido, cod_cuenta_contable
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Valores para el INSERT
    data = (
        row['cod_producto'], row['cod_cuenta'], row['num_cuota'], row['val_capital'], row['val_interes'],
        row['val_tasa_interes'], row['val_gastos'], row['val_gestion_cobro'], row['val_ahorro'],
        row['val_certificado'], row['val_otros'], row['val_impuesto'], sts_credito_tabla,
        fec_inicio, fec_vencimiento, row['txt_referencia'], fec_usrmod, row['val_seguro'], row['val_notificacion'],
        row['val_multa'], row['val_saldo_capital'], row['val_saldo_interes'], row['val_saldo_gestion_cobro'],
        row['val_saldo_ahorro'], row['val_saldo_certificado'], row['val_saldo_gastos'], row['val_saldo_otros'],
        row['val_saldo_impuesto'], row['val_saldo_seguro'], row['val_saldo_notificacion'], fec_ult_pago,
        row['val_saldo_multa'], row['val_capital_mora'], row['num_dias_mora'], row['val_saldo_mora'],
        row['val_edificio'], row['val_saldo_edificio'], row['val_fondo'], row['val_saldo_fondo'],
        row['cod_usrmod'], row['val_capital_vencido'], row['cod_cuenta_contable']
    )

    # Ejecutar INSERT
    cursor.execute(insert_query, data)
    conn.commit()

print("Datos insertados correctamente :)")

# Cerrar conexión
cursor.close()
conn.close()
