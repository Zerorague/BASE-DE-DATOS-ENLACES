import pathlib
import sqlite3 as sq
from pathlib import Path
import os


class bbdd():

    def __init__(self) -> None:
        self.__ruta = (Path.home())
        self.__r = self.__ruta.__str__()
        self.__ruta = self.__r+"\BBDD"

        try:
            con = sq.connect(self.__ruta)
            cur = con.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS PROYECTOS (
                    ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    NOMBRE VARCHAR(100) NOT NULL UNIQUE,
                    KILOMETROS FLOAT(3) NOT NULL,
                    FECHA DATE(20) NOT NULL
            )
        
            
            """)
            con.close()

        except:
            pass

    @property
    def getRuta(self):
        return self.__ruta


hola = bbdd()
