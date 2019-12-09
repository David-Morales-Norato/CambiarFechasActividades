import numpy as np
import datetime
from Robot import Robot
from selenium.webdriver.support.ui import Select

class robot_cambiar_fechas(Robot):
    def __init__(self, DRIVER_PATH):
        
        super().__init__(DRIVER_PATH)
        # String que tiene el id de los campos para seleccionar la fecha

        # delta de horas entre cada inicio y fin de una actividad
        self.DELTA_HORAS = 24
        logs_cambiar_fechas = [
            '[-5] Error al llenar el formulario para cambiar fechas de la actividad| Exception: ',
            '[5]  Se diligenció correctamente el formulario para cambiar fechas de la actividad']
        self._LOGS = self._LOGS + logs_cambiar_fechas


    def tratamiento_curso(self,datos, variables_de_control):
        # Eleccion es el primer elemento
        eleccion = variables_de_control[0]
        # Contador el segundo elemento
        contador = variables_de_control[1]
        
        if(eleccion !=3):
            # Obtenemos los datos sin contar el primer elemento
            datos = np.array(datos[1:])
            # Se separan los datos
            fila = datos[:,contador]
            # Adquirimos la actividar a cambiarle la fecha
            ACTIVIDAD = fila[0] 
            # Si la elección es 1 o 2 los datos vienen empaquetados de fomra similar
        else:
            # Si la elección es 3 los datos tienen 3 hojas y toca hacer tratamiento especial
            # Obtenemos la primera hoja que tiene nombres cursos, ids y actividades
            primera_hoja = datos[1]
            # Lo hacemos un np.array
            primera_hoja = np.array(primera_hoja)
            # Se separan los datos
            fila = primera_hoja[:,contador]
            # Adquirimos el CPL a calificar
            ACTIVIDAD = fila[1]
        try:
            # Se busca la actividad a cambiar la fecha
            actividad = self.driver.find_element_by_partial_link_text(ACTIVIDAD)
            actividad.location_once_scrolled_into_view
            actividad.click() 
            
            # Se abre camino hasta el formulario para cambiar fechas
            self.driver.find_element_by_link_text("Editar ajustes").click()
            collapsable = self.driver.find_element_by_xpath("//*[@id='id_general' and @class='clearfix collapsible']")
            collapsable.find_element_by_link_text("General").click()
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

        elif(eleccion == 3):
            # Obtenemos el resto de las hojas
            segunda_hoja = datos[2]
            tercera_hoja = datos[3]

            
            
            # Obtenemos el nombre del curso y su primer encuentro para cambiarle la fecha
            nombre_curso = fila[2]
            # Primer día de la semana en que se encuentra el curso para así modificarlo
            # 36 horas antes de que empieze
            primer_encuentro = fila[3]
            
            # Según sus agenda de semanas y lecciones 
            lecciones = segunda_hoja.get(nombre_curso)

            # Las actividades corresponden a una lección, ejemplo: CPS1.3, lección: 1.3
            leccion_actividad = ACTIVIDAD[-3:]

            # Obtenemos la posición de esa lección
            # Esa misma va a ser la semana que le corresponde a la actividad
            indice_leccion = lecciones.index(leccion_actividad)
            # y esa misma posición corresponde a la fecha para esa semana
            # Leemos la fecha en la posición de esa lección
            fecha_semana_sin_hora = str(tercera_hoja[indice_leccion]).split(" ")[0]

            # PRIMER ENCUENTRO TIENE ESTE FORMATO:
            # día:hora_inicio-hora_fin
            # Solo nos importa hora_inicio y día
            # Obtenemos el día de la semana que se encuentran por primera vez
            # se resta 1 para que quede: # 0 Lunes, 1 Martes, 2 Miércoles, 3 Jueves, 4 Viernes, 5 Sábado, 6 Domingo
            día_semana_actividad = str(int(primer_encuentro.split(":")[0])-1)
            # Obtenemos la hora de inicio del primer encuentro.
            hora_primer_encuentro = primer_encuentro.split(":")[1].split("-")[0]

            # Cuadramos la fecha con hora de inicio de la actividad
            # minutos 00
            fecha_semana_con_hora = fecha_semana_sin_hora +'-'+hora_primer_encuentro+':00'
            fecha_total_semana_de_actividad = datetime.datetime.strptime(fecha_semana_con_hora,'%Y-%m-%d-%H:%M') 
            inicio_actividad = self.proximo_dia_y_hora_actividad(fecha_total_semana_de_actividad,día_semana_actividad)

            fin_actividad = inicio_actividad + datetime.timedelta(hours=self.DELTA_HORAS)
            pass
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

    def proximo_dia_y_hora_actividad(self,d, weekday):
        days_ahead = int(weekday) - d.weekday()
        if days_ahead <= 0: # Target day already happened this week
            days_ahead += 7
        return d + datetime.timedelta(days_ahead) - datetime.timedelta(hours=36)
