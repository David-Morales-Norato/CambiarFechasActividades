from read_files import leer_datos,pd

class leer_datos_cambiar_fechas(leer_datos):

    def __init__(self):
        super().__init__()
        self.NOMBRES_HOJAS = ["CURSOS_ACTIVIDADES","ASIGNATURAS_SEMANAS","SEMANAS_FECHAS"]

    def lectura_especifica(self,file_path,tipo_lectura):
        try:
            # Lee el archivo xlxs por su ubicación
            
            # Si desean hacer una cambio de un número n de semanas
            if(tipo_lectura == 1):
                archivo_excel = pd.read_excel(file_path)
                datos = self.lectura_n_semanas(archivo_excel)

            # Si desean hacer una cambio a una fecha específica
            elif(tipo_lectura == 2):
                archivo_excel = pd.read_excel(file_path)
                datos = self.lectura_fecha_especifica(archivo_excel)

            elif(tipo_lectura == 3):
                archivo_excel = pd.read_excel(file_path, sheet_name=None)
                datos = self.lectura_calendario_academico(archivo_excel)
            else: 
                datos = None
            return datos
        except Exception as e:
            self.log += str(e)
            return None

    def lectura_calendario_academico(self,archivo_excel):

        # Separamos las hojas del archivo
        cursos_actividades_df = archivo_excel[self.NOMBRES_HOJAS[0]]
        asignaturas_semanas_df = archivo_excel[self.NOMBRES_HOJAS[1]]
        semanas_fechas_df = archivo_excel[self.NOMBRES_HOJAS[2]]

        # Leemos los cursos y las actividades 
        [cursos,actividad] = self.lectura_cursos_actividad(cursos_actividades_df)

        # Leemos la primera vez en la semana donde se encuentra el curso
        primera_vez = self.leer_columna(cursos_actividades_df,"PRIMER_ENCUENTRO")

        # Leemos los nombres de los cursos
        nombres_cursos = self.leer_columna(cursos_actividades_df,"NOMBRES_CURSOS")

        # Se empaqueta la primera hoja
        primera_hoja = [cursos,actividad,nombres_cursos,primera_vez]

        # Leemos los datos que contiene la seguna hoja
        # Serán organizados en un diccionario
        # Cada curso le corresponden lecciones que se ven en cada semana
        # Las semanas estarán en la tercera hoja
        # Segunda hoja = {"nombre_curso": lecciones}

        segunda_hoja = {}
        for curso in set(nombres_cursos):
            # Leemos las lecciones correspondientes al número de semanas
            lecciones = self.leer_columna(asignaturas_semanas_df,curso+"_LECCIONES")

            segunda_hoja.update({curso:lecciones})

        # Leemos solo la fecha estipulada del calendario académico para cada semena
        fecha_inicio_semana = self.leer_columna(semanas_fechas_df,"FECHA_INICIO_SEMANA")

        # ignoramos el numero de esa semana por que el busca según el índice de esa lección
        # la fecha de la semana 
        # la columna número semanas solo es para que el usuario se guíe
        tercera_hoja = fecha_inicio_semana
        
        return [cursos,primera_hoja, segunda_hoja,tercera_hoja]

    def lectura_n_semanas(self,data):
        # Leemos los cursos y las actividades 
        [cursos,actividad] = self.lectura_cursos_actividad(data)

        # Leemos el número de semanas a correr la actividad
        numero_semana = self.leer_columna(data,"NUMERO_SEMANA")

        return [cursos,actividad,numero_semana]

    def lectura_fecha_especifica(self,data):

        # Leemos los cursos y las actividades 
        [cursos,actividad] = self.lectura_cursos_actividad(data)

        # Leemos la fecha de inicio de la actividad
        fecha_inicio = self.leer_columna(data,"FECHA_INICIO")


        # Leemos la fecha de cierre de la actividad
        fecha_fin = self.leer_columna(data,"FECHA_FIN")
    
        return [cursos,actividad,fecha_inicio,fecha_fin]

    def get_log(self):
        return self.log