import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import time

HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0"}

busqueda = input('Ingrese su búsqueda: ')

# opcionCondicion = input('Ingrese una opción de condición de artículo: 0, 1 o 2: ')
'''
0: Nuevos y Usados
1: Sólo Nuevos
2: Sólo Usados
'''
nombreArchivoCSV = busqueda + '.csv'
nombreArchivoXLSX = busqueda + '.xlsx'

ultimaPagina = False
primerRegistro = True
hayPrecio = True
timeoutException = False
abortarEjecucion = False
calculandoTiempoEstimado = True

df = pd.DataFrame()

URL = 'https://listado.mercadolibre.com.ar/' + busqueda.replace(' ', '-').lower() + '#D[A:' + busqueda.lower() + ']'

'''
page = requests.get(url=URL, headers=HEADER)

BeautifulSoup(page.content, 'html.parser')

def condicionArticuloURL(opcion):
    if opcion == 0:
        return
'''

paginasVisitadas = 0
articulosRecabados = 0
tiempoEstimado = 0
limiteTimeoutsArticulo = 0
limiteTimeoutsGeneral = 0
limiteStatus400 = 0

page = None

tiempo_inicio = time.time()


def CambioCaracteresRaros(tag, specs):
    lista = []
    for fila in specs:
        lista.append(str(fila.find(tag).text.strip())
                     .replace('├í', 'á')
                     .replace('ĂĄ', 'á')
                     .replace('├Ī', 'á')
                     .replace('รก', 'á')
                     .replace('Ć”', 'á')
                     .replace('├®', 'é')
                     .replace('Ć©', 'é')
                     .replace('รฉ', 'é')
                     .replace('ûˋ', 'é')
                     .replace('├¡', 'í')
                     .replace('Ć­', 'í')
                     .replace('รญ', 'í')
                     .replace('ûÙ', 'í')
                     .replace('├│', 'ó')
                     .replace('Ăł', 'ó')
                     .replace('รณ', 'ó')
                     .replace('Ć³', 'ó')
                     .replace('û°', 'ó')
                     .replace('Ćŗ', 'ú')
                     .replace('├ü', 'Á')
                     .replace('Ć', 'Á')
                     .replace('û', 'Á')
                     .replace('┬░', '°')
                     .replace('ô¯', '°')
                     .replace('├▒', 'ñ')
                     .replace('Ă±', 'ñ')
                     .replace('Ć±', 'ñ')
                     .replace('รฑ', 'ñ')
                     .replace('ûÝ', 'ñ'))

    return lista


def AsignacionDatosOrdenados():
    for column in df.columns:
        try:
            indicesCabeceras.append(cabeceras.index(column))
        except:
            indicesCabeceras.append(-1)

    for index in indicesCabeceras:
        if index != -1:
            datosOrdenados.append(datos[index])
        else:
            datosOrdenados.append(np.nan)

    df.loc[df.shape[0]] = datosOrdenados


def SegundosAHHMMSS(segundo):
    hora = int(segundo / 3600)
    segundo -= hora * 3600
    minuto = int(segundo / 60)
    segundo -= minuto * 60
    stringHoras = str(hora) if hora >= 10 else str("0" + str(hora))
    stringMinutos = str(minuto) if minuto >= 10 else str("0" + str(minuto))
    stringSegundos = str(round(segundo, 2)) if segundo >= 10 else str("0" + str(round(segundo, 2)))
    return str(stringHoras + ':' + stringMinutos + ':' + stringSegundos)


