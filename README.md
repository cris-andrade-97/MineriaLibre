# MineriaLibre

## Introducción
MineriaLibre es un algoritmo dedicado a extraer datos de los artículos en MercadoLibre y en base a una búsqueda cualquiera. Se adapta satisfactoriamente a cada artículo para almacenar todos o la mayoría de los registros en una planilla de cálculo.

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
- ```pip install pandas numpy bs4 openpyxl pyqt5```

<b>Microsoft Windows</b>:
- Descargue e instale la última versión de <a href='https://www.python.org/downloads/'>Python3</a> (3.12 al momento de redactar este readme)
- Descargue e instale la última versión de <a href='https://git-scm.com/download/win'>Git</a> (2.42.0 al momento de redactar este readme)
- Abra la terminal de Windows con privilegios de administrador e ingrese los siguientes comandos en orden:
	- ```curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py```
	- ```python get-pip.py```
	- ```pip install pandas numpy bs4 openpyxl requests pyqt5```

## Ejecución
<b>Versión con interfaz gráfica</b>:
- Abra la terminal de su sistema operativo con privilegios de administrador o con superusuario.
- Clone este repositorio en la carpeta que desee con el comando ```git clone https://github.com/cris-andrade-97/MineriaLibre```
- Llame a la carpeta del proyecto con ```cd MineriaLibre```
- Ejecute el programa con ```python ./vistas/VentanaInicio.py```

<b>Versión en línea de comandos</b>:
- Abra la terminal de su sistema operativo con privilegios de administrador o con superusuario.
- Clone este repositorio en la carpeta que desee con el comando ```git clone https://github.com/cris-andrade-97/MineriaLibre```
- Llame a la carpeta del proyecto con ```cd MineriaLibre```
- Ejecute el programa con ```python ./old/mineria.py```

