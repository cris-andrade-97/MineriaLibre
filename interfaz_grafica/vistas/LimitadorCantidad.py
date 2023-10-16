import time

import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QWidget, QLabel

#from interfaz_grafica.lib import mineria
from lib import mineria
# from interfaz_grafica.vistas.Final import Ui_Final
from vistas.Final import Ui_Final
# from interfaz_grafica.lib.Hilo import HiloDeTrabajo
from lib.Hilo import HiloDeTrabajo


class Espera(QWidget):
    def __init__(self, tiempo):
        super().__init__()
        self.setWindowTitle("Espere")
        self.setFixedSize(525, 150)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setBold(True)
        font.setPointSize(12)
        self.label = QLabel('Espere mientras se recolectan los articulos...', self)
        tiempo_estimado = 'Tiempo estimado: '+ mineria.SegundosAHHMMSS(int(tiempo))
        self.tiempoLabel = QLabel(tiempo_estimado, self)
        self.tiempoLabel.setGeometry(10, 60, 501, 60)
        self.tiempoLabel.setFont(font)
        self.label.setGeometry(10, 30, 501, 60)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.tiempoLabel.setAlignment(QtCore.Qt.AlignCenter)


class Ui_LimitadorCantidad(object):
    def __init__(self, soup, busqueda, app, opcion):
        self.paginas = 1
        self.hiloDeTrabajo = None
        self.soup = soup
        self.app = app
        self.busqueda = busqueda
        self.cantidad = 0
        self.limitador = 0
        self.paginasDeArticulos = 0
        self.opcion = opcion
        self.esperar = None
        self.dataFrame = pd.DataFrame()
        self.tiempoInicio = 0

    def VentanaFinal(self):
        self.ventana = QtWidgets.QMainWindow()
        # def __init__(self, busqueda, opcion, dataFrame, paginas, app):
        self.uiFinal = Ui_Final(self.busqueda, self.opcion, self.dataFrame, self.paginasDeArticulos, self.app, self.tiempoInicio)
        self.uiFinal.setupUi(self.ventana)
        self.ventana.show()


    def setupUi(self, LimitadorCantidad):
        LimitadorCantidad.setObjectName("LimitadorCantidad")
        LimitadorCantidad.setFixedSize(556, 388)
        self.centralwidget = QtWidgets.QWidget(LimitadorCantidad)
        self.centralwidget.setObjectName("centralwidget")
        self.LimitadorTextBox = QtWidgets.QLineEdit(self.centralwidget)
        self.LimitadorTextBox.setGeometry(QtCore.QRect(90, 150, 381, 21))
        self.LimitadorTextBox.setMaximumSize(QtCore.QSize(500, 16777215))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        self.LimitadorTextBox.setFont(font)
        self.LimitadorTextBox.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.LimitadorTextBox.setObjectName("LimitadorTextBox")
        self.LimitadorLabel = QtWidgets.QLabel(self.centralwidget)
        self.LimitadorLabel.setGeometry(QtCore.QRect(20, 120, 521, 21))
        self.LimitadorLabel.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setBold(True)
        self.LimitadorLabel.setFont(font)
        self.LimitadorLabel.setObjectName("LimitadorLabel")
        self.Comenzar_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Comenzar_Button.setGeometry(QtCore.QRect(220, 300, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        self.Comenzar_Button.setFont(font)
        self.Comenzar_Button.setObjectName("Comenzar_Button")
        self.Comenzar_Button.clicked.connect(self.BotonComenzar)
        self.CantidadArtLabel = QtWidgets.QLabel(self.centralwidget)
        self.CantidadArtLabel.setGeometry(QtCore.QRect(20, 40, 521, 21))
        self.CantidadArtLabel.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(True)
        self.CantidadArtLabel.setFont(font)
        self.CantidadArtLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.CantidadArtLabel.setObjectName("CantidadArtLabel")
        self.AclaracionLabel = QtWidgets.QLabel(self.centralwidget)
        self.AclaracionLabel.setGeometry(QtCore.QRect(20, 60, 521, 21))
        self.AclaracionLabel.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(True)
        self.AclaracionLabel.setFont(font)
        self.AclaracionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.AclaracionLabel.setObjectName("AclaracionLabel")
        LimitadorCantidad.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(LimitadorCantidad)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 556, 22))
        self.menubar.setObjectName("menubar")
        LimitadorCantidad.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(LimitadorCantidad)
        self.statusbar.setObjectName("statusbar")
        LimitadorCantidad.setStatusBar(self.statusbar)

        self.retranslateUi(LimitadorCantidad)
        QtCore.QMetaObject.connectSlotsByName(LimitadorCantidad)

    def manejoResultadoHilo(self, result):
        self.dataFrame = result[0]
        self.paginasDeArticulos += result[1]
        self.VentanaFinal()

    def calculoTiempo(self, limitador, cantidadExacta, paginas):
        if limitador == 0 or limitador == cantidadExacta:
            return (paginas + cantidadExacta) * 2.9
        else:
            return (int(self.limitador / 49) + limitador) * 2.9

    def BotonComenzar(self):
        ok = False
        try:
            self.limitador = int(self.LimitadorTextBox.text())
            if mineria.LimitadorCantidad(cantidadArticulos=self.cantidad, limiteArticulos=self.limitador):
                ok = True
            else:
                msg = QMessageBox()
                msg.setWindowTitle('Valor fuera de rango')
                msg.setText('El número ingresado está fuera de los límites.\nIntente nuevamente.')
                x = msg.exec_()
        except ValueError:
            msg = QMessageBox()
            msg.setWindowTitle('Error de tipo de dato')
            msg.setText('Sólo se admiten números en este campo.\nIntente nuevamente.')
            x = msg.exec_()
        if ok:
            self.esperar = Espera(self.calculoTiempo(self.limitador, self.cantidad, self.paginas))
            self.app.closeAllWindows()
            self.esperar.show()
            self.hiloDeTrabajo = HiloDeTrabajo(self.soup, self.limitador, self.opcion)            
            self.hiloDeTrabajo.finished.connect(self.manejoResultadoHilo)
            self.tiempoInicio = time.time()
            self.hiloDeTrabajo.start()


    def CambiarLabels(self):
        cantidadArticulos =  mineria.CalcularCantidad(self.soup)
        self.cantidad = cantidadArticulos[0]
        self.paginas = cantidadArticulos[1]
        if cantidadArticulos[2]:
            self.CantidadArtLabel.setText(f'Hay exactamente {cantidadArticulos[0]} artículos con esa condición.')
        else:
            self.CantidadArtLabel.setText(f'Hay aproximadamente {cantidadArticulos[0]} artículos con esa condición.')
        self.LimitadorLabel.setText(f'Ingrese 0 si desea todos los artículos ó ingrese una cantidad entre 1 y {cantidadArticulos[0]}: ')

    def retranslateUi(self, LimitadorCantidad):
        _translate = QtCore.QCoreApplication.translate
        LimitadorCantidad.setWindowTitle(_translate("LimitadorCantidad", "Limitar la búsqueda"))
        self.CambiarLabels()
        self.Comenzar_Button.setText(_translate("LimitadorCantidad", "¡Comenzar!"))
        self.AclaracionLabel.setText(_translate("LimitadorCantidad", "Puede traerlos todos o parte de ellos"))

