from robot_gui import robot_gui, tk
from robot_cambiar_fechas import robot_cambiar_fechas
from read_files import leer_datos_cambiar_fechas

class cambiar_fechas_gui(robot_gui):
    def __init__(self):
        super().__init__()
        # Variable de control de la opción del tipo de tarea que se va a usar
        self.opcion = tk.IntVar()
        self.opcion.set(0) # Se setea en 0, el caso en que no ha escogido ninguna opción

        # Mover número 'n' de semanas 1
        # Mover a una fecha específica 2
        # Botones que son las opciones
        tk.Radiobutton(self.frame_left, text="Mover número 'n' de semanas",padx = 20, variable=self.opcion, value=1).grid(row=1,column=3)
        tk.Radiobutton(self.frame_left, text="Mover a una fecha específica",padx = 20, variable=self.opcion, value=2).grid(row=2,column=3)
        self.root.mainloop()

    def pre_run_especifico(self):
        # Lemos los datos del archivo CSV
        datos = leer_datos_cambiar_fechas(self.file_path, self.opcion.get())
        if(len(datos[-1])<1): # Si no hay algún error al leer los datos
            # Se pasan los datos y la opción de la tarea del robot
            self.run_robot(datos,self.opcion.get())
        else:
            # Si hay por lo menos un error lo imprime en el label de la GUI
            self.log += datos[-1]
            self.label_logs_result.config(text = datos[-1])

    def get_robot(self,driver_path):
        return robot_cambiar_fechas(driver_path)

    def run_robot_especifico(self,datos, tipo_tarea):

        # Mover número 'n' de semanas 1
        # Mover a una fecha específica 2
        tipo_recalificacion = tipo_tarea
        # Corre el robot y recorre cursos para recalificar 
        self.robot.recorrer_cursos(datos, tipo_recalificacion)