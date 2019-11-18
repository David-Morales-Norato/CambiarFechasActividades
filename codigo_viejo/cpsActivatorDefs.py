# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

By David A. Miranda, PhD (2017)

1. Install Anaconda Python
2. Add the conda-forge channel into environments
3. Install selenium in the environment with conda-forge
4. Install pySide in the enviroment with conda-forge
5. Install ChromeDriver: https://sites.google.com/a/chromium.org/chromedriver/downloads
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
from sys import platform
from sys import maxsize as msBits
import unicodedata
from datetime import datetime,timedelta

chromeDriverPaht = ''
logs = ''


if platform == "linux" or platform == "linux2":
    if msBits > 2**32:
        chromeDriverPaht = 'chromeDriver/Linux32/chromedriver'
    else:
        chromeDriverPaht = 'chromeDriver/Linux32/chromedriver'
elif platform == "darwin":
    chromeDriverPaht = 'chromeDriver/OSX/chromedriver'
elif platform == "win32":
    chromeDriverPaht = 'chromeDriver/Win32/chromedriver'

def ticAuthentication(nickName, password):
    wb = webdriver.Chrome(chromeDriverPaht)
    ##### Authentication #####
    wb.get('http://tic.uis.edu.co/ava/login/index.php')
    
    time.sleep(5)
    
    userName = wb.find_element_by_name('username')
    passWord = wb.find_element_by_name('password')
    
    userName.send_keys(nickName)
    passWord.send_keys(password)
    
    login_attempt = wb.find_element_by_xpath("//*[@type='submit']")
    login_attempt.submit()
    ##########################
    return wb

##### Open the course site #####
def setDateTimeTo(wb, moduleName, cpsName, openDateTime, closeDateTime, attempts):
    moduleForCPS = wb.find_element_by_link_text(moduleName)
    moduleForCPS.click()
    cpsToModify = wb.find_element_by_link_text(cpsName)
    cpsToModify.click()
    action = wb.find_element_by_link_text('Editar ajustes')
    action.click() 
    s1=wb.find_element_by_class_name('collapseexpand')
    if not s1.is_selected():
        s1.click()
        
    #### Temporalización #####
    def dateElement(nameBase, key, value):
        sl = wb.find_element_by_name(nameBase+'['+key+']')
        for opt in sl.find_elements_by_css_selector('option'):
            if opt.text == value:
                opt.click()
                break
    def setDate(nameBase, cDate):
        sw = wb.find_element_by_name(nameBase+'[enabled]')
        if not sw.is_selected():
            sw.click()
        monthOpt = {
                1:'enero', 
                2:'febrero', 
                3:'marzo', 
                4:'abril', 
                5:'mayo', 
                6:'junio', 
                7:'julio', 
                8:'agosto', 
                9:'septiembre',
                10:'octubre', 
                11:'noviembre',
                12:'noviembre'}
        dateElement(nameBase, 'day',str(cDate.day))
        dateElement(nameBase, 'month',monthOpt[cDate.month])
        dateElement(nameBase, 'year',str(cDate.year))
        dateElement(nameBase, 'hour','%02d' % cDate.hour) 
        dateElement(nameBase, 'minute','%02d' % cDate.minute) 
    
    setDate('timeopen',openDateTime)
    setDate('timeclose',closeDateTime)
    
    sw = wb.find_element_by_name('timelimit[enabled]')
    if sw.is_selected():
        sw.click()
        
    sl = wb.find_element_by_name('overduehandling')  #  Cuando el tiempo ha terminado: 
    for opt in sl.find_elements_by_css_selector('option'):
        if 'autom' in opt.text:
            opt.click()
            break
    sw = wb.find_element_by_name('timelimit[enabled]')  # Límite de tiempo
    if sw.is_selected():
        sw.click()
        
    sl = wb.find_element_by_name('attempts')  #  Número de intentos: 
    for opt in sl.find_elements_by_css_selector('option'):
        if opt.text == str(attempts):
            opt.click()
            break
        
    bt = wb.find_element_by_name('submitbutton2')  # Botón de envíar
    bt.click()

def setDateTimeToAndLogs(wb, moduleName, cpsName, openDateTime, closeDateTime, attempts):
    log1 = ''
    try:
        setDateTimeTo(wb, moduleName, cpsName, openDateTime, closeDateTime, attempts)
        log1 += '\n\t' +  cpsName + ', ' + moduleName 
        log1 += ', was activated to open at ' + str(openDateTime) 
        log1 += ' and close at ' + str(closeDateTime) + ' with ' + str(attempts) + ' attempts.'
    except:
        log1 += '\n\tError: ' +  cpsName + ', ' + moduleName + ', could not be activated, '
        log1 += 'please review the information of the course.'
    print log1
    return log1