
from ast import Delete
from logging import root
from pydoc import text
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import *
from tkinter import messagebox
from turtle import width
from BBDD import *
import sqlite3 as sq
import os
from datetime import datetime
from tkcalendar import Calendar, DateEntry
from flask_babel import Babel


class GUI(bbdd):
    def __init__(self) -> None:
        super().__init__()
        self.fecha = datetime.now()
        self.root = Tk()
        self.root.title("Seguimiento Proyectos")
        self.root.resizable(0, 0)
        self.root.geometry("350x600")
        # ---------------menu----------------
        self.barraMenu = Menu(self.root)
        self.root.config(menu=self.barraMenu, width=300, height=450)
        self.conexionMenu = Menu(self.barraMenu, tearoff=0)
        self.conexionMenu.add_command(
            label="verificar", command=self.__verificar_conexion)
        self.conexionMenu.add_command(label="salir", command=self.__salir)
        self.barraMenu.add_cascade(label="BBDD", menu=self.conexionMenu)
        # ---------------------------------------------------

        self.menuInfo = Menu(self.barraMenu, tearoff=0)
        self.menuInfo.add_command(label="creador", command=self.__creador)

        self.barraMenu.add_cascade(label="INFO", menu=self.menuInfo)

        # --------------entradas-------------------

        self.miFrame = Frame(self.root)
        self.miFrame.pack()
        self.nameProyect = StringVar()
        self.kmProyect = DoubleVar()
        self.idProyect = IntVar()

        self.cuadroName = Entry(self.miFrame, textvariable=self.nameProyect)
        self.cuadroName.grid(row=1, column=1, padx=10, pady=10, columnspan=3)
        self.cuadroName.config(justify="left", width=30)

        self.cuadroKm = Entry(self.miFrame, textvariable=self.kmProyect)
        self.cuadroKm.grid(row=2, column=1, padx=10, pady=10, columnspan=3)
        self.cuadroKm.config(justify="left", width=30)

        self.cuadroFecha = DateEntry(self.miFrame, bg="blue", fg="white")
        self.cuadroFecha.grid(row=3, column=1, padx=10, pady=10, columnspan=3)

        # option list menu
        self.mesesEleccion = StringVar(self.miFrame)
        self.mesesEleccion.set("Enero")
        self.meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                      "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        self.optionMes = OptionMenu(
            self.miFrame, self.mesesEleccion, *self.meses)
        self.optionMes.grid(row=4, column=1, padx=10, pady=10)

        # ---------------------------
        self.añosEleccion = StringVar(self.miFrame)
        self.añosEleccion.set(datetime.strftime(self.fecha, "%Y"))
        self.años = list(range(1990, 2051))
        self.optionMes = OptionMenu(
            self.miFrame, self.añosEleccion, *self.años)
        self.optionMes.grid(row=4, column=3, padx=10, pady=10)

        # scrolledtex
        self.miFrameScroll = Frame(self.root)
        self.miFrameScroll.pack()

        self.cuadroResultados = ScrolledText(
            self.miFrameScroll, width=39, height=15)
        self.cuadroResultados.grid(row=0, column=0, padx=10, pady=10)

        # labels---------------------

        self.nombreLabel = Label(self.miFrame, text="Proyecto")
        self.nombreLabel.grid(row=1, column=0, padx=10, pady=10)
        self.nombreLabel.config(justify="left")

        self.kmLabel = Label(self.miFrame, text="KM")
        self.kmLabel.grid(row=2, column=0, padx=10, pady=10)
        self.kmLabel.config(justify="left")

        self.fechaLabel = Label(self.miFrame, text="Fecha")
        self.fechaLabel.grid(row=3, column=0, padx=10, pady=10)
        self.fechaLabel.config(justify="left")

        self.consultaMesLabel = Label(self.miFrame, text="Mes")
        self.consultaMesLabel.grid(row=4, column=0, padx=10, pady=10)
        self.consultaMesLabel.config(justify="left")

        self.consultaAnoLabel = Label(self.miFrame, text="año")
        self.consultaAnoLabel.grid(row=4, column=2, padx=10, pady=10)
        self.consultaAnoLabel.config(justify="left")

        self.fechaActualLabel = Label(
            self.miFrame, text=datetime.strftime(self.fecha, "%d/%B/%Y"))
        self.fechaActualLabel.grid(
            row=0, column=0, columnspan=4, padx=10, pady=10)
        self.fechaActualLabel.config(justify="left")

        # --------------------botones--------------------

        self.miFrameBotones = Frame(self.root)
        self.miFrameBotones.pack()

        guardarBoton = Button(self.miFrameBotones,
                              text="Guardar", command=self.__guardar)
        guardarBoton.grid(row=0, column=0, padx=10, pady=10)

        leerBoton = Button(self.miFrameBotones,
                           text="Leer", command=self.__leer)
        leerBoton.grid(row=0, column=1, padx=10, pady=10)

        actualizarBoton = Button(
            self.miFrameBotones, text="Actualizar", command=self.__actualizar)
        actualizarBoton.grid(row=0, column=2, padx=10, pady=10)

        borrarBoton = Button(self.miFrameBotones,
                             text="Eliminar", command=self.__eliminar)
        borrarBoton.grid(row=0, column=3, padx=10, pady=10)
        borrarBoton.config(fg="red", cursor="pirate")

        ceBoton = Button(self.miFrameBotones, text="CE", command=self.__ce)
        ceBoton.grid(row=1, column=0, padx=10, pady=10)
        ceBoton.config(width=10)

        # buscar (id)

        idLabel = Label(self.miFrameBotones, text="ID")
        idLabel.grid(row=1, column=1, padx=0, pady=10)

        cuadroId = Entry(self.miFrameBotones, textvariable=self.idProyect)
        cuadroId.grid(row=1, column=2, padx=10, pady=10)
        cuadroId.config(width=10)

        verBoton = Button(self.miFrameBotones, text="ver", command=self.__ver)
        verBoton.grid(row=1, column=3, padx=5, pady=10)
        verBoton.config(width=5, cursor="star")

        self.root.mainloop()

    def __verificar_conexion(self):
        try:
            if os.path.exists(bd.getRuta):
                messagebox.showinfo("CONEXION", "conexion exitosa")
            else:
                con = sq.connect(bd.getRuta)
                cur = con.cursor()
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS PROYECTOS (
                        ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        NOMBRE VARCHAR(100) NOT NULL UNIQUE,
                        KILOMETROS FLOAT(3) NOT NULL,
                        FECHA DATE NOT NULL
                )


                """)
                con.commit()
                con.close()
                messagebox.showinfo("CONEXION", "conexion creada")

        except:
            messagebox.showerror(
                "Warning!", "error inesperado")

    def __salir(self):
        self.question = messagebox.askquestion("Salir", "¿Desea salir?")
        if self.question == "yes":
            self.root.destroy()
        else:
            pass

    def __creador(self):

        messagebox.showinfo(
            "DEV".center(40), "         Juli(OS)\njulioasmb@gmail.com")

    def __guardar(self):
        try:
            con = sq.connect(bd.getRuta)
            cur = con.cursor()
            cur.execute(
                f"INSERT INTO PROYECTOS(NOMBRE,KILOMETROS,FECHA) VALUES('{self.nameProyect.get().lower()}','{self.kmProyect.get()}','{self.cuadroFecha.get_date()}')")
            con.commit()
            con.close()
            messagebox.showinfo("BBDD", "Registro con exito")
        except:
            messagebox.showwarning(
                "Tener en cuenta", "No repetir 'nombre proyecto' ni dejar vacio 'KM'")

    def __ce(self):
        self.nameProyect.set("")
        self.kmProyect.set(0)
        self.cuadroResultados.delete(1.0, END)
        self.idProyect.set(0)

    def __leer(self):
        dicMeses = {
            "Enero": "01",
            "Febrero": "02",
            "Marzo": "03",
            "Abril": "04",
            "Mayo": "05",
            "Junio": "06",
            "Julio": "07",
            "Agosto": "08",
            "Septiembre": "09",
            "Octubre": "10",
            "Noviembre": "11",
            "Diciembre": "12"
        }
        con = sq.connect(bd.getRuta)
        cur = con.cursor()
        cur.execute(
            f"SELECT ID,NOMBRE,KILOMETROS,FECHA FROM PROYECTOS WHERE FECHA BETWEEN '{self.añosEleccion.get()}-{dicMeses[self.mesesEleccion.get()]}-01' and '{self.añosEleccion.get()}-{dicMeses[self.mesesEleccion.get()]}-31'")
        datos = cur.fetchall()
        con.close()

        con = sq.connect(bd.getRuta)
        cur = con.cursor()
        cur.execute(
            f"SELECT SUM(KILOMETROS) FROM PROYECTOS WHERE FECHA BETWEEN '{self.añosEleccion.get()}-{dicMeses[self.mesesEleccion.get()]}-01' and '{self.añosEleccion.get()}-{dicMeses[self.mesesEleccion.get()]}-31'")
        total = cur.fetchall()
        con.close()
        self.cuadroResultados.delete(1.0, END)
        if len(datos) == 0:
            messagebox.showinfo("BBDD", "no existen registros")
        else:
            for i in datos:
                self.cuadroResultados.insert(
                    END, f"id:{i[0]}\nnombre:{i[1]}\nKM:{i[2]}\nfecha:{i[3]}\n---------------------\n")
            self.cuadroResultados.insert(
                END, f"TOTAL: {(str(total))[2:-3]} KM")

    def __actualizar(self):

        con = sq.connect(bd.getRuta)
        cur = con.cursor()
        id = self.idProyect.get()

        cur.execute(
            f"UPDATE PROYECTOS SET NOMBRE='{self.nameProyect.get()}' WHERE ID = '{id}' ")
        con.commit()

        try:
            cur.execute(
                f"UPDATE PROYECTOS SET KILOMETROS='{self.kmProyect.get()}' WHERE ID = '{id}' ")
            con.commit()
            messagebox.showinfo("BBDD", f"Registro {id} actualizado")

            cur.execute(
                f"UPDATE PROYECTOS SET FECHA='{self.cuadroFecha.get_date()}' WHERE ID = '{id}' ")
            con.commit()
            con.close()
        except:
            messagebox.showerror("DATATYPE", "KM debe pertener a los reales")

    def __eliminar(self):
        con = sq.connect(bd.getRuta)
        cur = con.cursor()
        id = self.idProyect.get()
        self.question = messagebox.askquestion(
            "DELETE", f"¿Desea eliminar registro {id}?")
        if self.question == "yes":

            cur.execute(f"DELETE FROM PROYECTOS WHERE ID={id}")
            con.commit()
            con.close()
            messagebox.showinfo("BBDD", f"registro {id} eliminado")
        else:
            pass

    def __ver(self):
        try:
            con = sq.connect(bd.getRuta)
            cur = con.cursor()
            id = self.idProyect.get()

            cur.execute(
                f"SELECT NOMBRE, KILOMETROS, FECHA FROM PROYECTOS WHERE ID='{id}'")
            datos = cur.fetchall()
            fecha = datos[0][2]
            if fecha[5 == "0"]:
                fecha = f"{fecha[6:7]}/{fecha[8:10]}/{fecha[2:4]}"
            else:
                fecha = f"{fecha[5:7]}/{fecha[8:10]}/{fecha[2:4]}"

            con.close()

            self.nameProyect.set(datos[0][0])
            self.kmProyect.set(datos[0][1])
            self.cuadroFecha.set_date(fecha)
        except:
            messagebox.showerror("BBDD", f"Registro {id} no encontrado")


bd = bbdd()
guis = GUI()
