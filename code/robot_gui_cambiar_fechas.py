from robot_gui import robot_gui, tk
from robot_cambiar_fechas import robot_cambiar_fechas
from leer_cambiar_fechas import leer_datos_cambiar_fechas

DEBUG = True

class cambiar_fechas_gui(robot_gui):
    def __init__(self):
        super().__init__()
        # Variable de control de la opción del tipo de tarea que se va a usar
        self.opcion = tk.IntVar()
        self.opcion.set(0) # Se setea en 0, el caso en que no ha escogido ninguna opción

        # Mover número 'n' de semanas 1
        # Mover a una fecha específica 2
        # Mover según el calendario académico 3
        # Botones que son las opciones
        tk.Radiobutton(self.frame_left, text="Mover número 'n' de semanas",padx = 20, variable=self.opcion, value=1).grid(row=1,column=3)
        tk.Radiobutton(self.frame_left, text="Mover a una fecha específica",padx = 20, variable=self.opcion, value=2).grid(row=2,column=3)
        tk.Radiobutton(self.frame_left, text="Mover según el calendario académico",padx = 20, variable=self.opcion, value=3).grid(row=3,column=3)
        if(DEBUG):
            self.file_path = "/home/david-norato/Documentos/EXPERTIC/cambiar_fechas_actividades/datos/datos_num_semanas.xlsx"
            self.input_user_entry.insert(0,"exper-tic")
            self.input_pass_entry.insert(0,"exper-tic")
            self.archivo_cargado = True
            self.opcion.set(1)
        self.root.mainloop()

    def pre_run_especifico(self):
        # Lemos los datos del archivo CSV
        leer_datos = leer_datos_cambiar_fechas()
        datos = leer_datos.lectura_especifica(self.file_path, self.opcion.get())
        if(len(leer_datos.get_log())<1): # Si no hay algún error al leer los datos
            # Se pasan los datos y la opción de la tarea del robot
            self.run_robot(datos,self.opcion.get())
        else:
            # Si hay por lo menos un error lo imprime en el label de la GUI
            self.log += leer_datos.get_log()
            self.label_logs_result.config(text = leer_datos.get_log())

    def get_robot(self,driver_path):
        return robot_cambiar_fechas(driver_path)

    def run_robot_especifico(self,datos, tipo_tarea):

        # Mover número 'n' de semanas 1
        # Mover a una fecha específica 2
        # Mover según el calendario académico 3
        tipo_recalificacion = tipo_tarea
        # Corre el robot y recorre cursos para recalificar 
        self.robot.recorrer_cursos(datos, tipo_recalificacion)

    def revisar_log(self):

        log = self.robot.log
        salida = ''


        activiades_procesadas = log.count("[1]")
        actividades_fallidas = log.count("[-5]")
        actividades_exitosas = log.count("[5]")
        salida += "Total actividades procesadas: "+ str(activiades_procesadas) + '\n'
        salida += "Total actividades modificadas exitosamente: "+ str(actividades_exitosas) + '\n'
        salida += "Total actividades modificadas incorrectamente: "+ str(actividades_fallidas) + '\n'
        return salida