import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import time
import warnings

warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

HEADER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"}


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


def BusquedaInicial(search, option):
    pagina = None
    condicionNoExistente = False
    busquedaURL = 'https://listado.mercadolibre.com.ar/' + search.replace(' ', '-').lower() + '#D[A:' + search.lower() + ']'
    try:
        pagina = requests.get(url=busquedaURL, headers=HEADER, timeout=5)
    except requests.exceptions.ConnectionError or requests.exceptions.Timeout:
        print(' ')
        print('Excepción de timeout.')
    time.sleep(1)
    if pagina is not None:
        if pagina.status_code == 200:
            sopa = BeautifulSoup(pagina.content, 'html.parser', from_encoding="iso-8859-1")
            if option != '0':
                condition = 'Nuevo' if option == '1' else 'Usado'
                try:
                    pagina = requests.get(
                        str(sopa.find('a', {'aria-label': condition, 'class': 'ui-search-link'})['href']),
                        headers=HEADER, timeout=5)
                except TypeError:
                    condicionNoExistente = True
                    pagina = requests.get(url=busquedaURL, headers=HEADER, timeout=5)

                time.sleep(1)
                sopa = BeautifulSoup(pagina.content, 'html.parser', from_encoding="iso-8859-1")
            return [sopa, condicionNoExistente]
        else:
            return 0
    else:
        return 1



def CalcularCantidad(soup):
    try:
        cantidadPaginas = int(str(soup.find('li', class_='andes-pagination__page-count')
                                  .text.strip()).replace('de ', ''))
    except AttributeError:
        cantidadPaginas = 1

    cantidadArticulos = int(str(soup.find('span', class_='ui-search-search-result__quantity-results')
                                .text.strip()).replace(' resultados', '')
                            .replace('.', ''))

    print(' ')
    if cantidadArticulos < (49 * cantidadPaginas):
        return [cantidadArticulos, cantidadPaginas, True]
    else:
        cantidadArticulos = 49 * cantidadPaginas
        return [cantidadArticulos, cantidadPaginas, False]


def LimitadorCantidad(cantidadArticulos, limiteArticulos):
    if limiteArticulos == 0 or limiteArticulos == cantidadArticulos:
        return True
    elif 1 <= limiteArticulos < cantidadArticulos:
        return True
    else:
        return False


def SegundosAHHMMSS(segundo):
    hora = int(segundo / 3600)
    segundo -= hora * 3600
    minuto = int(segundo / 60)
    segundo -= minuto * 60
    stringHoras = str(hora) if hora >= 10 else str("0" + str(hora))
    stringMinutos = str(minuto) if minuto >= 10 else str("0" + str(minuto))
    stringSegundos = str(round(segundo, 2)) if segundo >= 10 else str("0" + str(round(segundo, 2)))
    return str(stringHoras + ':' + stringMinutos + ':' + stringSegundos)


# mineria.Scraping(self.soup, self.df, self.limitante, self.URL, self.primerSopa)
def Scraping(soup, dataFrame, limiteArticulos, URL, primerSoup):

    page = None

    df = dataFrame
    # limiteStatus400 = 0
    limiteTimeoutsArticulo = 0
    paginasVisitadas = 0
    timeoutException = False
    abortarEjecucion = False
    # primerSopa = True
    proximaURL = ''

    if not primerSoup:
        while limiteTimeoutsArticulo < 3:
            timeoutException = False
            try:
                page = requests.get(URL, headers=HEADER, timeout=5)
                soup = BeautifulSoup(page.content, 'html.parser', from_encoding="iso-8859-1")
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


    try:
        proximaURL = str(soup.find('a', class_='andes-pagination__link ui-search-link',
                            title='Siguiente')['href'])
    except TypeError:
        abortarEjecucion = True

    linksArticulos = [str(x['href'])
                      for x in soup.find_all('a', class_='ui-search-item__group__element ui-search-link')
                      if 'click1' not in str(x['href'])]

    if not timeoutException:
        paginasVisitadas += 1
        for articulo in linksArticulos:
            unidadMonetaria = ''
            especificaciones = []
            while True:
                while limiteTimeoutsArticulo < 3:
                    timeoutException = False
                    try:
                        page = requests.get(articulo, headers=HEADER, timeout=5)
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
                    soup = BeautifulSoup(page.content, 'html.parser')
                    especificaciones = soup.find_all('tr', class_='andes-table__row')
                    if len(especificaciones) > 0:
                        break
                else:
                    break

            if not timeoutException:
                try:
                    precio = int(
                        str(soup.find('span', class_='andes-money-amount__fraction').text.strip()).replace(
                            '.',
                            ''))
                    unidadMonetaria = str(soup.find('span', class_='andes-money-amount__currency-symbol')
                                          .text.strip())
                except TypeError:
                    precio = 0

                if precio != 0:
                    soup = None
                    page = None
                    cabeceras = CambioCaracteresRaros('th', especificaciones)
                    datos = CambioCaracteresRaros('td', especificaciones)

                    if len(df) == 0:
                        cabeceras.append('Unidad Monetaria')
                        cabeceras.append('Precio')
                        cabeceras.append('Link')
                        datos.append('ARS' if unidadMonetaria == '$' else 'U$S')
                        datos.append(str(precio))
                        datos.append(articulo)
                        df = pd.DataFrame(columns=cabeceras)
                        df.loc[df.shape[0]] = datos
                    else:
                        if set(cabeceras).issubset(df.columns):
                            if len(cabeceras) == len(df.columns):
                                indicesCabeceras = [cabeceras.index(column) for column in df.columns]
                                datosOrdenados = [datos[i] for i in indicesCabeceras]
                                df.loc[df.shape[0]] = datosOrdenados
                            elif len(cabeceras) < len(df.columns):
                                AsignacionDatosOrdenados(cabeceras, datos, df)
                        else:
                            for cabecera in cabeceras:
                                if cabecera not in df.columns:
                                    df[cabecera] = np.nan
                            AsignacionDatosOrdenados(cabeceras, datos, df)

                        df.loc[df.shape[0] - 1, 'Unidad Monetaria'] = 'ARS' if unidadMonetaria == '$' else 'U$S'
                        df.loc[df.shape[0] - 1, 'Precio'] = precio
                        df.loc[df.shape[0] - 1, 'Link'] = articulo
            print(len(df))
            if limiteArticulos > 0 and limiteArticulos == len(df):
                abortarEjecucion = True
                break
    else:
        #timeout acá
        pass

    return [df,paginasVisitadas,abortarEjecucion, proximaURL]

