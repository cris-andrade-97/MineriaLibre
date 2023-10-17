import time

import numpy as np
import pandas as pd
import requests
from PyQt5.QtCore import QThread, pyqtSignal
from bs4 import BeautifulSoup

def CambioCaracteresRaros(tag, specs):
    return [str(fila.find(tag).text.strip())
            .replace('├í', 'á')
            .replace('ĂĄ', 'á')
            .replace('ÃĄ', 'á')
            .replace('├Ī', 'á')
            .replace('รก', 'á')
            .replace('Ć”', 'á')
            .replace('√°', 'á')
            .replace('├®', 'é')
            .replace('ĂŠ', 'é')
            .replace('Ć©', 'é')
            .replace('รฉ', 'é')
            .replace('ûˋ', 'é')
            .replace('√©', 'é')
            .replace('ÃĐ', 'é')
            .replace('├¡', 'í')
            .replace('Ć­', 'í')
            .replace('รญ', 'í')
            .replace('ûÙ', 'í')
            .replace('├Ł', 'í')
            .replace('√≠', 'í')
            .replace('Ã­', 'í')
            .replace('Ă­', 'í')
            .replace('├│', 'ó')
            .replace('Ăł', 'ó')
            .replace('รณ', 'ó')
            .replace('Ć³', 'ó')
            .replace('û°', 'ó')
            .replace('√≥', 'ó')
            .replace('Ãģ', 'ó')
            .replace('Ćŗ', 'ú')
            .replace('Ãš', 'ú')
            .replace('รบ', 'ú')
            .replace('├║', 'ú')
            .replace('├ü', 'Á')
            .replace('Ć', 'Á')
            .replace('û', 'Á')
            .replace('Ă', 'Á')
            .replace('√Å', 'Á')
            .replace('ร', 'Á')
            .replace('┬░', '°')
            .replace('ô¯', '°')
            .replace('ยฐ', '°')
            .replace('Â°', '°')
            .replace('Ā°', '°')
            .replace('¬∞', '°')
            .replace('├▒', 'ñ')
            .replace('Ă±', 'ñ')
            .replace('Ć±', 'ñ')
            .replace('√±', 'ñ')
            .replace('Ãą', 'ñ')
            .replace('รฑ', 'ñ')
            .replace('ûÝ', 'ñ')
            .replace('Ăą', 'ñ')
            .replace('┬▓', '²')
            .replace('ยฒ', '²')
            for fila in specs]

def AsignacionDatosOrdenados(listaCabeceras, listaDatos, dataFrame):
    listaIndices = []
    listaOrdenada = []
    for column in dataFrame.columns:
        try:
            listaIndices.append(listaCabeceras.index(column))
        except ValueError:
            listaIndices.append(-1)

    for index in listaIndices:
        if index != -1:
            listaOrdenada.append(listaDatos[index])
        else:
            listaOrdenada.append(np.nan)

    dataFrame.loc[dataFrame.shape[0]] = listaOrdenada


