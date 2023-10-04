# MineriaLibre

## Introducción
MineriaWeb es un algoritmo dedicado a extraer datos de los artículos en MercadoLibre y en base a una búsqueda cualquiera. Se adapta satisfactoriamente a cada artículo para almacenar todos o la mayoría de los registros en una planilla de cálculo.

## Tecnologías usadas
- PyCharm IDE
- pandas
- numpy
- bs4
- Git
- GitHub

## Instrucciones de instalación
Abra la terminal de su sistema operativo y siga los pasos:

<b>Ubuntu y derivados</b>: 
- ```sudo apt update```
- ```sudo apt install python3 python3-pip git```
- ```pip install pandas numpy bs4 odfpy openpyxl```

<b>Arch Linux</b>: 
- ```sudo pacman -Syu```
- ```sudo pacman -S python python-pip git```
- ```pip install pandas numpy bs4 odfpy openpyxl```

<b>Debian</b>: 
- ```sudo apt-get update```
- ```sudo apt-get install python3 python-pip git```
- ```pip install pandas numpy bs4 odfpy openpyxl --break-system-packages```

<b>Microsoft Windows</b>:
- Instale la última versión de <a href='https://www.python.org/downloads/'>Python3</a> (3.12 al momento de redactar este readme)
- Instale la última versión de <a href='https://git-scm.com/download/win'>Git</a> (2.42.0 al momento de redactar este readme)
- ```curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py```
- ```python get-pip.py```
- ```pip install pandas numpy bs4 odfpy openpyxl```

## Ejecución
Abra la terminal de su sistema operativo y siga los pasos:

- Clone este repositorio en la carpeta que desee con el comando ```git clone https://github.com/cris-andrade-97/MineriaLibre```.
- Llame a la carpeta del proyecto con ```cd MineriaLibre```
- Dependiendo de su sistema operativo, ejecute el programa con ```python mineria.py``` o con ```python3 mineria.py```.

