from read_files import leer_datos,pd

class leer_datos_recalificar(leer_datos):
    def __init__(self):
        super().__init__()

    def lectura_especifica(self,file_path, tipo_lectura):
        try:
            # Lee el archivo csv por su ubicación
            data = pd.read_csv(file_path)

            # Si desean hacer una recalificación completa
            if(tipo_lectura == 1):
                datos = self.lectura_cursos_actividad(data)

            # Si desean hacer una recalificación para una pregunta de emparejamiento
            elif(tipo_lectura == 2):
                datos = self.lectura_tipo_recalificar_emparejamiento(data)

            else: 
                datos = None
            return datos
        except Exception as e:
            self.log += str(e)
            return None

    def lectura_tipo_recalificar_emparejamiento(self,data):
        # Leemos los cursos y las actividades 
        [cursos,actividad] = self.lectura_cursos_actividad(data)

        # Leemos el id de la pregunta a recalificar
        id_pregunta = self.leer_columna(data,"ID_PREGUNTA")
        

        # Leemos los enunciados de la pregunta
        enunciados = self.leer_columna(data,"ENUNCIADOS")

        # Leemos las respuestas de la pregunta
        respuestas = self.leer_columna(data,"Respuestas")

        return [cursos, actividad, id_pregunta,enunciados,respuestas]

    def get_log(self):
        return self.log