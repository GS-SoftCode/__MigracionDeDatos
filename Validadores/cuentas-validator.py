import pandas as pd

# Establecer que no se omita ningúna linea por rendimiento.
pd.set_option('display.max_rows', None)

# Establecer ruta y hoja para socios.
ruta_socios = "C:\\migrar\\socios.xlsx"
hoja_socios = 'Hoja1'
# Establecer ruta y hoja para cuentas.
ruta_cuentas = "C:\\migrar\\cuentas.xlsx"
hoja_cuentas = 'Hoja1'

# Leer excel socios.
df_socios = pd.read_excel(ruta_socios, sheet_name=hoja_socios)
SOCIOS_cod_socios = df_socios.iloc[:,0] #Lee la primera columna.
# Leer excel cuentas.
df_cuentas = pd.read_excel(ruta_cuentas, sheet_name=hoja_cuentas)
CUENTAS_cod_producto = df_cuentas.iloc[:,0] #Lee la primera columna.
CUENTAS_cod_cuentas = df_cuentas.iloc[:,1] #Lee la segunda columna.
CUENTAS_cod_socios = df_cuentas.iloc[:,2] #Lee la tercera columna.

# Función para comparar cod_socios de socios con cod_socios de cuentas.
def compararSociosCuentas(SOCIOS_cod_socios, CUENTAS_cod_socios):
    if not CUENTAS_cod_socios[~CUENTAS_cod_socios.isin(SOCIOS_cod_socios)].empty:
        print("Códigos de socio en 'cuentas' que no están en 'socios':")
        print(CUENTAS_cod_socios[~CUENTAS_cod_socios.isin(SOCIOS_cod_socios)])
    else:
        print("Todos los socios en 'cuentas' están registrados en 'socios'.")

# Función para verificar duplicados(vd) en los registros concatenados de cod_productos y cod_cuentas.
def vdProductosCuentas():
    df_cuentas['conct_columna'] = df_cuentas.iloc[:, 0].astype(str) + ' - ' + df_cuentas.iloc[:, 1].astype(str)
    duplicados = df_cuentas['conct_columna'].duplicated(keep=False)
    if duplicados.any():
        print("Duplicados encontrados:")
        print(df_cuentas['conct_columna'][duplicados])
    else:
        print("No hay duplicados.")
    df_cuentas.drop('conct_columna', axis=1, inplace=True)

# Llamados de funciones.
compararSociosCuentas(SOCIOS_cod_socios, CUENTAS_cod_socios)
vdProductosCuentas()