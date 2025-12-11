import pandas as pd

# Establecer que no se omita ningúna linea por rendimiento.
pd.set_option('display.max_rows', None)

# Establecer ruta y hoja para socios.
ruta_socios = "C:\\migrar\\socios.xlsx"
hoja_socios = 'Hoja1'
# Establecer ruta y hoja para cuentas.
ruta_cuentas = "C:\\migrar\\cuentas.xlsx"
hoja_cuentas = 'Hoja1'
# Establecer ruta y hoja para credito.
ruta_credito = "C:\\migrar\\credito.xlsx"
hoja_credito = 'Hoja1'

# Leer excel socios.
df_socios = pd.read_excel(ruta_socios, sheet_name=hoja_socios)
SOCIOS_cod_socios = df_socios.iloc[:,0] #Lee la primera columna.
# Leer excel cuentas
df_cuentas = pd.read_excel(ruta_cuentas, sheet_name=hoja_cuentas)
CUENTAS_cod_cuenta = df_cuentas.iloc[:,1] #Lee la segunda columna.
CUENTAS_cod_socio = df_cuentas.iloc[:,2] #Lee la tercera columna.
# Leer excel credito
df_credito = pd.read_excel(ruta_credito, sheet_name=hoja_credito)
CREDITO_cod_cuenta = df_credito.iloc[:,1] #Lee la segunda columna.
CREDITO_cod_cuenta_socio = df_credito.iloc[:,3] #Lee la cuarta columna.
CREDITO_cod_socio = df_credito.iloc[:,4] #Lee la quinta columna.

# Función para verificar duplicados(vd) en cod_cuenta de 'creditos'.
def vdCodCredito(df_credito, CREDITO_cod_cuenta):
    if CREDITO_cod_cuenta.duplicated().any():
        print("Hay valores duplicados:")
        print(df_credito[CREDITO_cod_cuenta.duplicated(keep=False)]) # Muestra los registros duplicados en consola.
    else:
        print("No hay valores duplicados.")

# Función para comparar cod_cuentas_socio de 'credito' con cod_cuentas de 'cuentas'.
def compararCreditoCuentasA(CUENTAS_cod_cuenta, CREDITO_cod_cuenta_socio):
    if not CREDITO_cod_cuenta_socio[~CREDITO_cod_cuenta_socio.isin(CUENTAS_cod_cuenta)].empty:
        print("Códigos de cuentas en 'credito' que no están en 'cuentas':")
        print(CREDITO_cod_cuenta_socio[~CREDITO_cod_cuenta_socio.isin(CUENTAS_cod_cuenta)])
    else:
        print("Todos las cuentas en 'credito' están registrados en 'cuentas'.")

# Función para comparar cod_socio de 'credito' con cod_socio de 'cuentas'.
def compararCreditoCuentasB(CUENTAS_cod_socio, CREDITO_cod_socio):
    if not CREDITO_cod_socio[~CREDITO_cod_socio.isin(CUENTAS_cod_socio)].empty:
        print("Códigos de socios en 'credito' que no están en 'cuentas':")
        print(CREDITO_cod_socio[~CREDITO_cod_socio.isin(CUENTAS_cod_socio)])
    else:
        print("Todos los socios en 'credito' están registrados en 'cuentas'.")

# Función para comparar cod_socio de 'credito' con cod_socio de 'socios'.
def compararCreditoSocios(SOCIOS_cod_socios, CREDITO_cod_socio):
    if not CREDITO_cod_socio[~CREDITO_cod_socio.isin(SOCIOS_cod_socios)].empty:
        print("Códigos de socios en 'credito' que no están en 'socios':")
        print(CREDITO_cod_socio[~CREDITO_cod_socio.isin(SOCIOS_cod_socios)])
    else:
        print("Todos los socios en 'credito' están registrados en 'socios'.")

vdCodCredito(df_credito, CREDITO_cod_cuenta)
compararCreditoCuentasA(CUENTAS_cod_cuenta, CREDITO_cod_cuenta_socio)
compararCreditoCuentasB(CUENTAS_cod_socio, CREDITO_cod_socio)
compararCreditoSocios(SOCIOS_cod_socios, CREDITO_cod_socio)