import pandas as pd

# Establecer que no se omita ningúna linea por rendimiento.
pd.set_option('display.max_rows', None)

# Establecer ruta y hoja para plant_deposi_plazo.
ruta_plant_deposi_plazo = "C:\\migrar\\plant_deposi_plazo.xlsx"
hoja_plant_deposi_plazo = 'Hoja1'
# Establecer ruta y hoja para plant_dep_plazo_tabla.
ruta_plant_dep_plazo_tabla = "C:\\migrar\\plant_dep_plazo_tabla.xlsx"
hoja_plant_dep_plazo_tabla = 'Hoja1'

# Leer excel plant_deposi_plazo
df_plant_deposi_plazo = pd.read_excel(ruta_plant_deposi_plazo, sheet_name=hoja_plant_deposi_plazo)
PLANT_DEPOSI_PLAZO_cod_cuenta = df_plant_deposi_plazo.iloc[:,1] #Lee la segunda columna.

# Leer excel plant_dep_plazo_tabla
df_plant_dep_plazo_tabla = pd.read_excel(ruta_plant_dep_plazo_tabla, sheet_name=hoja_plant_dep_plazo_tabla)
PLANT_DEP_PLAZO_TABLA_cod_cuenta = df_plant_dep_plazo_tabla.iloc[:,1] #Lee la segunda columna.

# Función para comparar cod_cuenta de 'plant_dep_plazo_tabla' con cod_cuenta de 'plant_deposi_plazo'.
def compararPlantDeposiPlantDepTablas(PLANT_DEPOSI_PLAZO_cod_cuenta, PLANT_DEP_PLAZO_TABLA_cod_cuenta):
    if not PLANT_DEPOSI_PLAZO_cod_cuenta[~PLANT_DEPOSI_PLAZO_cod_cuenta.isin(PLANT_DEP_PLAZO_TABLA_cod_cuenta)].empty:
        print("Códigos de cuentas en 'plant_dep_plazo_tabla' que no están en 'plant_deposi_plazo':")
        print(PLANT_DEPOSI_PLAZO_cod_cuenta[~PLANT_DEPOSI_PLAZO_cod_cuenta.isin(PLANT_DEP_PLAZO_TABLA_cod_cuenta)])
    else:
        print("Todas las cuentas en 'plant_dep_plazo_tabla' están registradas en 'plant_deposi_plazo'.")

compararPlantDeposiPlantDepTablas(PLANT_DEPOSI_PLAZO_cod_cuenta, PLANT_DEP_PLAZO_TABLA_cod_cuenta)