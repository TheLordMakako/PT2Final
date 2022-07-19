#from curses import window
from cProfile import label
from tkinter import ttk
from tkinter import *
import sqlite3
import time
from Zona1 import PT1
from Zona2 import PT2
from Zona3 import PT3
from Zona4 import PT4
from Zona5 import PT5
from Zona6 import PT6
import IntegracionTuits
import LimpiezaGeneral
import CargandoABaseDeDatosV2
import Relaciones
from threading import Thread

class aplicacion:
    
    def get_Relaciones(self):
        records = self.tree5.get_children()
        for element in records:
            self.tree5.delete(element)
        if (self._bandera[9] == 1):
            self.tree5.insert("", 0,text="Codigo Relaciones" , values ="Terminado")
        else:
            self.tree5.insert("", 0,text="Codigo Relaciones" , values ="Sin_ejecutar")
    
    def relaciones(self):
        self.relacion = Thread(target = Relaciones.main)
        self.relacion.start()
        self.relacion.join()
        self._bandera[9] = 1
    
    def get_Base (self):
        records = self.tree4.get_children()
        for element in records:
            self.tree4.delete(element)
        if (self._bandera[8] == 1):
            self.tree4.insert("", 0,text="Codigo BaseDatos" , values ="Terminado")
        else:
            self.tree4.insert("", 0,text="Codigo BaseDatos" , values ="Sin_ejecutar")
    
    def Base(self):
        self.base = Thread(target = CargandoABaseDeDatosV2.main)
        self.base.start()
        self.base.join()
        self._bandera[8] = 1
        
    def get_Limpieza (self):
        records = self.tree3.get_children()
        for element in records:
            self.tree3.delete(element)
        if (self._bandera[7] == 1):
            self.tree3.insert("", 0,text="Codigo Limpieza" , values ="Terminado")
        else:
            self.tree3.insert("", 0,text="Codigo Limpieza" , values ="Sin_ejecutar")
    
    def Limpieza(self):
        self.limp = Thread(target = LimpiezaGeneral.main)
        self.limp.start()
        self.limp.join()
        self._bandera[7] = 1
        
    def get_Integracion (self):
        records = self.tree2.get_children()
        for element in records:
            self.tree2.delete(element)
        if (self._bandera[6] == 1):
            self.tree2.insert("", 0,text="Codigo Integración" , values ="Terminado")
        else:
            self.tree2.insert("", 0,text="Codigo Integración" , values ="Sin_ejecutar")
    
    def Integracion(self):
        self.inte = Thread(target = IntegracionTuits.main)
        self.inte.start()
        self.inte.join()
        self._bandera[6] = 1
    
    def get_estatus(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        
        status = list(range(6))
        for n in status:
            if (self._bandera[n] == 1):
                self.tree.insert("",n,text="Boot"+ str(n+1) +"" , values ="Terminado")
            else:
                self.tree.insert("",n,text="Boot"+ str(n+1) +"" , values ="Sin_ejecutar")
        
    
    def boot1(self):
        self.boot1s.join()
        self._bandera[0] = 1
    
    def boot2(self):
        self.boot2s.join()
        self._bandera[1] = 1
    
    def boot3(self):
        self.boot2s.join()
        self._bandera[2] = 1
    
    def boot4(self):
        self.boot2s.join()
        self._bandera[3] = 1
    
    def boot5(self):
        self.boot2s.join()
        self._bandera[4] = 1
    
    def boot6(self):
        self.boot2s.join()
        self._bandera[5] = 1
    
    def boots(self):
            self.boot1s = Thread(target = PT1.main)
            self.boot2s = Thread(target = PT2.main)
            self.boot3s = Thread(target = PT3.main)
            self.boot4s = Thread(target = PT4.main)
            self.boot5s = Thread(target = PT5.main)
            self.boot6s = Thread(target = PT6.main)
            self.boot1s.start()
            self.boot2s.start()
            self.boot3s.start()
            self.boot4s.start()
            self.boot5s.start()
            self.boot6s.start()
            self.boot1()
            self.boot2()
            self.boot3()
            self.boot4()
            self.boot5()
            self.boot6()
            
    def __init__(self, window):
            self.wind = window
            self.wind.title('Proyeto de Titulación - Sistema de análisis para la ponderación de usuarios de Twitter en temas de tendencia')
            self.wind.geometry("925x650")
            self._bandera = [0] * 10
            
            #Creando el frame container
            frame = LabelFrame (self.wind, text = 'Scripts de tuits', font=("Times New Roman", 12,"bold"))
            #Creando el frame de unificación container
            frame2 = LabelFrame (self.wind, text = 'Unificacion de Todos los Tuits', font=("Times New Roman", 12,"bold"))
            #Creando conteiner para las reglas enerales
            frame3 = LabelFrame (self.wind, text= 'Secuencia de uso de la App', font=("Times New Roman", 12,"bold"))
            regla = Label(frame3, text="1.-validar el estado de los boots")
            regla2 = Label(frame3, text ='2.-Ejecutar la descarga')
            regla3 = Label(frame3, text = '3.-Verificar el estatus hasta que todos esten en Terminado')
            regla4 = Label(frame3, text = '4.-Ya terminados los boots, ejecutar script de unificación')
            regla5 = Label(frame3, text = '5.-Terminado el script de unificación, ejecutar el de limpieza de texto')
            regla6 = Label(frame3, text = '6.-Ejecutar el script para cargar a la base de datos')
            #Estados de boots en tabla y estado
            self.tree = ttk.Treeview(frame, height= 6, columns= 2)
            self.tree.heading('#0', text = 'Boot', anchor=CENTER)
            self.tree.heading('#1', text = 'Estado', anchor=CENTER)
            #Boton 
            boton1 = ttk.Button(frame, text = 'Ejecutar', command = self.boots)     
            boton2 = ttk.Button(frame, text = 'Estatus', command = self.get_estatus)
            ##frame de unificacion
            self.tree2 = ttk.Treeview(frame2, height= 1, columns= 2)
            self.tree2.heading('#0', text = 'Codigo', anchor=CENTER)
            self.tree2.heading('#1', text = 'Estado', anchor=CENTER)
            boton3 = ttk.Button(frame2, text = 'Estatus', command=self.get_Integracion)
            boton4 = ttk.Button(frame2, text = 'Ejecutar', command = self.Integracion)
            #frame de limpieza
            frame4 = LabelFrame(self.wind, text='Limpieza de texto', font=("Times New Roman", 12,"bold"))
            self.tree3 = ttk.Treeview(frame4,height=1, columns=2)
            self.tree3.heading('#0', text = 'Codigo', anchor=CENTER)
            self.tree3.heading('#1', text = 'Estado', anchor=CENTER)
            boton5 = ttk.Button(frame4, text = 'Estatus', command=self.get_Limpieza)
            boton6 = ttk.Button(frame4, text = 'Ejecutar', command = self.Limpieza)
            #frame de relaciones
            frame7 = LabelFrame(self.wind, text='Obtiene las relaciones', font=("Times New Roman", 12,"bold"))
            self.tree5 = ttk.Treeview(frame7,height=1, columns=2)
            self.tree5.heading('#0', text = 'Codigo', anchor=CENTER)
            self.tree5.heading('#1', text = 'Estado', anchor=CENTER)
            boton9 = ttk.Button(frame7, text = 'Estatus', command=self.get_Relaciones)
            boton10 = ttk.Button(frame7, text = 'Ejecutar', command = self.relaciones)
            #frame de base de datos
            frame5 = LabelFrame(self.wind, text='Base de datos', font=("Times New Roman", 12,"bold"))
            self.tree4 = ttk.Treeview(frame5,height=1, columns=2)
            self.tree4.heading('#0', text = 'Codigo', anchor=CENTER)
            self.tree4.heading('#1', text = 'Estado', anchor=CENTER)
            boton7 = ttk.Button(frame5, text = 'Estatus', command=self.get_Base)
            boton8 = ttk.Button(frame5, text = 'Ejecutar', command = self.Base)
            #frame de información
            frame6 = LabelFrame (self.wind, text= 'Información', font=("Times New Roman", 16,"bold"))
            Info = Label(frame6, text="INSTITUTO POLITÉCNICO NACIONAL", font=("Times New Roman", 14,"bold"))
            Info2 = Label(frame6, text ='Unidad Profesional Interdisciplinaria en Ingeniería y Tecnologías Avanzadas', font=("Times New Roman", 10,"bold"))
            Info3 = Label(frame6, text = 'Academia Telemática', font=("Times New Roman", 12,"bold"))
            Info4 = Label(frame6, text = 'PROYECTO TERMINAL',font=("Times New Roman", 12,"bold"))
            Info5 = Label(frame6, text = 'Presenta:',font=("Times New Roman", 12,"bold"))
            Info6 = Label(frame6, text = 'C. Ortiz Romero Héctor Arturo', font=("Times New Roman", 12,"bold"))
            Info7 = Label(frame6, text = 'Asesoras:', font=("Times New Roman", 12,"bold"))
            Info8 = Label(frame6, text = 'Dra. Obdulia Pichardo Lagunas', font=("Times New Roman", 12,"bold"))
            Info9 = Label(frame6, text = 'Dra. Bella Citlali Martínez Seis', font=("Times New Roman", 12,"bold"))
            #Posiciones
            frame3.grid(row = 1, column = 0, pady= 2, padx=15, ipady=10, sticky=W + E)
            frame.grid(row = 0, column = 1, pady=12, padx=15, sticky=N)
            frame2.grid(row = 0, column = 1, pady=3, padx=10, sticky=S)
            frame4.grid(row=1, column=1, pady=2, sticky=N)
            frame7.grid(row=1, column=1, pady=2, sticky=S)
            frame5.grid(row=2,column=1, pady=2, sticky=N)
            frame6.grid(row=0, column=0, pady=10, padx=15, ipady=10)
            Info.grid(row=0, column=0, pady =2)
            Info2.grid(row=1, column=0, pady =2)
            Info3.grid(row=2, column=0, pady =2)
            Info4.grid(row=3, column=0, pady =2)
            Info5.grid(row=4, column=0, pady =2)
            Info6.grid(row=5, column=0, pady =2)
            Info7.grid(row=6, column=0, pady =2)
            Info8.grid(row=7, column=0, pady =2)
            Info9.grid(row=8, column=0, pady =2)
            self.tree.grid(row = 0, column= 0, columnspan=2)
            self.tree2.grid(row=0, column=0,columnspan=2)
            self.tree3.grid(row=0, column=0,columnspan=2)
            self.tree4.grid(row=0, column=0,columnspan=2)
            self.tree5.grid(row=0, column=0,columnspan=2)
            regla.grid(row=0, column=0, pady =2, sticky=W)
            regla2.grid(row=1, column=0, pady =2, sticky=W)
            regla3.grid(row=2, column=0, pady =2, sticky= W)
            regla4.grid(row=3, column=0, pady =2, sticky= W)
            regla5.grid(row=4, column=0, pady =2, sticky= W)
            regla6.grid(row=5, column=0, pady =2, sticky= W)
            boton1.grid(row = 1, column= 1, sticky = W + E)
            boton2.grid(row = 1, column = 0, sticky = W + E)
            boton3.grid(row=1, column= 0,sticky= W + E)
            boton4.grid(row=1, column=1, sticky= W + E)
            boton5.grid(row=1, column= 0,sticky= W + E)
            boton6.grid(row=1, column=1, sticky= W + E)
            boton7.grid(row=1, column= 0,sticky= W + E)
            boton8.grid(row=1, column=1, sticky= W + E)
            boton9.grid(row=1, column= 0,sticky= W + E)
            boton10.grid(row=1, column=1, sticky= W + E)
            self.get_estatus()
            self.get_Integracion()
            self.get_Limpieza()
            self.get_Base()
            self.get_Relaciones()
            
            
    
    
    
         

if __name__ == '__main__':
	window = Tk()
	app = aplicacion(window)
	window.mainloop()
    