import pandas as pd

# Establecer que no se omita ningúna linea por rendimiento.
pd.set_option('display.max_rows', None)

# Establecer ruta y hoja para socios.
ruta_socios = "C:\\migrar\\socios.xlsx"
hoja_socios = 'Hoja1'
# Establecer ruta y hoja para cuentas.
ruta_cuentas = "C:\\migrar\\cuentas.xlsx"
hoja_cuentas = 'Hoja1'
# Establecer ruta y hoja para plant_deposi_plazo.
ruta_plant_deposi_plazo = "C:\\migrar\\plant_deposi_plazo.xlsx"
hoja_plant_deposi_plazo = 'Hoja1'

# Leer excel socios.
df_socios = pd.read_excel(ruta_socios, sheet_name=hoja_socios)
SOCIOS_cod_socios = df_socios.iloc[:,0] #Lee la primera columna.

# Leer excel cuentas.
df_cuentas = pd.read_excel(ruta_cuentas, sheet_name=hoja_cuentas)
CUENTAS_cod_producto = df_cuentas.iloc[:,0] #Lee la primera columna.
CUENTAS_cod_cuentas = df_cuentas.iloc[:,1] #Lee la segunda columna.
CUENTAS_cod_socios = df_cuentas.iloc[:,2] #Lee la tercera columna.
#Leer y concatenar cod_producto con cod_cuenta de 'cuentas'.
CUENTAS_concat = df_cuentas.iloc[:, 0].astype(str) + df_cuentas.iloc[:, 1].astype(str)

# Leer excel plant_deposi_plazo
df_plant_deposi_plazo = pd.read_excel(ruta_plant_deposi_plazo, sheet_name=hoja_plant_deposi_plazo)
PLANT_DEPOSI_PLAZO_cod_cuenta = df_plant_deposi_plazo.iloc[:,1] #Lee la segunda columna.
PLANT_DEPOSI_PLAZO_cod_socio = df_plant_deposi_plazo.iloc[:,2] #Lee la tercera columna.
PLANT_DEPOSI_PLAZO_cod_cuenta_socio = df_plant_deposi_plazo.iloc[:,26] #Lee la columna 27.
#Leer y concatenar cod_producto_socio con cod_cuenta_socio de 'plant_deposi_plazo'.
PLANT_DEPOSI_PLAZO_concat = df_plant_deposi_plazo.iloc[:, 25].astype(str) + df_plant_deposi_plazo.iloc[:, 26].astype(str)

# Función para verificar duplicados(vd) en cod_cuenta de 'plant_deposi_plazo'.
def vdCodPlantDeposi(df_plant_deposi_plazo, PLANT_DEPOSI_PLAZO_cod_cuenta):
    if PLANT_DEPOSI_PLAZO_cod_cuenta.duplicated().any():
        print("Hay valores duplicados:")
        print(df_plant_deposi_plazo[PLANT_DEPOSI_PLAZO_cod_cuenta.duplicated(keep=False)]) # Muestra los registros duplicados en consola.
    else:
        print("No hay valores duplicados.")

# Función para comparar cod_socio de 'plant_deposi_plazo' con cod_socio de 'cuentas'.
def compararPlantDeposiCuentas(CUENTAS_cod_socio, PLANT_DEPOSI_PLAZO_cod_socio):
    if not PLANT_DEPOSI_PLAZO_cod_socio[~PLANT_DEPOSI_PLAZO_cod_socio.isin(CUENTAS_cod_socio)].empty:
        print("Códigos de socios en 'plant_deposi_plazo' que no están en 'cuentas':")
        print(PLANT_DEPOSI_PLAZO_cod_socio[~PLANT_DEPOSI_PLAZO_cod_socio.isin(CUENTAS_cod_socio)])
    else:
        print("Todos los socios en 'plant_deposi_plazo' están registrados en 'cuentas'.")

# Función para comparar cod_socio de 'plant_deposi_plazo' con cod_socio de 'socios'.
def compararPlantDeposiSocios(SOCIOS_cod_socios, PLANT_DEPOSI_PLAZO_cod_socio):
    if not PLANT_DEPOSI_PLAZO_cod_socio[~PLANT_DEPOSI_PLAZO_cod_socio.isin(SOCIOS_cod_socios)].empty:
        print("Códigos de socios en 'plant_deposi_plazo' que no están en 'socios':")
        print(PLANT_DEPOSI_PLAZO_cod_socio[~PLANT_DEPOSI_PLAZO_cod_socio.isin(SOCIOS_cod_socios)])
    else:
        print("Todos los socios en 'plant_deposi_plazo' están registrados en 'socios'.")

# Función para comparar entre
# Concatenados de cod_producto_socio con cod_cuenta_socio de 'plant_deposi_plazo'...
                            # con
# Concatenados de cod_producto con cod_cuenta de 'cuentas'.
def compararConcat(CUENTAS_concat, PLANT_DEPOSI_PLAZO_concat, PLANT_DEPOSI_PLAZO_cod_cuenta_socio):
    if not PLANT_DEPOSI_PLAZO_concat[~PLANT_DEPOSI_PLAZO_concat.isin(CUENTAS_concat)].empty:
        print("cod_cuenta_socio de concatenaciones de plant_deposi_plazo que no están en cuentas:")
        print(PLANT_DEPOSI_PLAZO_cod_cuenta_socio[PLANT_DEPOSI_PLAZO_concat[~PLANT_DEPOSI_PLAZO_concat.isin(CUENTAS_concat)].index])
    else:
        print("Todas las concatenaciones de 'plant_deposi_plazo' están en 'cuentas'.")

vdCodPlantDeposi(df_plant_deposi_plazo, PLANT_DEPOSI_PLAZO_cod_cuenta)
compararPlantDeposiCuentas(CUENTAS_cod_socios, PLANT_DEPOSI_PLAZO_cod_socio)
compararPlantDeposiSocios(SOCIOS_cod_socios, PLANT_DEPOSI_PLAZO_cod_socio)
compararConcat(CUENTAS_concat, PLANT_DEPOSI_PLAZO_concat, PLANT_DEPOSI_PLAZO_cod_cuenta_socio)