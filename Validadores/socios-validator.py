import pandas as pd

# Establecer que no se omita ningúna linea por rendimiento.
pd.set_option('display.max_rows', None)

# Establecer ruta al archivo y hoja.
ruta = "C:\\migrar\\socios.xlsx"
hoja = 'Hoja1'

# Leer excel
df = pd.read_excel(ruta, sheet_name=hoja)
columna = df.iloc[:,0] #Lee la primera columna.

# Función para verificar duplicados(vd) en cod_socios.
def vdCodSocios(df, columna):
    if columna.duplicated().any():
        print("Hay valores duplicados:")
        print(df[columna.duplicated(keep=False)]) # Muestra los registros duplicados en consola.
    else:
        print("No hay valores duplicados.")

vdCodSocios(df, columna)