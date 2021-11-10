# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from tkinter import Label, Button, Entry, Frame, Tk, messagebox, filedialog
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from tkinter.ttk import Combobox
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import time
from IPython import display


MODELOS=['Elija una opcion','Modelo general estructura ARX', 'Modelo de Primer Orden']




class MainFrame(Frame):
    def __init__(self, master=None):
        super().__init__(master, width=500, height=500)
        self.master = master
        self.grid()
        #self.pack()
        self.create_widgets()


    def ElegirOpciones(self):
        if (self.cmbMetodos.get() == MODELOS[1]):
            self.ARX_widgets()
        elif (self.cmbMetodos.get() == MODELOS[2]):
            self.primer_orden_widgets()
            #messagebox.showinfo(title="Entro la funcion", message=" Valio madre")

    def hide_widgets(self):
        # clear window
        self.grid_forget()

    def m(self,index):
        if (index < 0):
            return 0
        else:
            return 1

    def mArray(self, lenght, startIndex):
        mArr = []
        for i in range(lenght):
            mArr.append(self.m(startIndex - i))
        return mArr


    def plot(self):

        fig=Figure()

        ax = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)
        canvas_wid = FigureCanvasTkAgg(fig, master=root)
        canvas_wid.get_tk_widget().grid(row=0,column=1)
        canvas_wid.draw()

        self.redraw(canvas_wid,ax,ax2)


    def iteracion_primer_orden(self):
        if(self.pausa==False):
            self.UN_i = float(self.txtmk.get())
            self.pk_i = float(self.txtpk.get())
            self.UN[self.i] = self.UN_i
            self.pk.append(self.pk_i)
            self.YN[self.i] = self.a1 * self.YN[self.i - 1] + self.b1 * self.UN[self.i - 1 - self.d] + self.b2 * self.UN[self.i - 2 - self.d] + self.pk[self.i]
            self.data.append(self.YN[self.i])
            self.un.append(self.UN[self.i])
            print(self.i)
            self.plot()
            self.i=self.i+1
            print(self.i)
            print(self.pausa)
        root.after(1000, self.iteracion_primer_orden)



    def redraw(self, canvas,ax,ax2):
        ax.clear()
        #ax.set_xlabel('Tiempo')
        ax.set_ylabel('Respuesta c(k)')
        ax.plot(self.data)
        ax2.clear()
        ax2.set_xlabel('Tiempo')
        ax2.set_ylabel('Entrada m(k)')
        ax2.plot(self.un)
        canvas.draw()




    def create_widgets(self):


        Label(self, text="Modelo:").place(x=30, y=90)

        self.btnCalcular = Button(self, text="Configuracion", command=self.ElegirOpciones)
        self.btnCalcular.place(x=100, y=150)


        self.cmbMetodos = Combobox(self, width="20", values=MODELOS, state="readonly")
        self.cmbMetodos.place(x=100, y=90)
        self.cmbMetodos.current(0)



    def ARX_widgets(self):
        for child in self.winfo_children():
            child.destroy()

        self.create_widgets()

        Label(self, text="Coeficiente d:").place(x=30, y=220)
        self.txtd = Entry(self, width=15)
        self.txtd.place(x=300, y=220)


        Label(self, text="Escribe las variables a's (empezando por a1)").place(x=30, y=250)
        self.txtn = Entry(self, width=15)
        self.txtn.place(x=300, y=250)

        Label(self, text="Escribe las variables a's (empezando por b0)").place(x=30, y=280)
        self.txtm = Entry(self, width=15)
        self.txtm.place(x=300, y=280)

        self.btnEmpezar = Button(self, text="Empezar", command=self.estructura_ARX)
        self.btnEmpezar.place(x=150, y=310)

        Label(self, text="Resultado").place(x=30, y=340)
        self.txtRes = Entry(self, width=30)
        self.txtRes.place(x=100, y=340)




    def estructura_ARX(self):

        d = int(self.txtd.get())
        entradas_a = (self.txtn.get().split(" "))
        aIndex = list(map(float, entradas_a))

        entradas_b = (self.txtm.get().split(" "))
        bIndex = list(map(float, entradas_b))

        startIndex = 0;

        for i in range(len(aIndex) - 1, 0, -1):
            if (aIndex[i] == 0):
                startIndex = startIndex + 1  # if last values of a index is 0 just remove it
                continue
            break  # when find the first "last" value of the array dif o zero just exit the loop

        aIndex = aIndex[0:-startIndex]  # define the new array with the zeros out
        # initiate c array
        c = []
        for k in range(32):
            if (k < len(aIndex)):  # Initial values = 0
                c.append(0)
            else:  # start to compute
                subCArray = c[-len(aIndex):]  # Get all the c values of the array to compute the c(k)
                subMArray = self.mArray(len(bIndex), k - d)  # Get all the m values of the array to compute the c(k)
                c.append(np.dot(aIndex, subCArray) + np.dot(bIndex, subMArray))

        # messagebox.showinfo(title="Entro la funcion", message=str(theta))
        # result = int(self.txtRes.get())


        self.txtRes.delete(0, 'end')
        self.txtRes.insert(0, c)
        messagebox.showinfo("Resultado", c)




    def pausar(self):
        self.pausa=True



    def primer_orden(self):


        self.pausa= False
        self.K = float(self.txtK.get())
        self.Tau = float(self.txtTau.get())
        self.ThetaP = float(self.txtThetaP.get())
        self.T = float(self.txtT.get())

        self.d = int(self.ThetaP//self.T)
        self.Theta=self.ThetaP-self.d*self.T
        self.m=1-(self.Theta/self.T)

        self.a1 = np.exp(-self.T / self.Tau)
        self.b1 = self.K * (1 - np.exp(-(self.m * self.T) / self.Tau))
        self.b2 = self.K * (np.exp(-(self.m * self.T) / self.Tau) - np.exp(-self.T / self.Tau))



        self.YN = np.zeros(100)
        self.UN = np.zeros(100)

        self.i = 0
        self.data = []
        self.pk = []
        self.un = []



        self.btnIteracion = Button(self, text="para", command=self.pausar)
        self.btnIteracion.place(x=150, y=480)

        if(self.pausa==False):
            self.iteracion_primer_orden()
        root.after(1000, )

   # messagebox.showinfo(title="Entro la funcion", message=str(theta))
        # result = int(self.txtRes.get())




    def primer_orden_widgets(self):

        for child in self.winfo_children():
            child.destroy()

        self.create_widgets()

        Label(self, text="Ganancia estática (K):").place(x=30, y=180)
        self.txtK = Entry(self, width=15)
        self.txtK.place(x=300, y=180)

        Label(self, text="Constante de tiempo (Tau):").place(x=30, y=220)
        self.txtTau = Entry(self, width=15)
        self.txtTau.place(x=300, y=220)

        Label(self, text="Tiempo muerto analógico (Theta prima)").place(x=30, y=250)
        self.txtThetaP = Entry(self, width=15)
        self.txtThetaP.place(x=300, y=250)

        Label(self, text="Intervalo de Muestreo (T)").place(x=30, y=280)
        self.txtT = Entry(self, width=15)
        self.txtT.place(x=300, y=280)

        Label(self, text="Magnitud del escalon m(k)").place(x=30, y=310)
        self.txtmk = Entry(self, width=15)
        self.txtmk.place(x=300, y=310)

        Label(self, text="Magnitud del escalon p(k)").place(x=30, y=340)
        self.txtpk = Entry(self, width=15)
        self.txtpk.place(x=300, y=340)

        self.btnEmpezar = Button(self, text="Empezar", command=self.primer_orden)
        self.btnEmpezar.place(x=150, y=380)

        Label(self, text="Resultado").place(x=30, y=410)
        self.txtRes = Entry(self, width=30)
        self.txtRes.place(x=100, y=410)

        




root = Tk()
#root.geometry("800x700")
app = MainFrame(master=root)
app.mainloop()


