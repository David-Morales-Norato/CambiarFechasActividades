#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 19:05:19 2017

@author: David A. Miranda, Ph.D

Its GUI was created with wxglade
"""

from getCPSDataFromXLS import *
from cpsActivatorDefs import *
import os.path
import wx

class MainWindows(wx.Frame):
    def __init__(self, parent):
        self.coursesCPSActivationData = ""
        self.courses = None
        self.cps = None
        self.calendar = None
        self.swError = None
        self.cpsXLSData = None
        self.logs = None
    
        wx.Frame.__init__(self,parent, id=wx.ID_ANY, title='CPS Activator Robot', size=(300,240), style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panel = wx.Panel(self)
        
        self.stFilePath = wx.StaticText(self.panel, label=self.coursesCPSActivationData, style=wx.ALIGN_CENTRE)
        self.stNickName = wx.StaticText(self.panel, label="Nombre de usuario: ")
        self.etNickNane = wx.TextCtrl(self.panel, size=(280, -1))
        self.stPassWord = wx.StaticText(self.panel, label="Contraseña: ")
        self.etPassWord = wx.TextCtrl(self.panel, size=(280, -1), style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        
        self.btGetFilePath = wx.Button(self.panel, label="Cargar datos", size=(280,-1))
        self.btGetFilePath.Bind(wx.EVT_BUTTON, self.getData)
        
        self.btStartRobot = wx.Button(self.panel, label="Despertar al Robot", size=(280,-1))
        self.btStartRobot.Bind(wx.EVT_BUTTON, self.startRobot)
        
        self.windowSizer = wx.BoxSizer()
        self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)
        
        self.sizer = wx.GridBagSizer(8, 1)
        self.sizer.Add(self.stFilePath   , (0, 1))
        self.sizer.Add(self.btGetFilePath, (1, 1), border=25)
        self.sizer.Add(self.stNickName   , (2, 1))
        self.sizer.Add(self.etNickNane   , (3, 1))
        self.sizer.Add(self.stPassWord   , (4, 1))
        self.sizer.Add(self.etPassWord   , (5, 1))
        self.sizer.Add(self.btStartRobot , (6, 1), border=25)
        
        self.border = wx.BoxSizer()
        self.border.Add(self.sizer, 1, wx.CENTER, 1)
        
        self.panel.SetSizerAndFit(self.border)  
        self.SetSizerAndFit(self.windowSizer)
        
        self.SetMinSize((300,240))
        self.SetMaxSize((300,240))
        self.Maximize()
        self.Centre()
        self.Show()
    
    def getData(self, e):
        openFileDialog = wx.FileDialog(self, "Seleccione el archivo de datos", "", "", 
                                       "Excel fles (*.xlsx)|*.xlsx", 
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        self.stFilePath.SetLabelText(openFileDialog.GetPath())
        self.coursesCPSActivationData = self.stFilePath.GetLabelText()
        #print self.stFilePath.GetLabelText()
        openFileDialog.Destroy()
        if not os.path.isfile(self.coursesCPSActivationData):
            self.stFilePath.SetLabelText('<< Debe cargar datos ...>>')

    def loadData(self,e):
        if os.path.isfile(self.coursesCPSActivationData):
            courses, cps, calendar, swError, cpsXLSData, logs = getCPSDataFromXLS(self.coursesCPSActivationData)
            self.courses    = courses
            self.cps        = cps
            self.calendar   = calendar
            self.swError    = swError
            self.cpsXLSData = cpsXLSData
            self.logs       = logs
        else:
            self.stFilePath.SetLabelText('<< Debe cargar datos ...>>')

    def startRobot(self, e):
        swOk = True
        nickName = self.etNickNane.GetValue()
        passWord = self.etPassWord.GetValue()

        if len(nickName) < 3 or len(passWord) < 3 :
            swOk = False
            message = 'Usted se debe autenticar, para ello se requiere:'
            if len(nickName) < 3:
                message += '\n\tSu nombre de usuario.'
            if len(passWord) < 3:
                message += '\n\tSu contraseña.'
            dlg = wx.MessageDialog(self, message, 'Error', wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()
        
        if swOk and not os.path.isfile(self.coursesCPSActivationData):
            swOk = False
            self.getData(self)
            self.startRobot(self)

        if swOk:
            #print 'NickName: ', nickName
            #print 'PassWord: ', passWord
            courses    = self.courses
            cps        = self.cps
            calendar   = self.calendar
            swError    = self.swError
            cpsXLSData = self.cpsXLSData
            logs       = self.logs
            
            self.loadData(self)
    
            wb = ticAuthentication(nickName,passWord)
        
            jiTTDeltaTime = timedelta(hours=36)
            jiTTTeacherTime = timedelta(hours=2)
        
            if swError:
                print('Error: it was not possible to obtain valid information from ' + self.coursesCPSActivationData)
            else:
                row = cpsXLSData['logs'].max_row
                cpsXLSData['logs'].cell(row=row+1, column=1).value = datetime.now()
                for course in courses:
                    row += 1
                    cGroup = course['group']     ; cpsXLSData['logs'].cell(row=row, column=2).value = cGroup
                    cTheacher = course['teacher']; cpsXLSData['logs'].cell(row=row, column=3).value = cTheacher
                    cLink = course['link']       ; cpsXLSData['logs'].cell(row=row, column=4).value = cLink
                    cWeekDay = course['weekDay'] ; cpsXLSData['logs'].cell(row=row, column=5).value = cWeekDay
                    chour = course['hour']       ; cpsXLSData['logs'].cell(row=row, column=6).value = chour
                    try:
                        wb.get(cLink)
                        log = 'Group: ' + str(cGroup)
                        log += ', Teacher: ' +  str(cTheacher)
                        log += ', Link: ' + str(cLink)
                        swOk = True
                    except:
                        log = '\nError: the excel data file contain invalid rows ...'
                        swOk = False
                    print(log)
                    cpsLog = ''
                    if swOk:
                        for c in cps:
                            cName = c['courseName']
                            cpsName = c['cpsName'] 
                            cModule = c['module']  
                            cWeek = c['week']
                            cAttempts = c['attempts']
                            mD = calendar[cWeek] + timedelta(hours=chour)
                            days = mD.weekday() - cWeekDay
                            openDateTime  = (mD - timedelta(days=days))-jiTTDeltaTime
                            closeDateTime = (mD - timedelta(days=days))-jiTTTeacherTime
                            cpsLog +=setDateTimeToAndLogs(wb, cModule, cpsName, openDateTime, closeDateTime, cAttempts)
                        cpsXLSData['logs'].cell(row=row, column=7).value = log+cpsLog
                    logs += '\n' + log + cpsLog
            cpsXLSData.save(self.coursesCPSActivationData)                
            wb.quit()

app = wx.App(False)
win = MainWindows(None)
app.MainLoop()