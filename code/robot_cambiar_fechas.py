import numpy as np
import datetime
from Robot import Robot
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.webdriver.support.ui import Select

class robot_cambiar_fechas(Robot):
    def __init__(self, DRIVER_PATH):
        
        super().__init__(DRIVER_PATH)
        # String que tiene el id de los campos para seleccionar la fecha


        logs_cambiar_fechas = [
            '[-5] Error al llenar el formulario para cambiar fechas de la actividad| Exception: ',
            '[5]  Se diligenció correctamente el formulario para cambiar fechas de la actividad']
        self._LOGS = self._LOGS + logs_cambiar_fechas


    def tratamiento_curso(self,datos, variables_de_control):
        # Obtenemos los datos sin contar el  último elemento

        datos = np.array(datos[1:][:-1])
        # Eleccion es el primer elemento
        eleccion = variables_de_control[0]
        # Contador el segundo elemento
        contador = variables_de_control[1]
        # Se separan los datos
        fila = datos[:,contador]
        # Adquirimos el CPL a calificar
        ACTIVIDAD = fila[0] 
        try:
            # Se busca la actividad a cambiar la fecha
            actividad = self.driver.find_element_by_partial_link_text(ACTIVIDAD)
            actividad.location_once_scrolled_into_view
            actividad.click() 

            # Se abre camino hasta el formulario para cambiar fechas
            self.driver.find_element_by_link_text("Editar ajustes").click()
            self.driver.find_element_by_link_text("General").click()
            self.driver.find_element_by_link_text("Temporalización").click()
            self.driver.find_element_by_link_text("Temporalización").location_once_scrolled_into_view
            

        except Exception as e:
            # En caso de no encontrar alguno se registra en el log
            self.log +=self._LOGS[2]+ str(e)       

        # Calculamos las fechas a cambiar

        # Mover número 'n' de semanas: 1
        # Mover a una fecha específica: 2
        if(eleccion == 1): # En caso de mover un n número de semanas 
            numero_semanas = int(fila[1])
            fecha_open = self.get_fecha('open')
            fecha_close = self.get_fecha('close')
            delta_weeks = datetime.timedelta(weeks=numero_semanas)
            inicio_actividad = fecha_open + delta_weeks
            fin_actividad = fecha_close + delta_weeks

        elif(eleccion == 2): # Adquirimos las fechas que se van a mover las actividades
            # Formato fecha: "DD-MM-AA-HH:mm"
            # DD: días
            # MM: Meses
            # AA: Años
            # HH: Horas
            # mm: Minutos
            fecha_inicio = fila[1]
            fecha_fin = fila[2]

            inicio_actividad = datetime.datetime.strptime(fecha_inicio,  '%d-%m-%Y-%H:%M')
            fin_actividad = datetime.datetime.strptime(fecha_fin,  '%d-%m-%Y-%H:%M')

        try:
            # Seteamos las fechas de inicio y de fin en el formulario
            self.set_fecha('open',inicio_actividad)
            self.set_fecha('close',fin_actividad)

            # Enviamos el formulario
            self.driver.find_element_by_id('id_submitbutton2').location_once_scrolled_into_view
            self.driver.find_element_by_id('id_submitbutton2').click()
        except Exception as e:
            # En caso de no ser encontrado se captura la excepción y  se registra en el log
            self.log +=self._LOGS[6]+ str(e)

        self.log +=self._LOGS[7]
    
    def set_fecha(self,open_or_close,fecha):
        
        # Función para cambiar fechas del formulario 

        # open_or_close toma dos valores {'open','close'}
        # Fecha es un obejto datetime donde está la fecha con hora

        select_day = Select(self.driver.find_element_by_id("id_time"+open_or_close+"_day"))
        select_month = Select(self.driver.find_element_by_id("id_time"+open_or_close+"_month"))
        select_year = Select(self.driver.find_element_by_id("id_time"+open_or_close+"_year"))
        select_hour = Select(self.driver.find_element_by_id("id_time"+open_or_close+"_hour"))
        select_minute = Select(self.driver.find_element_by_id("id_time"+open_or_close+"_minute"))
        select_day.select_by_value(str(fecha.day))
        select_month.select_by_value(str(fecha.month))
        select_year.select_by_value(str(fecha.year))
        select_hour.select_by_value(str(fecha.hour))
        select_minute.select_by_value(str(fecha.minute))

        
    def get_fecha(self,open_or_close):
        
        # Función para obtener las fechas del formulario 
        # Formato fecha: "DD-MM-AA-HH:mm"
        # DD: días
        # MM: Meses
        # AA: Años
        # HH: Horas
        # mm: Minutos

        # open_or_close toma dos valores {'open','close'}

        select_day = Select(self.driver.find_element_by_id("id_time"+open_or_close+"_day"))
        day = select_day.first_selected_option.text


        select_month = Select(self.driver.find_element_by_id("id_time"+open_or_close+"_month"))
        month = select_month.first_selected_option.get_attribute('value')

        select_year = Select(self.driver.find_element_by_id("id_time"+open_or_close+"_year"))
        year = select_year.first_selected_option.text
        
        select_hour = Select(self.driver.find_element_by_id("id_time"+open_or_close+"_hour"))
        hour = select_hour.first_selected_option.text

        select_minute = Select(self.driver.find_element_by_id("id_time"+open_or_close+"_minute"))
        minute = select_minute.first_selected_option.text

        fecha = day + '-' + month + '-' + year + '-' + hour + ':' + minute
        return datetime.datetime.strptime(fecha,  '%d-%m-%Y-%H:%M')