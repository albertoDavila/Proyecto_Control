# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from tkinter import Label, Button, Entry, Frame, Tk, messagebox, filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from tkinter.ttk import Combobox
import numpy as np


MODELOS=['Elija una opcion','Modelo general estructura ARX', 'Modelo de Primer Orden']




class MainFrame(Frame):
    def __init__(self, master=None):
        super().__init__(master, width=500, height=500)
        self.master = master
        self.grid()
        #self.pack()

        self.create_widgets()

        self.mk = []
        self.pk = []
        self.ek = []
        self.ck = []
        self.rk=[]

        self.MK = np.zeros(100)
        self.EK = np.zeros(100)
        self.PK = np.zeros(100)
        self.CK = np.zeros(100)
        self.Is_graph=False

        self.Modo='Manual'
        self.Modelo_actual='Niguno'
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



    def plot(self):
        self.Is_graph=True
        fig=Figure()
        ax = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)
        canvas_wid = FigureCanvasTkAgg(fig, master=root)
        canvas_wid.get_tk_widget().grid(row=0,column=1)
        canvas_wid.draw()
        self.redraw(canvas_wid,ax,ax2)




    def redraw(self, canvas,ax,ax2):
        ax.clear()
        #ax.set_xlabel('Tiempo')
        ax.set_ylabel('Valor')
        ax.plot(self.ck)
        ax.plot(self.rk)
        ax.legend(['c(k)', 'r(k)'])

        ax2.clear()
        ax2.set_xlabel('Tiempo')
        ax2.set_ylabel('Valor')
        ax2.plot(self.mk)
        ax2.plot(self.pk)
        ax2.legend(['m(k)', 'p(k)'])
        print('el MK es', self.mk)
        print('el PK es', self.pk)
        canvas.draw()






    def create_widgets(self):
        Label(self, text="Modelo:").place(x=30, y=90)
        self.btnCalcular = Button(self, text="Seleccionar", command=self.ElegirOpciones)
        self.btnCalcular.place(x=350, y=90)
        self.cmbMetodos = Combobox(self, width="20", values=MODELOS, state="readonly")
        self.cmbMetodos.place(x=100, y=90)
        self.cmbMetodos.current(0)
        self.btnReiniciar = Button(self, text="Reiniciar Programa", command=self.resetAll)
        self.btnReiniciar.place(x=350, y=120)





    def resetAll(self):
        for child in self.winfo_children():
            child.destroy()
        self.create_widgets()




    def Automatico_widgets(self):
        for child in self.winfo_children():
            child.destroy()

        self.create_widgets()

        Label(self, text="Ganancia estática (Kc):").place(x=30, y=180)
        self.txtKc = Entry(self, width=15)
        self.txtKc.place(x=300, y=180)

        Label(self, text="Constante de tiempo integral(Ti):").place(x=30, y=220)
        self.txtTi = Entry(self, width=15)
        self.txtTi.place(x=300, y=220)

        Label(self, text="Constante derivativa (Td)").place(x=30, y=250)
        self.txtTd = Entry(self, width=15)
        self.txtTd.place(x=300, y=250)

        Label(self, text="Magnitud del escalon p(k)").place(x=30, y=310)
        self.txtpk = Entry(self, width=15)
        self.txtpk.place(x=300, y=310)

        Label(self, text="Magnitud del escalon r(k)").place(x=30, y=340)
        self.txtrk = Entry(self, width=15)
        self.txtrk.place(x=300, y=340)

        if self.Modo=='Manual':
            Label(self, text="Intervalo de Muestreo (T)").place(x=30, y=280)
            self.txtT = Entry(self, width=15)
            self.txtT.place(x=300, y=280)



        elif self.Modo == 'Automatico':
            self.btnIteracion = Button(self, text="Pausar", command=self.pausar)
            self.btnIteracion.place(x=280, y=410)
            self.btnAutomatico = Button(self, text="Modo automático", highlightbackground='green',
                                        command=self.Setup_Modo_Automatico)
            self.btnAutomatico.place(x=350, y=410)


        Label(self, text="Resultado").place(x=30, y=380)
        self.txtRes = Entry(self, width=30)
        self.txtRes.place(x=100, y=380)

        self.btnEmpezar = Button(self, text="Empezar", command=self.PID)
        self.btnEmpezar.place(x=150, y=410)


    def PID(self):
        self.pausa = False
        self.Kc = float(self.txtKc.get())
        self.Ti = float(self.txtTi.get())
        self.Td = float(self.txtTd.get())
        if self.Modo=='Manual':
            self.r0 = self.ck[-1]
            self.T = float(self.txtT.get())
            self.ek.append(self.r0)
        else:
            self.r0 = float(self.txtrk.get())
            self.ek.append(self.r0)


        print('Valor de Kc', self.Kc)
        print('Valor de T', self.T)
        print('Valor de Ti', self.Ti)
        print('Valor de Td', self.Td)



        self.B0 = self.Kc*(1 + (self.T / self.Ti) + (self.Td / self.T))
        self.B1 = self.Kc*(-1 - (2 * self.Td / self.T))
        self.B2 = self.Kc*(self.Td / self.T)

        self.i = 0
        self.btnIteracion = Button(self, text="Pausar", command=self.pausar)
        self.btnIteracion.place(x=280, y=410)

        if (self.pausa == False):
            self.iteracion_PID()


    def iteracion_PID(self):
        if (self.pausa == False):
            self.EK[self.i] = self.ek[-1]
            self.pk_i = float(self.txtpk.get())
            self.PK[self.i] = self.pk_i
            self.MK[self.i] = self.MK[self.i - 1] + self.B0 * self.EK[self.i ]+self.B1 * self.EK[self.i - 1 ] + self.B1 * self.EK[self.i - 1 ] + self.PK[self.i]
            self.mk.append(self.MK[self.i])
            self.ek.append(self.EK[self.i])
            self.pk.append(self.PK[self.i])
            print(self.cmbMetodos.get() )


            self.plot()
            self.txtRes.delete(0, 'end')
            self.txtRes.insert(0, self.mk)
            self.i = self.i + 1


        if(self.Modelo_actual=='Primer orden'):
            root.after(1000, self.iteracion_primer_orden)
        elif(self.Modelo_actual=='ARX'):
            root.after(1000, self.iteracion_ARX())

    def Setup_Modo_Automatico(self):
        if self.btnAutomatico['highlightbackground']=='red':
            self.btnAutomatico['highlightbackground'] = 'green'
            self.Modo='Automatico'
            self.pausar()
            self.Automatico_widgets()
        else:
            self.btnAutomatico['highlightbackground'] == 'red'
            self.Modo = 'Manual'
            self.pausar()
            if self.Modelo_actual=='Primer orden':
                self.primer_orden_widgets()
            elif self.Modelo_actual=='ARX':
                self.ARX_widgets()


    def ARX_widgets(self):
        for child in self.winfo_children():
            child.destroy()

        self.create_widgets()
        self.cmbMetodos.set(MODELOS[1])
        Label(self, text="Coeficiente d:").place(x=30, y=220)
        self.txtd = Entry(self, width=8)
        self.txtd.place(x=400, y=220)

        Label(self, text="4 Coeficientes de a's separados por comas (a1,a2,a3, a4)").place(x=30, y=250)
        self.txtA = Entry(self, width=8)
        self.txtA.place(x=400, y=250)

        Label(self, text="4 Coeficientes de b's separados por comas (b0,b1,b2,b3)").place(x=30, y=280)
        self.txtB = Entry(self, width=8)
        self.txtB.place(x=400, y=280)
        Label(self, text="Magnitud del escalon m(k)").place(x=30, y=310)
        self.txtmk = Entry(self, width=15)
        self.txtmk.place(x=300, y=310)
        Label(self, text="Magnitud del escalon p(k)").place(x=30, y=340)
        self.txtpk = Entry(self, width=15)
        self.txtpk.place(x=300, y=340)

        self.btnEmpezar = Button(self, text="Empezar", command=self.ARX)
        self.btnEmpezar.place(x=150, y=370)

        Label(self, text="Resultado").place(x=30, y=400)
        self.txtRes = Entry(self, width=30)
        self.txtRes.place(x=100, y=400)

    def ARX(self):
        self.Modelo_actual='ARX'
        self.pausa = False
        self.d = int(self.txtd.get())
        self.entradas_a = (self.txtA.get().split(","))
        self.aIndex = list(map(float, self.entradas_a))
        self.entradas_b = (self.txtB.get().split(","))
        self.bIndex = list(map(float, self.entradas_b))
        self.i = 0

        self.mk.append(float(self.txtpk.get()))
        self.pk.append(float(self.txtpk.get()))

        self.btnIteracion = Button(self, text="Pausar", command=self.pausar)
        self.btnIteracion.place(x=280, y=430)

        self.btnAutomatico = Button(self, text="Modo automático", highlightbackground='red',
                                    command=self.Setup_Modo_Automatico)
        self.btnAutomatico.place(x=350, y=430)

        if (self.pausa == False):
            self.iteracion_ARX()

    def iteracion_ARX(self):
        if(self.pausa==False):
            self.MK[self.i] = self.mk[-1]
            self.PK[self.i] = self.pk[-1]
            self.CK[self.i] = self.aIndex[0] * self.CK[self.i - 1] + self.aIndex[1] * self.CK[self.i - 2]+ self.aIndex[2] * self.CK[self.i - 3]+self.aIndex[3] * self.CK[self.i - 4]+self.bIndex[0] * self.MK[self.i - 1] + self.bIndex[1] * self.MK[self.i - 2]+ self.bIndex[2] * self.MK[self.i - 3]+self.bIndex[3] * self.MK[self.i - 4] + self.PK[self.i]

            self.ck.append(self.CK[self.i])
            self.mk.append(self.MK[self.i])

            if self.Modo == 'Manual':
                self.rk.append(self.CK[self.i])
                self.pk.append(self.PK[self.i])
            else:
                self.rk.append(float(self.txtrk.get()))
                self.pk.append(float(self.txtpk.get()))


            self.plot()
            self.txtRes.delete(0, 'end')
            self.txtRes.insert(0, self.ck)

            self.i=self.i+1

        if self.Modo == 'Manual':
            root.after(1000, self.iteracion_ARX)
        elif self.Modo == 'Automatico':
            root.after(1000, self.iteracion_PID)




    def pausar(self):
        self.pausa=True



    def primer_orden(self):
        self.pausa= False
        self.Modelo_actual='Primer orden'
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
        self.i = 0

        self.mk.append(float(self.txtpk.get()))
        self.pk.append(float(self.txtpk.get()))

        self.btnIteracion = Button(self, text="Pausar", command=self.pausar)
        self.btnIteracion.place(x=280, y=410)

        self.btnAutomatico = Button(self, text="Modo automático", highlightbackground='red', command=self.Setup_Modo_Automatico)
        self.btnAutomatico.place(x=350, y=410)

        if(self.pausa==False):
            self.iteracion_primer_orden()
        #root.after(1000, )

   # messagebox.showinfo(title="Entro la funcion", message=str(theta))
        # result = int(self.txtRes.get())
    def iteracion_primer_orden(self):
        if(self.pausa==False):
            self.MK[self.i] = self.mk[-1]
            self.PK[self.i] = self.pk[-1]
            self.CK[self.i] = self.a1 * self.CK[self.i - 1] + self.b1 * self.MK[self.i - 1 - self.d] + self.b2 * self.MK[self.i - 2 - self.d] + self.PK[self.i]
            self.ck.append(self.CK[self.i])
            self.mk.append(self.MK[self.i])
            if self.Modo=='Manual':
                self.rk.append(self.CK[self.i])
                self.pk.append(self.PK[self.i])
            else:
                self.rk.append(float(self.txtrk.get()))
                self.pk.append(float(self.txtpk.get()))

            self.plot()
            self.txtRes.delete(0, 'end')
            self.txtRes.insert(0, self.ck)

            self.i=self.i+1
        if self.Modo == 'Manual':
            root.after(1000, self.iteracion_primer_orden)
        elif self.Modo =='Automatico':
            root.after(1000, self.iteracion_PID)



    def primer_orden_widgets(self):
        for child in self.winfo_children():
            child.destroy()
        self.create_widgets()
        self.cmbMetodos.set(MODELOS[2])
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
        Label(self, text="Resultado").place(x=30, y=380)
        self.txtRes = Entry(self, width=30)
        self.txtRes.place(x=100, y=380)
        self.btnEmpezar = Button(self, text="Empezar", command=self.primer_orden)
        self.btnEmpezar.place(x=150, y=410)



        




root = Tk()
root.title('Proyecto Ingenieria de Control')
root.geometry("800x700")
app = MainFrame(master=root)

app.mainloop()


