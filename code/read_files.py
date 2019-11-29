import pandas as pd
NOMBRES_HOJAS = ["CURSOS_ACTIVIDADES","ASIGNATURAS_SEMANAS","SEMANAS_FECHAS"]

def lectura_cursos_actividad(data):

    log = ''

    # Leemos los id del curso
    datos_cursos = leer_columna(data,"CURSOS_ID")
    cursos = datos_cursos[0]
    log += datos_cursos[1]

    # Leemos las actividades para cada curso
    datos_actividad = leer_columna(data,"ACTIVIDAD")
    actividad = datos_actividad[0]
    log += datos_actividad[1]

    # Se retornan los datos con el log
    return [cursos, actividad,log]

def leer_datos_cambiar_fechas(file_path,tipo_lectura):
    # Coming soon
    log = ''
    try:
        # Lee el archivo xlxs por su ubicación
        
        # Si desean hacer una cambio de un número n de semanas
        if(tipo_lectura == 1):
            archivo_excel = pd.read_excel(file_path)
            datos = lectura_n_semanas(archivo_excel)

        # Si desean hacer una cambio a una fecha específica
        elif(tipo_lectura == 2):
            archivo_excel = pd.read_excel(file_path)
            datos = lectura_fecha_especifica(archivo_excel)

        elif(tipo_lectura == 3):
            archivo_excel = pd.read_excel(file_path, sheet_name=None)
            datos = lectura_calendario_academico(archivo_excel)
        else: 
            datos = None
        return datos
    except Exception as e:
        log += str(e)
        return None

def lectura_calendario_academico(archivo_excel):
    log = ''

    # Separamos las hojas del archivo
    cursos_actividades_df = archivo_excel[NOMBRES_HOJAS[0]]
    asignaturas_semanas_df = archivo_excel[NOMBRES_HOJAS[1]]
    semanas_fechas_df = archivo_excel[NOMBRES_HOJAS[2]]

    # Leemos los cursos y las actividades 
    datos_cursos_actividad = lectura_cursos_actividad(cursos_actividades_df)
    cursos = datos_cursos_actividad[0]
    actividad = datos_cursos_actividad[1]
    log += datos_cursos_actividad[-1]

    # Leemos los nombres de los cursos
    datos_nombres_cursos = leer_columna(cursos_actividades_df,"NOMBRES_CURSOS")
    nombres_cursos = datos_nombres_cursos[0]
    log += datos_nombres_cursos[1]

    # Se empaqueta la primera hoja
    primera_hoja = [nombres_cursos,cursos,actividad]


    # Leemos los datos que contiene la seguna hoja
    # Serán organizados en un diccionario
    # Cada curso le corresponden un número de semanas y las lecciones que se ven en cada semana
    # segunda_hoja = {"nombre_curso": [numero_semanas, lecciones]}
    segunda_hoja = {}
    for curso in set(nombres_cursos):
        # Leemos el número de semanas
        datos_no_semanas = leer_columna(asignaturas_semanas_df,curso+"_NÚMERO_SEMANA")
        no_semanas = datos_no_semanas[0]
        log += datos_no_semanas[1]

        # Leemos las lecciones correspondientes al número de semanas
        datos_lecciones = leer_columna(asignaturas_semanas_df,curso+"_LECCIONES")
        lecciones = datos_lecciones[0]
        log += datos_lecciones[1]

        segunda_hoja.update({curso:[no_semanas,lecciones]})


    # Leemos los datos que contiene la tercera hoja
    no_semana = leer_columna(semanas_fechas_df,"NÚMERO_SEMANA")
    fecha_inicio_semana = leer_columna(semanas_fechas_df,"FECHA_INICIO_SEMANA")

    tercera_hoja = [no_semana,fecha_inicio_semana]
    
    return [primera_hoja, segunda_hoja,tercera_hoja, log]

def lectura_n_semanas(data):
    log = ''
    # Leemos los cursos y las actividades 
    datos_cursos_actividad = lectura_cursos_actividad(data)
    cursos = datos_cursos_actividad[0]
    actividad = datos_cursos_actividad[1]
    log = datos_cursos_actividad[-1]

    # Leemos el número de semanas a correr la actividad
    datos_numero_semana = leer_columna(data,"NUMERO_SEMANA")
    numero_semana = datos_numero_semana[0]
    log += datos_numero_semana[1]

    return [cursos,actividad,numero_semana,log]

def lectura_fecha_especifica(data):
    log = ''
    # Leemos los cursos y las actividades 
    datos_cursos_actividad = lectura_cursos_actividad(data)
    cursos = datos_cursos_actividad[0]
    actividad = datos_cursos_actividad[1]
    log += datos_cursos_actividad[-1]

    # Leemos la fecha de inicio de la actividad
    datos_fecha_inicio = leer_columna(data,"FECHA_INICIO")
    fecha_inicio = datos_fecha_inicio[0]
    log += datos_fecha_inicio[1]


    # Leemos la fecha de cierre de la actividad
    datos_fecha_fin = leer_columna(data,"FECHA_FIN")
    fecha_fin = datos_fecha_fin[0]
    log += datos_fecha_fin[1]


    return [cursos,actividad,fecha_inicio,fecha_fin,log]

def leer_datos_recalificar(file_path, tipo_lectura):
    log = ''
    try:
        # Lee el archivo csv por su ubicación
        data = pd.read_csv(file_path)

        # Si desean hacer una recalificación completa
        if(tipo_lectura == 1):
            datos = lectura_cursos_actividad(data)

        # Si desean hacer una recalificación para una pregunta de emparejamiento
        elif(tipo_lectura == 2):
            datos = lectura_tipo_recalificar_emparejamiento(data)

        else: 
            datos = None
        return datos
    except Exception as e:
        log += str(e)
        return None

def lectura_tipo_recalificar_emparejamiento(data):
    log = ''
    # Leemos los cursos y las actividades 
    datos_cursos_actividad = lectura_cursos_actividad(data)
    cursos = datos_cursos_actividad[0]
    actividad = datos_cursos_actividad[1]
    log += datos_cursos_actividad[-1]


    # Leemos el id de la pregunta a recalificar
    datos_id_pregunta = leer_columna(data,"ID_PREGUNTA")
    id_pregunta = datos_id_pregunta[0]
    log += datos_id_pregunta[1]
    

    # Leemos los enunciados de la pregunta
    datos_enunciados = leer_columna(data,"ENUNCIADOS")
    enunciados = datos_enunciados[0]
    log += datos_enunciados[1]

    # Leemos las respuestas de la pregunta
    datos_respuestas = leer_columna(data,"Respuestas")
    respuestas = datos_respuestas[0]
    log += datos_respuestas[1]


    return [cursos, actividad, id_pregunta,enunciados,respuestas,log]

def leer_columna(data_frame, nombre_columna):
    log = ''
    try:
        # Intenta encontrar la columna 
 
        columna = data_frame[nombre_columna].dropna().tolist()

        if(len(columna) == 0):# Si no encuentra bota error 
            raise Exception(nombre_columna)
        else:
            pass
    except Exception as e:
        log += "Fallo al leer columna: " + str(e) + "\n"
        columna = None

    return [columna,log]