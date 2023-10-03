import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import time
import warnings

warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

HEADER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"}

ultimaPagina = False
primerRegistro = True
hayPrecio = True
timeoutException = False
abortarEjecucion = False
calculandoTiempoEstimado = True

opcion = ''

cantidadPaginas = 0
cantidadArticulosAprox = 0
limiteArticulos = 0
paginasVisitadas = 0
articulosRecabados = 0
tiempoEstimado = 0
limiteTimeoutsArticulo = 0
limiteTimeoutsGeneral = 0
limiteStatus400 = 0
tiempo_inicio = 0
tiempoTotal = 0

df = pd.DataFrame()
linksArticulos = []

page = None

busqueda = input('Ingrese su búsqueda: ')

while True:
    print('')
    print('0: Nuevos y Usados')
    print('1: Sólo Nuevos')
    print('2: Sólo Usados')
    print('')
    opcion = input('Ingrese una opción de condición de artículos: 0, 1 o 2: ')
    if opcion == '0' or opcion == '1' or opcion == '2':
        break
    else:
        print('')
        print('Su opción no está contemplada. Intente nuevamente.')

URL = 'https://listado.mercadolibre.com.ar/' + busqueda.replace(' ', '-').lower() + '#D[A:' + busqueda.lower() + ']'


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
        except:
            listaIndices.append(-1)

    for index in listaIndices:
        if index != -1:
            listaOrdenada.append(listaDatos[index])
        else:
            listaOrdenada.append(np.nan)

    dataFrame.loc[dataFrame.shape[0]] = listaOrdenada


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
            limiteStatus400 = 0
            limiteTimeoutsArticulo = 0
            paginasVisitadas += 1

            soup = BeautifulSoup(page.content, 'html.parser', from_encoding="iso-8859-1")

            if primerRegistro:
                if opcion != '0':
                    condicion = 'Nuevo' if opcion == '1' else 'Usado'
                    try:
                        page = requests.get(
                            str(soup.find('a', {'aria-label': condicion, 'class': 'ui-search-link'})['href']),
                            headers=HEADER, timeout=5)
                        soup = BeautifulSoup(page.content, 'html.parser', from_encoding="iso-8859-1")
                        time.sleep(1)
                    except:
                        print('No hay artículos con esa condición en su búsqueda, '
                              'volviendo a la opción "0" por default...')
                        opcion = '0'
                condicion = None
                try:
                    cantidadPaginas = int(str(soup.find('li', class_='andes-pagination__page-count')
                                              .text.strip()).replace('de ', ''))
                except:
                    cantidadPaginas = 1

                cantidadArticulos = int(str(soup.find('span', class_='ui-search-search-result__quantity-results')
                                            .text.strip()).replace(' resultados', '')
                                        .replace('.', ''))

                print(' ')
                if cantidadArticulos < (49 * cantidadPaginas):
                    print('Hay exactamente', str(cantidadArticulos), 'artículos.')
                else:
                    cantidadArticulos = 49 * cantidadPaginas
                    print('Hay aproximadamente', str(cantidadArticulos), 'artículos.')

                print('Puede traerlos todos o parte de ellos.')

                while True:
                    print(' ')
                    print('Ingrese 0 si desea todos los artículos ó ingrese una cantidad entre 1 y',
                          str(cantidadArticulos), ':')
                    try:
                        limiteArticulos = int(input())
                        if limiteArticulos == 0 or limiteArticulos == cantidadArticulos:
                            tiempoEstimado = (cantidadPaginas + cantidadArticulos) * 2.05
                            break
                        elif 1 <= limiteArticulos < cantidadArticulos:
                            tiempoEstimado = (int(limiteArticulos / 49) + limiteArticulos) * 2.05
                            break
                        else:
                            print('Opción fuera de rango. Intente nuevamente.')
                    except:
                        print('Sólo se admiten números. Intente nuevamente.')

                tiempo_inicio = time.time()
                print(' ')
                print('-----------------------------------------------')
                print('Tiempo estimado calculado:', SegundosAHHMMSS(int(tiempoEstimado)))
                print('-----------------------------------------------')
                print(' ')

            try:
                URL = str(soup.find('a', class_='andes-pagination__link shops__pagination-link ui-search-link',
                                    title='Siguiente')['href'])
            except:
                ultimaPagina = True

            linksArticulos = [str(x['href'])
                              for x in soup.find_all('a', class_='ui-search-item__group__element ui-search-link')
                              if 'click1' not in str(x['href'])]

            if limiteArticulos != 0 and limiteArticulos < len(linksArticulos) and cantidadPaginas == 1:
                linksArticulos = linksArticulos[0:limiteArticulos]

            for articulo in linksArticulos:
                unidadMonetaria = ''
                precio = 0
                especificaciones = []
                while True:
                    while limiteTimeoutsArticulo < 3:
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
                    except:
                        precio = 0

                    if precio != 0:
                        soup = None
                        page = None
                        articulosRecabados += 1
                        cabeceras = CambioCaracteresRaros('th', especificaciones)
                        datos = CambioCaracteresRaros('td', especificaciones)
                        especificaciones = []

                        if primerRegistro:
                            primerRegistro = False
                            cabeceras.append('Unidad Monetaria')
                            cabeceras.append('Precio')
                            cabeceras.append('Link')
                            datos.append('ARS' if unidadMonetaria == '$' else 'U$S')
                            datos.append(str(precio))
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
                                    indicesCabeceras = []
                                    datosOrdenados = []
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

                        datos = []
                        cabeceras = []
                    else:
                        print(' ')
                        print('Artículo sin precio. Pasando al siguiente...')
                else:
                    limiteTimeoutsGeneral += 1
                    print(' ')
                    if limiteTimeoutsGeneral == 3:
                        print('Límite de timeouts consecutivos alcanzado para el artículo.')
                        print('Tres artículos consecutivos han tenido excepciones de timeout.')
                        print('Abortando ejecución...')
                        abortarEjecucion = True
                        break
                    else:
                        limiteTimeoutsArticulo = 0
                        print('Límite de timeouts consecutivos alcanzado para el artículo. Pasando al siguiente...')

                if limiteArticulos > 0 and limiteArticulos == len(df):
                    abortarEjecucion = True
                    break
        else:
            limiteStatus400 += 1
            print(' ')
            print('No fue posible realizar la solicitud.')
            print('Status: ' + str(page.status_code))
            if limiteStatus400 == 3:
                print('Tercer intento consecutivo realizado.')
                print('Abortando ejecución...')
                abortarEjecucion = True
                break
            else:
                print('Intento ' + str(limiteStatus400) + ' de 3')
    elif limiteTimeoutsGeneral == 3:
        print(' ')
        print('Límite de timeouts consecutivos alcanzado.')
        print('Tercer intento realizado.')
        try:
            print('Status: ' + str(page.status_code))
        except:
            print('Sin conexión.')
        print('Abortando ejecución...')
        break

print(' ')
if len(df) > 0:
    nombreArchivo = ''
    df = df.sample(frac=1, random_state=np.random.randint(low=0, high=101)).reset_index(drop=True)
    df['Precio'] = df['Precio'].astype(int)
    if opcion == '0':
        nombreArchivo = busqueda + ' - Nuevos y Usados'
    elif opcion == '1':
        nombreArchivo = busqueda + ' - Sólo Nuevos'
    elif opcion == '2':
        nombreArchivo = busqueda + ' - Sólo Usados'
    df.to_excel(str(nombreArchivo + '.xlsx'), index=False)
    print('Planilla de cálculos creada correctamente.')
else:
    print('Planilla de cálculos no fue creada. Cantidad nula de registros.')

tiempoTotal = time.time() - tiempo_inicio

print(' ')
print('Páginas visitadas:', paginasVisitadas)
print('Artículos recabados:', articulosRecabados)
print('Tiempo transcurrido:', SegundosAHHMMSS(tiempoTotal))
