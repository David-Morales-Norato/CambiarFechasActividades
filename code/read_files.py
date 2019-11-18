import pandas as pd


def lectura_cursos_actividad(data):
    log = ''
    try:
        # Intenta encontrar la columna
        cursos = data["CURSOS"].dropna().tolist()

        if(len(cursos)==0): # Si no encuentra bota error
            raise Exception("Fallo, no hay cursos que recorrer")    
        else:
            pass
    except Exception as e:
        log += "Fallo al leer columna: " + str(e) + "\n"
        cursos = None

    try:
        # Intenta encontrar la columna 
        ACTIVIDAD = data["ACTIVIDAD"].dropna().tolist()
        if(len(ACTIVIDAD) == 0):# Si no encuentra bota error
            raise Exception("Cuidado, no hay ACTIVIDAD que leer")
        else:
            pass
    except Exception as e:
        log += "Fallo al leer columna: " + str(e) + "\n"
        ACTIVIDAD = None

    return [cursos, ACTIVIDAD,log]

def leer_datos_cambiar_fechas(file_path,tipo_lectura):
    # Coming soon
    log = ''
    try:
        # Lee el archivo csv por su ubicación
        data = pd.read_csv(file_path)

        # Si desean hacer una cambio de un número n de semanas
        if(tipo_lectura == 1):
            datos = lectura_n_semanas(data)

        # Si desean hacer una cambio a una fecha específica
        elif(tipo_lectura == 2):
            datos = lectura_fecha_especifica(data)

        else: 
            datos = None
        return datos
    except Exception as e:
        log += str(e)
        return None
def lectura_n_semanas(data):
    datos_previos = lectura_cursos_actividad(data)
    log = datos_previos[-1]
    cursos = datos_previos[0]
    ACTIVIDAD = datos_previos[1]
    try:
        # Intenta encontrar la columna 
 
        numero_semana = data["NUMERO_SEMANA"].dropna().tolist()

        if(len(numero_semana) == 1):# Si no encuentra bota error 
            raise Exception("numero_semana")
        else:
            pass
    except Exception as e:
        log += "Fallo al leer columna: " + str(e) + "\n"
        numero_semana = None

    return [cursos,ACTIVIDAD,numero_semana,log]

def lectura_fecha_especifica(data):
    datos_previos = lectura_cursos_actividad(data)
    log = datos_previos[-1]
    cursos = datos_previos[0]
    ACTIVIDAD = datos_previos[1]
    try:
        # Intenta encontrar la columna 
 
        fecha_inicio = data["FECHA_INICIO"].dropna().tolist()

        if(len(fecha_inicio) == 1):# Si no encuentra bota error 
            raise Exception("fecha_inicio")
        else:
            pass
    except Exception as e:
        log += "Fallo al leer columna: " + str(e) + "\n"
        fecha_inicio = None
    
    try:# Intenta encontrar la columna
        fecha_fin = data["FECHA_FIN"].dropna().tolist()

        if(len(fecha_fin) == 0):# Si no encuentra bota error
            raise Exception("Fallo al leer fecha_fin")
        else:
            pass
    except Exception as e:
        log += "Fallo al leer columna: " + str(e) + "\n"
        fecha_fin = None


    return [cursos,ACTIVIDAD,fecha_inicio,fecha_fin,log]

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
    datos_previos = lectura_cursos_actividad(data)
    log = datos_previos[-1]
    cursos = datos_previos[0]
    ACTIVIDAD = datos_previos[1]

    try:
        # Intenta encontrar la columna 
 
        id_pregunta = data["ID_PREGUNTA"].dropna().tolist()

        if(len(id_pregunta) != 1):# Si no encuentra bota error o encuentra más de una
            raise Exception("Id pregunta filas")
        else:
            pass
    except Exception as e:
        log += "Fallo al leer columna: " + str(e) + "\n"
        id_pregunta = None
    
    try:# Intenta encontrar la columna
        enunciados = data["ENUNCIADOS"].dropna().tolist()

        if(len(enunciados) == 0):# Si no encuentra bota error
            raise Exception("Fallo al leer los Enunciados")
        else:
            pass
    except Exception as e:
        log += "Fallo al leer columna: " + str(e) + "\n"
        enunciados = None

    try:
        # Intenta encontrar la columna
        respuestas = data["Respuestas"].dropna().tolist()

        if(len(respuestas) == 0):# Si no encuentra bota error
            raise Exception("Fallo al leer los respuestas")
        else:
            pass

    except Exception as e:
        log += "Fallo al leer columna: " + str(e) + "\n"
        respuestas = None

    return [cursos, ACTIVIDAD, id_pregunta,enunciados,respuestas,log]
