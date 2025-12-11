import pandas as pd

# Establecer que no se omita ningúna linea por rendimiento.
pd.set_option('display.max_rows', None)

# Establecer ruta y hoja para credito.
ruta_credito = "C:\\migrar\\credito.xlsx"
hoja_credito = 'Hoja1'
# Establecer ruta y hoja para credito-tabla.
ruta_credito_tabla = "C:\\migrar\\credito_tabla.xlsx"
hoja_credito_tabla = 'Hoja1'

# Leer excel credito
df_credito = pd.read_excel(ruta_credito, sheet_name=hoja_credito)
CREDITO_cod_cuenta = df_credito.iloc[:,1] #Lee la segunda columna.
# Leer excel credito-tabla
df_credito_tabla = pd.read_excel(ruta_credito_tabla, sheet_name=hoja_credito_tabla)
CREDITO_TABLA_cod_cuenta = df_credito_tabla.iloc[:,1] #Lee la segunda columna.

# Función para comparar cod_cuentas de 'credito-tabla' con cod_cuentas de 'credito'.
def compararCreditoCreditoTabla(CREDITO_cod_cuenta, CREDITO_TABLA_cod_cuenta):
    if not CREDITO_TABLA_cod_cuenta[~CREDITO_TABLA_cod_cuenta.isin(CREDITO_cod_cuenta)].empty:
        print("Códigos de cuentas en 'credito-tabla' que no están en 'credito':")
        print(CREDITO_TABLA_cod_cuenta[~CREDITO_TABLA_cod_cuenta.isin(CREDITO_cod_cuenta)])
    else:
        print("Todos las cuentas en 'credito-tabla' están registrados en 'credito'.")

compararCreditoCreditoTabla(CREDITO_cod_cuenta, CREDITO_TABLA_cod_cuenta)