while True:
    if ultimaPagina or abortarEjecucion:
        break

    try:
        page = requests.get(url=URL, headers=HEADER, timeout=5)
        limiteTimeoutsGeneral = 0
    except:
        print(' ')
        print('Excepción de timeout.')
        limiteTimeoutsGeneral += 1
        print('Intento ' + str(limiteTimeoutsGeneral) + ' de 5')
    time.sleep(1)
    if page is not None:
        if page.status_code == 200:
            limiteTimeoutsArticulo = 0
            paginasVisitadas += 1

            soup = BeautifulSoup(page.content, 'html.parser', from_encoding="iso-8859-1")

            if calculandoTiempoEstimado:
                calculandoTiempoEstimado = False
                try:
                    cantidadPaginas = int(str(soup.find('li', class_='andes-pagination__page-count')
                                              .text.strip()).replace('de ', ''))
                except:
                    cantidadPaginas = 1
                tiempoEstimado = (cantidadPaginas + cantidadPaginas * 48) * 2
                print('-----------------------------------------------')
                print('Tiempo estimado calculado:', SegundosAHHMMSS(int(tiempoEstimado)))
                print('-----------------------------------------------')

            try:
                URL = str(soup.find('a', class_='andes-pagination__link shops__pagination-link ui-search-link',
                                    title='Siguiente')['href'])
            except:
                ultimaPagina = True

            linksArticulos = [str(x['href'])
                              for x in soup.find_all('a', class_='ui-search-item__group__element '
                                                                 'shops__items-group-details ui-search-link')
                              if 'click1' not in str(x['href'])]

            for articulo in linksArticulos:
                hayPrecio = True
                precio = 0
                especificaciones = []

                while True:
                    while limiteTimeoutsArticulo < 5:
                        timeoutException = False
                        try:
                            page = requests.get(articulo, headers=HEADER, timeout=5)
                            limiteTimeoutsArticulo = 0
                            limiteTimeoutsGeneral = 0
                            break
                        except:
                            timeoutException = True
                            limiteTimeoutsArticulo += 1
                            print(' ')
                            print('No fue posible realizar la solicitud del artículo.')
                            print('Intento ' + str(limiteTimeoutsArticulo) + ' de 5')
                        time.sleep(1)

                    if not timeoutException:
                        soup = BeautifulSoup(page.content, 'html.parser')
                        try:
                            precio = int(
                                str(soup.find('span', class_='andes-money-amount__fraction').text.strip()).replace('.',
                                                                                                                   ''))
                        except:
                            hayPrecio = False
                            break

                        especificaciones = soup.find_all('tr', class_='andes-table__row')

                        if len(especificaciones) > 0:
                            break
                    else:
                        break

                if not timeoutException:
                    if hayPrecio:
                        articulosRecabados += 1

                        cabeceras = CambioCaracteresRaros('th', especificaciones)
                        datos = CambioCaracteresRaros('td', especificaciones)

                        datosOrdenados = []
                        unidadMonetaria = str(soup.find('span', class_='andes-money-amount__currency-symbol')
                                              .text.strip())
                        if primerRegistro:
                            primerRegistro = False
                            cabeceras.append('Unidad Monetaria')
                            cabeceras.append('Precio')
                            cabeceras.append('Link')
                            datos.append('ARS' if unidadMonetaria == '$' else 'U$S')
                            datos.append(precio)
                            datos.append(articulo)
                            df = pd.DataFrame(columns=cabeceras)
                            df.loc[df.shape[0]] = datos
                            print(len(df))
                        else:
                            if set(cabeceras).issubset(df.columns):
                                if len(cabeceras) == len(df.columns):
                                    indicesCabeceras = [cabeceras.index(column) for column in df.columns]
                                    datosOrdenados = [datos[i] for i in indicesCabeceras]
                                    df.loc[df.shape[0]] = datosOrdenados
                                elif len(cabeceras) < len(df.columns):
                                    indicesCabeceras = []
                                    AsignacionDatosOrdenados()
                            else:
                                indicesCabeceras = []
                                for cabecera in cabeceras:
                                    if cabecera not in df.columns:
                                        df[cabecera] = np.nan
                                AsignacionDatosOrdenados()

                            df.loc[df.shape[0] - 1, 'Unidad Monetaria'] = 'ARS' if unidadMonetaria == '$' else 'U$S'
                            df.loc[df.shape[0] - 1, 'Precio'] = precio
                            df.loc[df.shape[0] - 1, 'Link'] = articulo
                            print(len(df))
                    else:
                        print(' ')
                        print('Artículo sin precio. Pasando al siguiente...')
                else:
                    limiteTimeoutsGeneral += 1
                    print(' ')
                    if limiteTimeoutsGeneral == 5:
                        print('Límite de timeouts consecutivos alcanzado para el artículo.')
                        print('Cinco artículos consecutivos han tenido excepciones de timeout.')
                        print('Abortando ejecución...')
                        abortarEjecucion = True
                        break
                    else:
                        limiteTimeoutsArticulo = 0
                        print('Límite de timeouts consecutivos alcanzado para el artículo. Pasando al siguiente...')
        else:
            limiteStatus400 += 1
            print(' ')
            print('No fue posible realizar la solicitud.')
            print('Status: ' + str(page.status_code))
            if limiteStatus400 == 5:
                print('Quinto intento realizado.')
                print('Abortando ejecución...')
                abortarEjecucion = True
                break
            else:
                print('Intento ' + str(limiteStatus400) + ' de 5')
    elif limiteTimeoutsGeneral == 5:
        print(' ')
        print('Límite de timeouts consecutivos alcanzado.')
        try:
            print('Status: ' + str(page.status_code))
        except:
            print('Sin conexión.')
        print('Abortando ejecución...')
        break

df['Precio'] = df['Precio'].astype(int)

try:
    df.to_csv(str(nombreArchivoCSV), index=False, encoding='iso-8859-1')
    print('Encoding Latin-1')
except:
    df.to_csv(str(nombreArchivoCSV), index=False, encoding='utf-8')
    print('Encoding UTF-8')
finally:
    df.to_excel(str(nombreArchivoXLSX), index=False)

segundos = time.time() - tiempo_inicio

print(' ')
print('Páginas visitadas:', paginasVisitadas)
print('Artículos recabados:', articulosRecabados)
print('Tiempo transcurrido:', SegundosAHHMMSS(segundos))
