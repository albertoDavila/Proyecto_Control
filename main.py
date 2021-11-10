
from mainFrame import MainFrame
from tkinter import Tk

def main():
    root = Tk()
    #root.geometry("800x700")
    app = MainFrame(master=root)
    root.after(1000, app.iteracion_primer_orden)
    app.mainloop()
if __name__=="__main__":
    main()