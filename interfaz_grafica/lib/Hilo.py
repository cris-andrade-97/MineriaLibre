import pandas as pd
from PyQt5.QtCore import QThread, pyqtSignal
from lib import mineria
# from interfaz_grafica.lib import mineria

class HiloDeTrabajo(QThread):
    finished = pyqtSignal(list)

    def __init__(self, soup, limitador, opcion):
        super().__init__()
        self.soup = soup
        self.dataFrame = pd.DataFrame()
        self.limitador = limitador
        self.opcion = opcion
        self.URL = ''
        self.paginasDeArticulos = 0


    def run(self):
        result = mineria.Scraping(self.soup, self.dataFrame, self.limitador, self.URL, True)
        self.dataFrame = result[0]
        self.paginasDeArticulos += result[1]
        self.URL = result[3]

        while not result[2]:
            self.soup = None
            result = mineria.Scraping(self.soup, self.dataFrame, self.limitador, self.URL, False)

        self.finished.emit(result)
