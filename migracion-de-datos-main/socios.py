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

conn = psycopg2.connect(**db_config)
cursor = conn.cursor()

# ruta del documento
socios = 'C:\\migrar\\socios.xlsx'
sheet_name = 'Hoja1'  # Cambia esto al nombre de la hoja que deseas importar

df = pd.read_excel(socios, sheet_name=sheet_name)

# --------------------------------------------------------------------------------------
val_numeric= ['cod_parroquia', 'cod_canton', 'cod_provincia', 'cod_pais', 'cod_act_economica',
              'cod_instruccion', 'cod_usrmod', 'val_ingreso_mensual', 'val_activo', 'val_pasivo',
              'val_patrimonio', 'val_gastos_mensuales', 'val_vivienda', 'num_tiempo_trabajo',
              'num_cargas_familiares', 'cod_socio_conyuge', 'cod_socio_vinculado', 'cod_relacion',
              'cod_oficina', 'cod_parroquia_nac', 'cod_canton_nac', 'cod_provincia_nac', 'cod_pais_nac',
              'cod_pais_dom', 'cod_barrio', 'cod_etnia']
df[val_numeric] = df[val_numeric].fillna(0)
# ----------------------------------------------------------------------------------------
val_string= ['tipo de socio S Socio C Cliente', 'Tipo de persona N Natural J Juridica',
             'Tipo de identificacion C Cedula R RUC', 'Numero de identificacion o cedula', 'nombre del socio', 'apellidos del socio',
             'nom_juridico', 'Genero M Masculino, F Femenino',
             'Estado Civil C Casado S Solvero D Divorciado U Union Libre V Viudo', 'sts_socio',
             'nom_representante_legal', 'ape_representante_legal', 'num_id_rel_legal', 'nombre_conyuge',
             'ape_conyuge', 'cod_tipo_id_con', 'num_id_con', 'direccion', 'dir2_dom', 'Telefono',
             'TelefonoTrab', 'Celular', 'sts_operador_cel', 'dir_correo', 'img_foto', 'txt_link',
             'nom_beneficiario', 'ape_beneficiario', 'cod_tipo_id_ben', 'num_id_ben', 'dir_trabajo',
             'dir2_trabajo', 'cod_tipo_sangre', 'cod_origen_ingresos', 'cod_causal_vinculacion',
             'txt_observacion_relacion', 'txt_lugar_trabajo', 'sts_rep_asamblea', 'sts_pep',
             'sts_fuente_ingresos', 'sts_actualiza_web', 'sts_consejo_administracion',
             'sts_consejo_vigilancia', 'sts_asamblea_gen_repres', 'sts_edu_financiera',
             'sts_representante_legal'
             ]
df[val_string] = df[val_string].fillna('')
# ----------------------------------------------------------------------------------------

df['Fecha de nacimiento'] = pd.to_datetime(df['Fecha de nacimiento'], errors='coerce')

