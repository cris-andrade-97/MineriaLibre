# MineriaLibre

## Introducción
MineriaLibre es un algoritmo dedicado a extraer datos de los artículos en MercadoLibre y en base a una búsqueda cualquiera. Se adapta satisfactoriamente a cada artículo para almacenar todos o la mayoría de los registros en una planilla de cálculo.

## Objetivos del proyecto
- Realizar una búsqueda en MercadoLibre a elección 
- Aplicar filtros de condición de artículo a elección
- Navegar los resultados con un algoritmo de web scraping
- Recabar los artículos limitando la cantidad de los mismos a elección
- Amoldar los registros al set de datos y/o viceversa
- Entregarle al usuario una planilla con los artículos recabados
- Robustez ante la posibilidad de timeouts del lado servidor o malas conexiones a internet
- Desarrollar una interfaz que le facilite la búsqueda e informe de resultados

## Alcances y limitaciones
- Sólo aplicable al sitio web MercadoLibre
- Limitación de velocidad de solicitudes
- Variabilidad en el tiempo estimado
- Búsquedas imprecisas pueden afectar la calidad de los registros
- Sólo se puede aplicar un filtro

## Tecnologías usadas
- PyCharm IDE
- pandas
- numpy
- bs4
- Git
- GitHub
- PyQt5

## Instrucciones de instalación
Abra la terminal de su sistema operativo y siga los pasos:

<b>Ubuntu y derivados</b>: 
- ```sudo apt update```
- ```sudo apt install python3 python3-pip git```
- ```pip install pandas numpy bs4 openpyxl pyqt5 requests```

<b>Microsoft Windows</b>:
- Descargue e instale la última versión de <a href='https://www.python.org/downloads/'>Python3</a> (3.12 al momento de redactar este readme)
- Descargue e instale la última versión de <a href='https://git-scm.com/download/win'>Git</a> (2.42.0 al momento de redactar este readme)
- Abra la terminal de Windows con privilegios de administrador e ingrese los siguientes comandos en orden:
	- ```curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py```
	- ```python get-pip.py```
	- ```pip install pandas numpy bs4 openpyxl requests pyqt5```

## Ejecución
<b>Versión con interfaz gráfica</b>:
- Abra la terminal de su sistema operativo.
- Clone este repositorio en la carpeta que desee con el comando ```git clone https://github.com/cris-andrade-97/MineriaLibre```
- Llame a la carpeta de esta versión con ```cd MineriaLibre/interfaz_grafica```
- Ejecute el programa con ```python run.py```

<b>Versión en línea de comandos</b>:
- Abra la terminal de su sistema operativo.
- Clone este repositorio en la carpeta que desee con el comando ```git clone https://github.com/cris-andrade-97/MineriaLibre```
- Llame a la carpeta de esta versión con ```cd MineriaLibre/linea_comandos```
- Ejecute el programa con ```python mineria.py```

