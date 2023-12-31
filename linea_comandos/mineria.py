import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import time
import warnings
import os
import openpyxl

warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

HEADER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"}

ultimaPagina = False
primerRegistro = True
timeoutException = False
abortarEjecucion = False

opcion = ''
busqueda = ''
page = None
URL = ''

cantidadPaginas = 0
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


def SegundosAHHMMSS(segundo):
    hora = int(segundo / 3600)
    segundo -= hora * 3600
    minuto = int(segundo / 60)
    segundo -= minuto * 60
    stringHoras = str(hora) if hora >= 10 else str("0" + str(hora))
    stringMinutos = str(minuto) if minuto >= 10 else str("0" + str(minuto))
    stringSegundos = str(round(segundo, 2)) if segundo >= 10 else str("0" + str(round(segundo, 2)))
    return str(stringHoras + ':' + stringMinutos + ':' + stringSegundos)

try:
    while limiteTimeoutsGeneral < 3:
        while busqueda == '':
            print(' ')
            busqueda = input('Ingrese su búsqueda: ')
            if busqueda == '':
                print(' ')
                print('La búsqueda no puede ser nula. Intente nuevamente.')
        try:
            URL = 'https://listado.mercadolibre.com.ar/' + busqueda.replace(' ', '-').lower() + '#D[A:' + busqueda.lower() + ']'
            page = requests.get(url=URL, headers=HEADER, timeout=5)
            time.sleep(1)
            if page.status_code == 200:
                break
            elif 400 <= page.status_code <= 404:
                print(' ')
                print('La búsqueda no ha devuelto resultados. Intente nuevamente.')
                busqueda = ''
            else:
                print(' ')
                print('Error interno del servidor. Intente nuevamente.')
                busqueda = ''
        except requests.exceptions.ConnectionError or requests.exceptions.Timeout:
            print(' ')
            print('Excepción de timeout.')
            limiteTimeoutsGeneral += 1
            print('Intento ' + str(limiteTimeoutsGeneral) + ' de 3')
            if limiteTimeoutsGeneral == 3:
                abortarEjecucion = True

    while not abortarEjecucion:
        print('')
        print('Seleccione una condición de producto:')
        print(' ')
        print('0: Todos')
        print('1: Sólo Nuevos')
        print('2: Sólo Usados')
        print('')
        opcion = input('Ingrese una opción de condición de artículos: 0, 1 o 2: ')
        if opcion == '0' or opcion == '1' or opcion == '2':
            abortarEjecucion = False
            break
        else:
            print('')
            print('Su opción no está contemplada. Intente nuevamente.')

    while True:
        if ultimaPagina or abortarEjecucion:
            break
        try:
            page = requests.get(url=URL, headers=HEADER, timeout=5)
            limiteTimeoutsGeneral = 0
        except requests.exceptions.ConnectionError or requests.exceptions.Timeout:
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
                        except TypeError:
                            print('No hay artículos con esa condición en su búsqueda, '
                                  'volviendo a la opción "Todos" por default...')
                            opcion = '0'

                    condicion = None

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
                        print('Hay exactamente', str(cantidadArticulos), 'artículos con esa condición.')
                    else:
                        cantidadArticulos = 49 * cantidadPaginas
                        print('Hay aproximadamente', str(cantidadArticulos), 'artículos con esa condición.')

                    print('Puede traerlos todos o parte de ellos.')

                    while True:
                        print(' ')
                        anuncioCantidad = f'Ingrese 0 si desea todos los artículos ó ingrese una cantidad entre 1 y {cantidadArticulos}: '
                        limiteArticulos = int(input(anuncioCantidad))
                        try:
                            if limiteArticulos == 0 or limiteArticulos == cantidadArticulos:
                                tiempoEstimado = (cantidadPaginas + cantidadArticulos) * 1.4
                                break
                            elif 1 <= limiteArticulos < cantidadArticulos:
                                tiempoEstimado = (int(limiteArticulos / 49) + limiteArticulos) * 1.4
                                break
                            else:
                                print('Opción fuera de rango. Intente nuevamente.')
                        except ValueError:
                            print(' ')
                            print('Sólo se admiten números. Intente nuevamente.')

                    tiempo_inicio = time.time()
                    print(' ')
                    print('-----------------------------------------------')
                    print('Tiempo estimado calculado:', SegundosAHHMMSS(int(tiempoEstimado)))
                    print('-----------------------------------------------')
                    print(' ')

                try:
                    URL = str(soup.find('a', class_='andes-pagination__link ui-search-link',
                                        title='Siguiente')['href'])
                except TypeError:
                    ultimaPagina = True

                linksArticulos = [str(x['href'])
                                  for x in soup.find_all('a', class_='ui-search-item__group__element ui-search-link')
                                  if 'click1' not in str(x['href'])]

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
            except AttributeError:
                print('Sin conexión.')
            print('Abortando ejecución...')
            break

except KeyboardInterrupt:
    print(' ')
    print('Programa interrumpido manualmente.')
    print('Abortando ejecución...')

print(' ')
if len(df) > 0:
    if not os.path.exists('../resultados'):
        print('Carpeta "resultados" creada en la raiz del proyecto.')
        os.makedirs('../resultados')

    nombreArchivo = ''
    df['Precio'] = df['Precio'].astype(int)
    if opcion == '0':
        nombreArchivo = busqueda + ' - Todos'
    elif opcion == '1':
        nombreArchivo = busqueda + ' - Sólo Nuevos'
    elif opcion == '2':
        nombreArchivo = busqueda + ' - Sólo Usados'

    opcion = f'../resultados/'+str(nombreArchivo + '.xlsx')
    df.to_excel(opcion, index=False)
    print(str(f'Planilla de cálculos "{nombreArchivo}.xlsx" creada correctamente en la carpeta "resultados" en la raiz del proyecto.'))

    wb = openpyxl.load_workbook(filename=opcion)
    ws = wb.active
    for column_cells in ws.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length * 1.15

    wb.save(opcion)

else:
    print('Planilla de cálculos no fue creada. Cantidad nula de registros.')

if tiempo_inicio != 0:
    tiempoTotal = time.time() - tiempo_inicio
else:
    tiempoTotal = 0

print(' ')
print('Páginas visitadas:', paginasVisitadas)
print('Artículos recabados:', articulosRecabados)
print('Tiempo transcurrido:', SegundosAHHMMSS(tiempoTotal))