for index, row in df.iterrows():
    if row['codigo del socio'] == None:
            print("Error en campo numero" + row['codigo del socio'])
    insert_query = f"INSERT INTO sgf_socio (cod_socio, cod_tipo_socio, fec_ingreso, cod_tipo_persona, cod_tipo_id, num_id, cod_parroquia, cod_canton, cod_provincia, cod_pais, nom_socio, ape_socio, cod_act_economica, cod_instruccion, nom_juridico, sts_sexo, fec_nacimiento, sts_civil, sts_socio, nom_representante_legal, ape_representante_legal, cod_tipo_id_rep_legal, num_id_rel_legal, nom_conyuge, ape_conyuge, fec_nac_con, cod_tipo_id_con, num_id_con, dir_dom, dir2_dom, tel_dom, tel_trabajo, tel_celular, sts_operador_cel, dir_correo, img_foto, txt_link, fec_usrmod, cod_usrmod, nom_beneficiario, ape_beneficiario, cod_tipo_id_ben, num_id_ben, dir_trabajo, dir2_trabajo, cod_tipo_sangre, val_ingreso_mensual, fec_solicitud, cod_origen_ingresos, val_activo, val_pasivo, val_patrimonio, val_gastos_mensuales, cod_causal_vinculacion, fec_causal, cod_tipo_vivienda, val_vivienda, num_tiempo_trabajo, num_cargas_familiares, cod_socio_conyuge, cod_socio_vinculado, cod_relacion, txt_observacion_relacion, cod_oficina, txt_lugar_trabajo, cod_nivel_estudios, sts_rep_asamblea, cod_parroquia_nac, cod_canton_nac, cod_provincia_nac, cod_pais_nac, cod_pais_dom, cod_barrio, sts_pep, sts_fuente_ingresos, sts_actualiza_web, fec_reingreso, sts_consejo_administracion, sts_consejo_vigilancia, sts_asamblea_gen_repres, sts_edu_financiera, cod_etnia, sts_representante_legal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    # transformar fechas
    fec_ingreso = row['fec_ingreso'].strftime('%Y-%m-%d') if not pd.isnull(row['fec_ingreso']) else None
    fec_nacimiento = row['Fecha de nacimiento'].strftime('%Y-%m-%d') if not pd.isnull(row['Fecha de nacimiento']) else None
    fec_nac_con = row['fec_nac_con'].strftime('%Y-%m-%d') if not pd.isnull(row['fec_nac_con']) else None
    fec_usrmod = row['fec_usrmod'].strftime('%Y-%m-%d') if not pd.isnull(row['fec_usrmod']) else None
    fec_solicitud = row['fec_solicitud'].strftime('%Y-%m-%d') if not pd.isnull(row['fec_solicitud']) else None
    fec_causal = row['fec_causal'].strftime('%Y-%m-%d') if not pd.isnull(row['fec_causal']) else None
    fec_reingreso = row['fec_reingreso'].strftime('%Y-%m-%d') if not pd.isnull(row['fec_reingreso']) else None

    image= row['img_foto'] if not pd.isnull(row['img_foto']) else None

    tipo_socio = str(row['tipo de socio S Socio C Cliente'])
    tipo_persona = str(row['Tipo de persona N Natural J Juridica'])
    tipo_identificacion = str(row['Tipo de identificacion C Cedula R RUC'])
    sexo = str(row['Genero M Masculino, F Femenino'])
    estado_civil = str(row['Estado Civil C Casado S Solvero D Divorciado U Union Libre V Viudo'])
    sts_socio = str(row['sts_socio'])
    id_rep_legal = str(row['cod_tipo_id_rep_legal'])
    cod_tipo_id = str(row['cod_tipo_id_con'])
    sts_operador_cell = str(row['sts_operador_cel'])
    cod_tipo_id_ben = str(row['cod_tipo_id_ben'])
    cod_origen_ingresos = str(row['cod_origen_ingresos'])
    cod_tipo_vivienda = str(row['cod_tipo_vivienda'])
    cod_nivel_estudios = str(row['cod_nivel_estudios'])
    sts_rep_asamblea = str(row['sts_rep_asamblea'])
    sts_pep = str(row['sts_pep'])
    sts_fuente_ingresos = str(row['sts_fuente_ingresos'])
    sts_actualiza_web = str(row['sts_actualiza_web'])
    sts_consejo_administracion = str(row['sts_consejo_administracion'])
    sts_consejo_vigilancia = str(row['sts_consejo_vigilancia'])
    sts_asamblea_gen_repres = str(row['sts_asamblea_gen_repres'])
    sts_edu_financiera = str(row['sts_edu_financiera'])
    sts_representante_legal = str(row['sts_representante_legal'])

    data = (row['codigo del socio'], tipo_socio[0], fec_ingreso, tipo_persona[0], tipo_identificacion[0], row['Numero de identificacion o cedula'], row['cod_parroquia'], row['cod_canton'], row['cod_provincia'], row['cod_pais'], row['nombre del socio'], row['apellidos del socio'], row['cod_act_economica'], row['cod_instruccion'], row['nom_juridico'], sexo[0], fec_nacimiento, estado_civil[0], sts_socio[0], row['nom_representante_legal'], row['ape_representante_legal'], id_rep_legal[0], row['num_id_rel_legal'], row['nombre_conyuge'], row['ape_conyuge'], fec_nac_con, cod_tipo_id[0], row['num_id_con'], row['direccion'], row['dir2_dom'], row['Telefono'], row['TelefonoTrab'], row['Celular'], sts_operador_cell[0], row['dir_correo'], image, row['txt_link'], fec_usrmod, row['cod_usrmod'], row['nom_beneficiario'], row['ape_beneficiario'], cod_tipo_id_ben[0], row['num_id_ben'], row['dir_trabajo'], row['dir2_trabajo'], row['cod_tipo_sangre'], row['val_ingreso_mensual'], fec_solicitud, cod_origen_ingresos[0], row['val_activo'], row['val_pasivo'], row['val_patrimonio'], row['val_gastos_mensuales'], row['cod_causal_vinculacion'], fec_causal, cod_tipo_vivienda[0], row['val_vivienda'], row['num_tiempo_trabajo'], row['num_cargas_familiares'], row['cod_socio_conyuge'], row['cod_socio_vinculado'], row['cod_relacion'], row['txt_observacion_relacion'], row['cod_oficina'], row['txt_lugar_trabajo'], cod_nivel_estudios[0], sts_rep_asamblea[0], row['cod_parroquia_nac'], row['cod_canton_nac'], row['cod_provincia_nac'], row['cod_pais_nac'], row['cod_pais_dom'], row['cod_barrio'], sts_pep[0], sts_fuente_ingresos[0], sts_actualiza_web[0], fec_reingreso, sts_consejo_administracion[0], sts_consejo_vigilancia[0], sts_asamblea_gen_repres[0], sts_edu_financiera[0], row['cod_etnia'], sts_representante_legal[0])
    
    cursor.execute(insert_query, data)
    #print(data)
    
    #print(insert_query)
    conn.commit()

cursor.close()
conn.close()

print("Datos insertados correctamente :)...")    
