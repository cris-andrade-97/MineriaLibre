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

df = pd.DataFrame()

primerRegistro = True

hayPrecio = True

URL = 'https://listado.mercadolibre.com.ar/' + busqueda.replace(' ', '-').lower() + '#D[A:' + busqueda.lower() + ']'

'''
page = requests.get(url=URL, headers=HEADER)

BeautifulSoup(page.content, 'html.parser')

def condicionArticuloURL(opcion):
    if opcion == 0:
        return
'''

while True:

    if ultimaPagina:
        break

    page = requests.get(url=URL, headers=HEADER)
    time.sleep(1)

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
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
            especificaciones = []
            while True:
                page = requests.get(articulo, headers=HEADER)
                time.sleep(1)
                soup = BeautifulSoup(page.content, 'html.parser')
                especificaciones = soup.find_all('tr', class_='andes-table__row')
                if len(especificaciones) > 0:
                    break

            cabeceras = [cabecera.find('th').text.strip() for cabecera in especificaciones]
            datos = [dato.find('td').text.strip() for dato in especificaciones]
            datosOrdenados = []
            cabecerasOrdenadas = []
            unidadMonetaria = str(soup.find('span', class_='andes-money-amount__currency-symbol').text.strip())
            precio = 0
            try:
                precio = int(str(soup.find('span', class_='andes-money-amount__fraction').text.strip()).replace('.', ''))
            except:
                hayPrecio = False

            if hayPrecio:
                if primerRegistro:
                    primerRegistro = False
                    cabeceras.append('Unidad Monetaria')
                    cabeceras.append('Precio')
                    datos.append(unidadMonetaria)
                    datos.append(precio)
                    df = pd.DataFrame(columns=cabeceras)
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

            print(len(df))
            df.to_csv(str(nombreArchivo))
