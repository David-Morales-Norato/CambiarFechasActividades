
import datetime
from Robot import Robot
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException

class robot_cambiar_fechas(Robot):
    def __init__(self, DRIVER_PATH):
        super().__init__(DRIVER_PATH)

        logs_cambiar_fechas = [ ]
        self._LOGS = self._LOGS + logs_cambiar_fechas

    def tratamiento_curso(self,datos, eleccion,indice_curso):

        # Se separan los datos

        # Mover número 'n' de semanas 1
        # Mover a una fecha específica 2
        ACTIVIDAD = datos[1][0] # Adquirimos el CPL a calificar
        if(eleccion == 1):
            numero_semana = datos[2][indice_curso]# Adquirimos las semanas que se van a correr cada actividad

        elif(eleccion == 2): # Adquirimos las fechas específicas en que se van a mover las actividades
            fechas_inicio = datos[2][indice_curso]
            fechas_fin = datos[3][indice_curso]

        try:
            # Se busca la actividad a cambiar la fecha
            actividad = self.driver.find_element_by_partial_link_text(ACTIVIDAD)
            actividad.location_once_scrolled_into_view
            actividad.click() 

        except Exception as e:
            # En caso de no ser encontrado se captura la excepción y  se registra en el log
            self.log +=self._LOGS[2]+ str(e)

        self.driver.find_element_by_link_text("Editar ajustes").click()

        if(eleccion == 1): # En caso de mover un número n de semanas
            print(numero_semana)
            pass
        elif(eleccion == 2): # En caso de mover a una fecha en específico
            print(fechas_inicio)
            print(fechas_fin)
            pass            

        #Si no ha saltado alguna excepción, se guarda que fue un curso exitoso
        self.log+=self._LOGS[4]