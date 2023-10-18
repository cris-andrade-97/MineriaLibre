import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from lib import mineria
# from PyQt5.QtCore import Qt
# import pandas as pd
# from interfaz_grafica.lib import mineria
# from interfaz_grafica.vistas.Busqueda import Ui_Busqueda

class Ui_Final(object):
    def __init__(self, paginas, app, tiempo_inicial, carpetaNueva, largoFinalSet):
       self.paginasDeArticulos = paginas
       self.app = app
       self.tiempoInicial = tiempo_inicial
       self.carpetaNueva = carpetaNueva
       self.URL = ''
       self.abortar = False
       self.largoFinalSet = largoFinalSet


    def setupUi(self, Final):
        Final.setObjectName("Final")
        Final.setFixedSize(648, 374)
        self.centralwidget = QtWidgets.QWidget(Final)
        self.centralwidget.setObjectName("centralwidget")
        self.FinalLabel = QtWidgets.QLabel(self.centralwidget)
        self.FinalLabel.setGeometry(QtCore.QRect(20, 30, 611, 40))
        self.FinalLabel.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(12)
        font.setBold(True)
        self.FinalLabel.setFont(font)
        self.FinalLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.FinalLabel.setObjectName("FinalLabel")
        self.SalirButton = QtWidgets.QPushButton(self.centralwidget)
        self.SalirButton.setGeometry(QtCore.QRect(520, 290, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        self.SalirButton.setFont(font)
        self.SalirButton.setObjectName("SalirButton")
        self.SalirButton.clicked.connect(self.AccionSalir)
        self.TiempoTranscurLabel = QtWidgets.QLabel(self.centralwidget)
        self.TiempoTranscurLabel.setGeometry(QtCore.QRect(20, 200, 611, 21))
        self.TiempoTranscurLabel.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setBold(True)
        self.TiempoTranscurLabel.setFont(font)
        self.TiempoTranscurLabel.setObjectName("TiempoTranscurLabel")
        self.ArtRecabadosLabel = QtWidgets.QLabel(self.centralwidget)
        self.ArtRecabadosLabel.setGeometry(QtCore.QRect(20, 170, 611, 21))
        self.ArtRecabadosLabel.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setBold(True)
        self.ArtRecabadosLabel.setFont(font)
        self.ArtRecabadosLabel.setObjectName("ArtRecabadosLabel")
        self.PagVisitadasLabel = QtWidgets.QLabel(self.centralwidget)
        self.PagVisitadasLabel.setGeometry(QtCore.QRect(20, 140, 611, 21))
        self.PagVisitadasLabel.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setBold(True)
        self.PagVisitadasLabel.setFont(font)
        self.PagVisitadasLabel.setObjectName("PagVisitadasLabel")
        self.ResultadosLabel = QtWidgets.QLabel(self.centralwidget)
        self.ResultadosLabel.setGeometry(QtCore.QRect(18, 80, 611, 20))
        self.ResultadosLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ResultadosLabel.setObjectName("ResultadosLabel")
        self.VolverInicioButton = QtWidgets.QPushButton(self.centralwidget)
        self.VolverInicioButton.clicked.connect(self.AccionInicio)
        self.VolverInicioButton.setGeometry(QtCore.QRect(20, 290, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        self.VolverInicioButton.setFont(font)
        self.VolverInicioButton.setObjectName("VolverInicioButton")
        Final.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Final)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 481, 22))
        self.menubar.setObjectName("menubar")
        Final.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Final)
        self.statusbar.setObjectName("statusbar")
        Final.setStatusBar(self.statusbar)
        self.retranslateUi(Final)
        QtCore.QMetaObject.connectSlotsByName(Final)

    def AccionSalir(self):
        self.app.closeAllWindows()
        quit()

    def AccionInicio(self):
        from vistas.Busqueda import Ui_Busqueda
        self.app.closeAllWindows()
        self.ventana = QtWidgets.QMainWindow()
        self.inicio = Ui_Busqueda(self.app)
        self.inicio.setupUi(self.ventana)
        self.ventana.show()

    def retranslateUi(self, Final):
        self.app.closeAllWindows()
        tiempo = mineria.SegundosAHHMMSS(time.time() - self.tiempoInicial)
        _translate = QtCore.QCoreApplication.translate
        Final.setWindowTitle(_translate("Final", "Fin de recolección"))
        self.FinalLabel.setText(_translate("Final", "¡Recolección finalizada!"))

        if self.carpetaNueva:
            msg = QMessageBox()
            msg.setWindowTitle('Carpeta \'resultados\' creada')
            msg.setText('La carpeta \'resultados\' fue creada existosamente.')
            x = msg.exec_()

        self.PagVisitadasLabel.setText(f'Páginas recorridas: {self.paginasDeArticulos}')
        self.ArtRecabadosLabel.setText(f'Artículos recabados: {self.largoFinalSet}')
        self.TiempoTranscurLabel.setText(f'Tiempo transcurrido: {tiempo}')
        self.VolverInicioButton.setText(_translate("Busqueda", "Volver al inicio"))

        self.SalirButton.setText(_translate("Final", "Salir"))

        self.ResultadosLabel.setText(_translate("Final", "Su planilla fue almacenada en la carpeta \'resultados\', ubicada en la raiz del proyecto."))
