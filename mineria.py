import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import time

HEADER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"}

busqueda = input('Ingrese su búsqueda: ')

# opcionCondicion = input('Ingrese una opción de condición de artículo: 0, 1 o 2: ')
'''
0: Nuevos y Usados
1: Sólo Nuevos
2: Sólo Usados
'''
nombreArchivo = busqueda + '.csv'

ultimaPagina = False
primerRegistro = True
hayPrecio = True
primerVuelta = True
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
limiteTimeouts = 0
limite404 = 0

page = None

tiempo_inicio = time.time()


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
    timeoutException = False
    if ultimaPagina:
        break

    if abortarEjecucion:
        break

    try:
        page = requests.get(url=URL, headers=HEADER, timeout=5)
        time.sleep(1)
    except:
        print(' ')
        print('Excepción de timeout.')
        limiteTimeouts += 1

    if page is not None:
        if page.status_code == 200:
            limiteTimeouts = 0
            primerVuelta = False
            paginasVisitadas += 1
            soup = BeautifulSoup(page.content, 'html.parser')
            if calculandoTiempoEstimado:
                calculandoTiempoEstimado = False
                cantidadPaginas = int(str(soup.find('li', class_='andes-pagination__page-count')
                                          .text.strip()).replace('de ', ''))
                tiempoEstimado = (cantidadPaginas + cantidadPaginas * 48) * 2.08656
                print('')
                print('Tiempo estimado calculado:', SegundosAHHMMSS(int(tiempoEstimado)))
                print('')

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
                    while limiteTimeouts < 5:
                        timeoutException = False
                        try:
                            page = requests.get(articulo, headers=HEADER, timeout=5)
                            time.sleep(1)
                            limiteTimeouts = 0
                            break
                        except:
                            timeoutException = True
                            limiteTimeouts += 1
                            print(' ')
                            print('No fue posible realizar la solicitud del artículo.')
                            print('Intento ' + str(limiteTimeouts) + ' de 5')

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

                if hayPrecio and not timeoutException:
                    articulosRecabados += 1
                    cabeceras = [cabecera.find('th').text.strip() for cabecera in especificaciones]

                    datos = [dato.find('td').text.strip() for dato in especificaciones]

                    datosOrdenados = []
                    unidadMonetaria = str(soup.find('span', class_='andes-money-amount__currency-symbol').text.strip())
                    if primerRegistro:
                        primerRegistro = False
                        cabeceras.append('Unidad Monetaria')
                        cabeceras.append('Precio')
                        cabeceras.append('Link')
                        datos.append('ARS' if unidadMonetaria == '$' else 'U$S')
                        datos.append(precio)
                        datos.append(articulo)
                        df = pd.DataFrame(columns=cabeceras)
                        df['Precio'] = df['Precio'].astype(int)
                        df.loc[df.shape[0]] = datos
                    else:
                        if set(cabeceras).issubset(df.columns):
                            if len(cabeceras) == len(df.columns):
                                indicesCabeceras = [cabeceras.index(column) for column in df.columns]
                                datosOrdenados = [datos[i] for i in indicesCabeceras]
                                df.loc[df.shape[0]] = datosOrdenados
                            elif len(cabeceras) < len(df.columns):
                                indicesCabeceras = []
                                for column in df.columns:
                                    try:
                                        indicesCabeceras.append(cabeceras.index(column))
                                    except:
                                        indicesCabeceras.append(-1)

                                for indices in indicesCabeceras:
                                    if indices != -1:
                                        datosOrdenados.append(datos[indices])
                                    else:
                                        datosOrdenados.append(np.nan)

                                df.loc[df.shape[0]] = datosOrdenados
                        else:
                            indicesCabeceras = []
                            for cabecera in cabeceras:
                                if cabecera not in df.columns:
                                    df[cabecera] = np.nan

                            for column in df.columns:
                                try:
                                    indicesCabeceras.append(cabeceras.index(column))
                                except:
                                    indicesCabeceras.append(-1)

                            for indices in indicesCabeceras:
                                if indices != -1:
                                    datosOrdenados.append(datos[indices])
                                else:
                                    datosOrdenados.append(np.nan)

                            df.loc[df.shape[0]] = datosOrdenados

                        df.loc[df.shape[0] - 1, 'Unidad Monetaria'] = 'ARS' if unidadMonetaria == '$' else 'U$S'
                        df.loc[df.shape[0] - 1, 'Precio'] = precio
                        df.loc[df.shape[0] - 1, 'Link'] = articulo
                else:
                    abortarEjecucion = True
                    print('Límite de timeouts alcanzado.')
                    print('Abortando ejecución...')
                    break

                print(len(df))
                df.to_csv(str(nombreArchivo), index=False, encoding='utf-16')
        elif page.status_code >= 400:
            limite404 += 1
            print(' ')
            print('No fue posible realizar la solicitud.')
            print('Status: ' + str(page.status_code))
            print('Intento ' + str(limite404) + ' de 5')
            if limite404 == 5:
                print(' ')
                print('Quinto intento realizado.')
                print('Status: ' + str(page.status_code))
                print('Abortando ejecución...')
                abortarEjecucion = True
                break
    else:
        if limiteTimeouts == 5:
            print(' ')
            print('Límite de timeouts alcanzado.')
            try:
                print('Status: ' + str(page.status_code))
            except:
                print('Sin conexión.')
            print('Abortando ejecución...')
            break


segundos = time.time() - tiempo_inicio

print(' ')
print('Páginas visitadas:', paginasVisitadas)
print('Artículos recabados:', articulosRecabados)
print('Tiempo transcurrido:', SegundosAHHMMSS(segundos))