class HiloDeTrabajo(QThread):
    finished = pyqtSignal(list)
    progreso = pyqtSignal(int)
    def __init__(self, soup, limitador):
        super().__init__()
        self.soup = soup
        self.dataFrame = pd.DataFrame()
        self.limitador = limitador
        self.URL = ''
        self.paginasVisitadas = 0
        self.HEADER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"}

    def Scrap(self, primerSoup):
        page = None
        # limiteStatus400 = 0
        limiteTimeoutsArticulo = 0
        timeoutException = False
        abortarEjecucion = False
        # primerSopa = True

        if not primerSoup:
            while limiteTimeoutsArticulo < 3:
                timeoutException = False
                try:
                    page = requests.get(self.URL, headers=self.HEADER, timeout=5)
                    self.soup = BeautifulSoup(page.content, 'html.parser', from_encoding="iso-8859-1")
                    limiteTimeoutsArticulo = 0
                    # limiteTimeoutsGeneral = 0
                    break
                except requests.exceptions.ConnectionError or requests.exceptions.Timeout:
                    timeoutException = True
                    limiteTimeoutsArticulo += 1
                    print(' ')
                    print('No fue posible realizar la solicitud del artículo.')
                    print('Intento ' + str(limiteTimeoutsArticulo) + ' de 3')
                time.sleep(1)

        if not timeoutException:
            try:
                self.URL = str(self.soup.find('a', class_='andes-pagination__link ui-search-link',
                                              title='Siguiente')['href'])
            except TypeError:
                abortarEjecucion = True

            linksArticulos = [str(x['href'])
                              for x in self.soup.find_all('a', class_='ui-search-item__group__element ui-search-link')
                              if 'click1' not in str(x['href'])]
            self.paginasVisitadas += 1

            for articulo in linksArticulos:
                unidadMonetaria = ''
                especificaciones = []
                while True:
                    while limiteTimeoutsArticulo < 3:
                        timeoutException = False
                        try:
                            page = requests.get(articulo, headers=self.HEADER, timeout=5)
                            limiteTimeoutsArticulo = 0
                            # limiteTimeoutsGeneral = 0
                            break
                        except requests.exceptions.ConnectionError or requests.exceptions.Timeout:
                            timeoutException = True
                            limiteTimeoutsArticulo += 1
                            print(' ')
                            print('No fue posible realizar la solicitud del artículo.')
                            print('Intento ' + str(limiteTimeoutsArticulo) + ' de 3')
                        time.sleep(1)

                    if not timeoutException:
                        self.soup = BeautifulSoup(page.content, 'html.parser')
                        especificaciones = self.soup.find_all('tr', class_='andes-table__row')
                        if len(especificaciones) > 0:
                            break
                    else:
                        break

                if not timeoutException:
                    try:
                        precio = int(
                            str(self.soup.find('span', class_='andes-money-amount__fraction').text.strip()).replace(
                                '.',
                                ''))
                        unidadMonetaria = str(self.soup.find('span', class_='andes-money-amount__currency-symbol')
                                              .text.strip())
                    except TypeError:
                        precio = 0

                    if precio != 0:
                        self.soup = None
                        page = None
                        cabeceras = CambioCaracteresRaros('th', especificaciones)
                        datos = CambioCaracteresRaros('td', especificaciones)

                        if len(self.dataFrame) == 0:
                            cabeceras.append('Unidad Monetaria')
                            cabeceras.append('Precio')
                            cabeceras.append('Link')
                            datos.append('ARS' if unidadMonetaria == '$' else 'U$S')
                            datos.append(str(precio))
                            datos.append(articulo)
                            self.dataFrame = pd.DataFrame(columns=cabeceras)
                            self.dataFrame.loc[self.dataFrame.shape[0]] = datos
                        else:
                            if set(cabeceras).issubset(self.dataFrame.columns):
                                if len(cabeceras) == len(self.dataFrame.columns):
                                    indicesCabeceras = [cabeceras.index(column) for column in self.dataFrame.columns]
                                    datosOrdenados = [datos[i] for i in indicesCabeceras]
                                    self.dataFrame.loc[self.dataFrame.shape[0]] = datosOrdenados
                                elif len(cabeceras) < len(self.dataFrame.columns):
                                    AsignacionDatosOrdenados(cabeceras, datos, self.dataFrame)
                            else:
                                for cabecera in cabeceras:
                                    if cabecera not in self.dataFrame.columns:
                                        self.dataFrame[cabecera] = np.nan
                                AsignacionDatosOrdenados(cabeceras, datos, self.dataFrame)

                            self.dataFrame.loc[self.dataFrame.shape[0] - 1, 'Unidad Monetaria'] = 'ARS' if unidadMonetaria == '$' else 'U$S'
                            self.dataFrame.loc[self.dataFrame.shape[0] - 1, 'Precio'] = precio
                            self.dataFrame.loc[self.dataFrame.shape[0] - 1, 'Link'] = articulo
                self.progreso.emit(len(self.dataFrame))
                if self.limitador > 0 and self.limitador == len(self.dataFrame):
                    abortarEjecucion = True
                    break
        else:
            # timeout
            print('Excepción de Timeout: Revise su conexión a internet.')
            abortarEjecucion = True
            pass
        return abortarEjecucion

    def run(self):
        # [df,paginasVisitadas,abortarEjecucion, proximaURL]
        abortar = self.Scrap(True)
        while not abortar:
            self.soup = None
            abortar = self.Scrap(False)
        result = [self.dataFrame,self.paginasVisitadas]

        self.finished.emit(result)