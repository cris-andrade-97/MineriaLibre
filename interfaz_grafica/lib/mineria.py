import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import warnings

warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

HEADER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"}

primerVuelta = True

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


