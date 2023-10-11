import os
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import pandas as pd
import mineria


class Ui_Final(object):

    def __init__(self, busqueda, soup, limitador, app):
        self.app = app
        self.limitador = limitador
        self.tiempoInicial = time.time()
        self.dataFrame = pd.DataFrame()
        self.busqueda = busqueda
        self.paginasDeArticulos = 0
        self.soup = soup
        self.URL = ''
        self.abortar = False

    def setupUi(self, Final):
        Final.setObjectName("Final")
        Final.resize(648, 374)
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
        self.SalirButton.setGeometry(QtCore.QRect(260, 290, 111, 31))
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

    def Scraping(self, firstSoup):
        resultadoScraping = mineria.Scraping(self.soup, self.dataFrame, self.limitador, self.URL, firstSoup)
        self.dataFrame = resultadoScraping[0]
        self.paginasDeArticulos += resultadoScraping[1]
        self.abortar = resultadoScraping[2]
        self.URL = resultadoScraping[3]

    def retranslateUi(self, Final):
        self.Scraping(True)
        while not self.abortar:
            self.soup = None
            self.Scraping(False)

        self.app.closeAllWindows()
        tiempo = mineria.SegundosAHHMMSS(time.time() - self.tiempoInicial)
        _translate = QtCore.QCoreApplication.translate
        Final.setWindowTitle(_translate("Final", "Fin de recolección"))
        self.FinalLabel.setText(_translate("Final", "¡Recolección finalizada!"))

        self.PagVisitadasLabel.setText(f'Páginas recorridas: {self.paginasDeArticulos}')
        self.ArtRecabadosLabel.setText(f'Artículos recabados: {len(self.dataFrame)}')
        self.TiempoTranscurLabel.setText(f'Tiempo transcurrido: {tiempo}')

        if not os.path.exists('../resultados'):
            msg = QMessageBox()
            msg.setWindowTitle('Carpeta "resultados"')
            msg.setText('Carpeta resultados creada en la raiz del proyecto.')
            x = msg.exec_()
            os.makedirs('../resultados')

        self.dataFrame['Precio'] = self.dataFrame['Precio'].astype(int)
        self.dataFrame.to_excel(str('../resultados/' + self.busqueda + '.xlsx'), index=False)

        self.SalirButton.setText(_translate("Final", "Salir"))

        self.ResultadosLabel.setText(_translate("Final", "Su planilla fue almacenada en la carpeta \'resultados\', ubicada en la raiz del proyecto."))
