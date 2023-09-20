import pandas
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time

HEADER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"}

busqueda = input('Ingrese su búsqueda: ')

URL = 'https://listado.mercadolibre.com.ar/' + busqueda.replace(' ', '-').lower() + '#D[A:' + busqueda.lower() + ']'

df = pandas.DataFrame()

primerRegistro = True

while True:
    page = requests.get(url=URL, headers=HEADER)
    time.sleep(1)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')

        linksArticulos = [str(x['href'])
                          for x in soup.find_all('a', class_='ui-search-item__group__element shops__items-group-details ui-search-link')
                          if 'click1' not in str(x['href'])]

        for articulo in linksArticulos:
            especificaciones = []
            while True:
                page = requests.get(articulo, headers=HEADER)

                soup = BeautifulSoup(page.content, 'html.parser')
                especificaciones = soup.find_all('tr', class_='andes-table__row ui-vpp-striped-specs__row')
                if len(especificaciones) > 0:
                    break

            cabeceras = [cabecera.find('th').text.strip() for cabecera in especificaciones]
            datos = [dato.find('td').text.strip() for dato in especificaciones]
            datosOrdenados = []
            cabecerasOrdenadas = []

            print(cabeceras)
            print(datos)

            if primerRegistro:
                primerRegistro = False
                df.columns = cabeceras
                df.loc[df.shape[0]] = datos
            else:
                if set(cabeceras).issubset(df.columns) and len(cabeceras) == len(df.columns):
                    indicesCabeceras = [cabeceras.index(column) for column in df.columns]
                    datosOrdenados = [datos[i] for i in indicesCabeceras]
                    df.loc[df.shape[0]] = datosOrdenados
                elif set(cabeceras).issubset(df.columns) and len(cabeceras) < len(df.columns):
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
                            datosOrdenados.append(None)

        proximaPagina = str(
            soup.find('a', class_='andes-pagination__link shops__pagination-link ui-search-link')['href'])

